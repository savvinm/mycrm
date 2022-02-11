from django.db import models

class User(models.Model):
    login = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    fullname = models.CharField(max_length=128)
    role = models.CharField(max_length=16)

class Request(models.Model):
    creator = models.CharField(max_length=128)
    description = models.TextField()
    phoneNumber = models.CharField(max_length=16)
    email = models.TextField(max_length=128)
    additional = models.TextField()
    status = models.CharField(max_length=16)

class Project(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=16)
    deadline = models.DateField()
    creationDate = models.DateField()

class Task(models.Model):
    executor = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.TextField()
    status = models.CharField(max_length=16)
    creationDate = models.DateField()
