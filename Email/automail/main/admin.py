from django.contrib import admin
from .models import Employee,Log

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display=['id','name','birthday','doj']


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display=['id','date','emp_id','emp_name','event']