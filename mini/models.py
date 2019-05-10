from django.db import models



# Create your models here.
class maintenance(models.Model):
    image=models.ImageField(upload_to='static/')

class STUDENT_REGISTER(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    institute_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class WORKER_REGISTER1(models.Model):

    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class REGISTRATIONS(models.Model):
    status=models.CharField(max_length=200,default="available")
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    institute_name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

class LOGIN_DETAILS(models.Model):
    email_id=models.CharField(max_length=100)
    password=models.CharField(max_length=100)

class ALL_PROBLEMS1(models.Model):
    problem_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=1000)
    location = models.CharField(max_length = 1000)
    image=models.ImageField(upload_to='static/uploads/')
    status=models.CharField(max_length=100)
    worker_name = models.CharField(max_length=100)
    problem_type = models.CharField(max_length=20)
    report_date = models.CharField(max_length=100)
    completion_date = models.CharField(max_length=100)

class TEMP_PROBLEMS(models.Model):
    description = models.CharField(max_length=1000)
    location = models.CharField(max_length = 1000)
    image=models.ImageField(upload_to='static/uploads/')
    status=models.CharField(max_length=100)

class TEMP_REPORT(models.Model):
    worker_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='static/uploads/completed/')
    date = models.CharField(max_length=100)

class WORKER_REPORT(models.Model):
    worker_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    image = models.ImageField(upload_to='static/uploads/completed/')
    date = models.CharField(max_length=100)

class adminlog(models.Model):
    name=models.CharField(max_length=100)
    email_id=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
