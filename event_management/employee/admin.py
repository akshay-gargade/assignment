from django.contrib import admin
from .models import Employee, EmailTemplate, Event, EmailLog

admin.site.register(Employee)
admin.site.register(EmailTemplate)
admin.site.register(EmailLog)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'employee', 'employee_email')

    def employee_email(self, obj):
        return obj.employee.email
