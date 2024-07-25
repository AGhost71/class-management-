from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Student, Teacher,classroom,assignment
from .models import Submission

class StudentSignUpForm(UserCreationForm):
    PhoneNumber = forms.CharField(max_length=15, required=True)
    Picture = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('PhoneNumber', 'Picture')

    def save(self, commit=True):
        print(self.fields)
        user = super().save(commit=False)
        user.is_student = True
        user.PhoneNumber= self.cleaned_data.get('PhoneNumber')
        user.Picture = self.cleaned_data.get('Picture')
        if commit:
            user.save()
            Student.objects.get_or_create(user=user)
        return user

class TeacherSignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=True)
    profile_picture = forms.ImageField(required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ( 'PhoneNumber', 'Picture')

    def save(self, commit=True):
        print(self.fields)
        user = super().save(commit=False)
        user.is_teacher = True
        user.PhoneNumber = self.cleaned_data.get('PhoneNumber')
        user.Picture = self.cleaned_data.get('Picture')
        if commit:
            user.save()
            Teacher.objects.get_or_create(user=user)
        return user
    


class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['file']

class GradeUpdateForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['grade']

class ClassForm(forms.ModelForm):
    class Meta:
        model = classroom
        fields = ['class_name']

class AssignmentForm(forms.ModelForm):
    class Meta:
        model = assignment
        fields = ['title', 'Description', 'File']