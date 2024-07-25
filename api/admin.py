from django.contrib import admin

# Register your models here.
from .models import CustomUser, Student, Teacher, classroom, assignment, Submission

admin.site.register(CustomUser)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(classroom)
admin.site.register(assignment)
admin.site.register(Submission)