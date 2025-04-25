from django.contrib import admin
# Register your models here.
from time_tracker.models import Department, JobRole, EmployeeProfile, Timesheet, AnnualLeave

admin.site.register(Department)
admin.site.register(JobRole)
admin.site.register(EmployeeProfile)
admin.site.register(Timesheet)
admin.site.register(AnnualLeave)

