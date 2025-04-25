from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.shortcuts import render
from django.template import Context
from django.template import RequestContext
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from time_tracker.models import Timesheet
from time_tracker.models import AnnualLeave 
import datetime
now = datetime.datetime.now(datetime.timezone.utc)

def clock_action(request, user): # Define function, accept a request and user details
    """Receives the users input e.g. clock in / out actions, stores and retrieves records to and from the database"""
    # When the employee clocks in/out the post is received, the date and time is recorded and it is logged to the employees user_id
    clock_action = request.POST.get('clock_action','')  
    now = datetime.datetime.now().replace(tzinfo=now)
    logged_status = Timesheet.objects.filter(employee=user).latest()
    # when the employee logs in they can not log in again until they logout first 
    if clock_action == "ClockIn":
        if logged_status.logging == "OUT":
            timesheet = Timesheet(employee=user, recorded_by=user, clocking_time=now, logging="IN", ip_address=request.META.get('REMOTE_ADDR','NA'))
            timesheet.save()
            return HttpResponseRedirect('/timesheet_success/in/?time=%s' % now)
        else:
            error_message = "You must clock out before you can clock in.\n"
    # when the employee logs out they can not log out again until they login first
    elif clock_action == "ClockOut":
        if logged_status.logging == "IN":
            delta = now - logged_status.clocking_time
            hours = delta.total_seconds() / 3600.
            max_hours = 12
            # the employee cannot clock out more than 12 hours after the previous clock in
            if hours < max_hours:            
                timesheet = Timesheet(employee=user, recorded_by=user, clocking_time=now, logging="OUT", ip_address=request.META.get('REMOTE_ADDR','NA'))
                timesheet.save()
                return HttpResponseRedirect('/timesheet_success/out/?time=%s' % now)
            else:
                error_message = "You cannot clock out more than %s hours after previous clock in. Please report to manager.\n" % max_hours        
        else:
            error_message = "You must clock in before you can clock out.\n"        
    else:
        error_message = "Massive Error.\n"
    # errors are displayed if conditions are not satisfied
    return render(request, "index.html", {'error_message': error_message})

    
def holiday_request(request, user):
    """ Takes the date and time that the employee requested from / to """ 
    holiday_request = request.POST.get('holiday_request','')
    if holiday_request == "HolidayRequest":
        holiday_req = AnnualLeave(employee=user, recorded_by=user, status=1)
        date_from = request.POST.get('date_from')
        time_from = request.POST.get('time_from')
        date_to = request.POST.get('date_to')
        time_to = request.POST.get('time_to')
        holiday_req.date_from = "%s %s" % (date_from, time_from)
        holiday_req.date_to = "%s %s" % (date_to, time_to)
        holiday_req.save()
        # displays a pending message to the employeee
        return HttpResponseRedirect('/vacation_pending/?datetimefrom=%s&datetimeto=%s' % (holiday_req.date_from, holiday_req.date_to))
    else:
        # error is displayed if conditions are not satisfied
        error_message = "Incorrect Holiday Request Action.\n"
        return render(request, "index.html", {'error_message': error_message})

def index(request):
    
    error_message = ""
    
    if request.method == "POST":
            # authenticate the user
            username = request.POST.get('employee_id','')
            password = request.POST.get('password','')
            user = auth.authenticate(username=username, password=password)
            # if empty an error message is displayed 
            if user is not None:
                # if its a clock in/out action or holiday request action its processed 
                if 'clock_action' in request.POST:
                    return clock_action(request,user)
                elif 'holiday_request' in request.POST:
                    return holiday_request(request,user)                   
            else:
                error_message = "Incorrect Username/Password.\n"
    # error is displayed if conditions are not satisfied
    return render(request, "index.html", {'error_message': error_message})

def timesheet_success(request, in_or_out): # Define function, accept a request and in_or_out
    """ displays to the employee the date and time that they logged in or out """

    timestamp = request.GET.get('time','Error')

    return render(request, "timesheet_success.html", {'in_or_out':in_or_out, 'timestamp':timestamp})

def vacation_pending(request):
    """ displays to the employee the dates and times that they requested holidays form / to  """

    date_time_from = request.GET.get('datetimefrom','Error')
    
    date_time_to = request.GET.get('datetimeto','Error')

    return render(request, "vacation_pending.html", {'date_time_from':date_time_from, 'date_time_to':date_time_to,})    


def login(request):
    return render(request, "login.html", {})

def auth_view(request): 
    """ Authenticates the employees id and password """
    username = request.POST.get('employee_id', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)
    # if the form is empty or incorrect details are entered an error is displayed
    if user is not None:
        auth.login(request, user)
        return HttpResponseRedirect('/loggedin')
    else:
        return HttpResponseRedirect('/invalid_login')

@login_required
def holiday_request_action(request, action, holiday_request_id): # Define function, accept a request, action and holiday_request_id
    """ Managemnent login is required. Enables the manager to approve, reject and cancel holiday requests """
    if action == "approve":
        annual_leave = AnnualLeave.objects.get(id=holiday_request_id)
        annual_leave.status = 2
        annual_leave.save()
        return HttpResponseRedirect('/loggedin/')
    elif action == "reject":                    
        annual_leave = AnnualLeave.objects.get(id=holiday_request_id)
        annual_leave.status = 3
        annual_leave.save()
        return HttpResponseRedirect('/loggedin/')
    elif action == "cancel":                    
        annual_leave = AnnualLeave.objects.get(id=holiday_request_id)
        annual_leave.status = 4
        annual_leave.save()
        return HttpResponseRedirect('/loggedin/')
    else:
        # display error massage
        error_message = "Incorrect Holiday Request Action.\n"
        return render(request, "loggedin.html", {'error_message':error_message})
    


@login_required
def mgnt_clocking(request): #Define function, accept a request 
    """ Managemnent login is required. Enables the manager to clock in/out an employee """
    if request.method == "POST":
        # the employees id, and the managers clock action in/out 
        username = request.POST.get('employee_id', '')        
        mgnt_clock_action = request.POST.get('mgnt_clock_action','')
        # 
        try:
            employee = User.objects.get(username=username)

            if mgnt_clock_action == "ClockIn":
                clockin_date = request.POST.get('clockin_date')
                clockin_time = request.POST.get('clockin_time')
                # create Timesheet with logging = IN, time = now
                timesheet = Timesheet(employee=employee, recorded_by=request.user, logging="IN", ip_address=request.META.get('REMOTE_ADDR','NA'))
                timesheet.clocking_time = "%s %s" % (clockin_date, clockin_time)
                timesheet.save()
                return HttpResponseRedirect('/loggedin/')
            elif mgnt_clock_action == "ClockOut":
                clockin_date = request.POST.get('clockin_date')
                clockin_time = request.POST.get('clockin_time')
                # create Timesheet with logging = IN, time = now
                timesheet = Timesheet(employee=employee, recorded_by=request.user, logging="OUT", ip_address=request.META.get('REMOTE_ADDR','NA'))
                timesheet.clocking_time = "%s %s" % (clockin_date, clockin_time)
                timesheet.save()
                return HttpResponseRedirect('/loggedin/')
        except Exception as e:
            return render(request, "loggedin.html", {'error_message':"%s"%e})
        else:
            return HttpResponseRedirect('/loggedin/')

@login_required
def loggedin(request):  # Define function, accept a request 
    """ Managemnent login is required. Enables the manager to view and edit employees timesheets, holidays requests and sick leave """
    # ORM queries the database for all of the entries.
    timesheets = Timesheet.objects.all() 
    holiday_requests = AnnualLeave.objects.all()
   

    error_message = ""
    
    # Responds with passing the object items (contains info from the DB) to the template loggedin.html 
    return render(request, "loggedin.html", {'error_message':error_message, 'full_name':request.user.username, 'timesheets': timesheets, 'holiday_requests': holiday_requests,}) 

def invalid_login(request):
    """ invalid login responce """
    return render('invalid_login.html')

def logout(request):
    """ logout responce """
    auth.logout(request)
    return render('logout.html')




