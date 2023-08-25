from django.db import models
from datetime import date


class Employee(models.Model):
    """
    Employee model fields
    """
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    dob = models.DateField()
    doj = models.DateField()

    def calculate_work_anniversary(self):
        """
        Return the no of years from date of joining
        """

        today = date.today()
        work_anniversary = today.year - self.doj.year
        return work_anniversary

    def __str__(self):
        return self.name


class Event(models.Model):
    """
    Event model fields
    """
    name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EmailTemplate(models.Model):
    """
    EmailTemplate model fields
    """
    name = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    content = models.TextField()

    def __str__(self):
        return self.name


class EmailLog(models.Model):
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    status = models.CharField(max_length=10)  # 'success' or 'failure'
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recipient
