from django.urls import path, include
from .views import send_event_emails

urlpatterns = [
    path('send_event_emails/', send_event_emails, name='send_event_emails'),

]
