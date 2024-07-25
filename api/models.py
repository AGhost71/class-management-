from django.db import models
from django.urls import reverse
# Create your models here.
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import RegexValidator

class CustomUser(AbstractUser):
    PhoneNumber = models.CharField( max_length=12,validators = [RegexValidator(regex = r"^\0?\d{10}$",message="phonenumber must be numeric",code = "invalid phonenumber"),])
    Picture = models.ImageField(upload_to="profilepictures")
    is_teacher = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    objects = UserManager()

class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

class classroom(models.Model):
    classteacher = models.ForeignKey(Teacher,on_delete=models.CASCADE)
    classstudent = models.ManyToManyField(Student)
    class_name = models.CharField(max_length=100)

    def __str__(self):
        return self.class_name
    def get_absolute_url(self):
        return reverse('class_detail', args=[str(self.id)])

class assignment(models.Model):
    title = models.CharField(max_length=300)
    Class_room = models.ForeignKey(classroom,on_delete=models.CASCADE)
    UploadDate = models.DateTimeField(auto_now_add=True)
    Description = models.CharField(max_length=1000)
    File = models.FileField(upload_to="Assignment")
    def get_absolute_url(self):
        return reverse('assignment_detail', args=[str(self.id)])
    
class Submission(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    assignment = models.ForeignKey(assignment, on_delete=models.CASCADE, related_name="submission_assignment")
    upload_date = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to="submissions")
    grade = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.student.user.username}'

