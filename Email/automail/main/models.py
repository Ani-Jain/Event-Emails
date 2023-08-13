from django.db import models

class Employee(models.Model):
    name=models.CharField(max_length=100)
    birthday= models.DateField()
    doj= models.DateField()
    email = models.EmailField(max_length=254)

    def __str__(self):
        return self.name
    

class Log(models.Model):
    date = models.DateField()
    emp_id = models.IntegerField()
    emp_name = models.CharField(max_length=100)
    event = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)

    def __str__(self):
        return (self.emp_name + self.event)

