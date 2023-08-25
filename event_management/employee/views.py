from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import date
from celery import shared_task

from employee.models import Employee, Event, EmailTemplate, EmailLog
from event_management.settings import EMAIL_HOST_USER


@shared_task
def send_event_emails(self):
    """
    This function is used to fetch current date events and according to event it fetches template and send the mails
    to  users.
    """

    today = date.today()
    employee_birthday = Employee.objects.filter(dob__month=today.month, dob__day=today.day)
    employee_work_anniversary = Employee.objects.filter(doj__month=today.month, doj__day=today.day)

    if len(employee_birthday) >= 1:
        birthday_template = EmailTemplate.objects.filter(name='Birthday').first()
        for user in employee_birthday:
            employee_instance = Employee.objects.get(pk=user.id)
            subject = 'Happy Birthday!'
            from_email = EMAIL_HOST_USER
            recipient_list = [user.email]
            template_name = 'birthday.html'
            message = render_to_string(template_name, {'user': user, 'birthday_template': birthday_template})

            try:
                response = send_mail(subject, '', from_email, recipient_list, html_message=message)
                if response == 1:
                    Event.objects.create(name=birthday_template.name, employee=employee_instance)
                    EmailLog.objects.create(recipient=recipient_list, subject=subject, status='success')
                else:
                    EmailLog.objects.create(recipient=recipient_list, subject=subject, status='failed')

            except Exception as e:
                EmailLog.objects.create(recipient=recipient_list, subject=subject, status='failed')

        if len(employee_work_anniversary) >= 1:
            anniversary_template = EmailTemplate.objects.filter(name='Anniversary').first()
            for user in employee_work_anniversary:
                duration = user.calculate_work_anniversary()
                formatted_content = anniversary_template.content.format(user.name, duration, duration, duration)
                employee_instance = Employee.objects.get(pk=user.id)
                context = {
                    'user': user,
                    'duration': user.calculate_work_anniversary(),
                    'formatted_content': formatted_content,
                }
                subject = 'Happy Work Aniiversary!'
                from_email = EMAIL_HOST_USER
                recipient_list = [user.email]
                template_name = 'work_anniversary.html'
                message = render_to_string(template_name, context)

                try:
                    response = send_mail(subject, '', from_email, recipient_list, html_message=message)
                    if response == 1:
                        Event.objects.create(name=anniversary_template.name, employee=employee_instance)
                        EmailLog.objects.create(recipient=recipient_list, subject=subject, status='success')
                    else:
                        EmailLog.objects.create(recipient=recipient_list, subject=subject, status='failed')

                except Exception as e:
                    EmailLog.objects.create(recipient=recipient_list, subject=subject, status='failed')

        return HttpResponse("Event emails sent successfully")
    else:
        return HttpResponse("Today there is no event!!")
