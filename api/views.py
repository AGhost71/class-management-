from django.views import View
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect,reverse
from django.urls import reverse_lazy
from .models import classroom, Teacher,Student,CustomUser,assignment,Submission
from django.contrib.auth import login
from django.views.generic import ListView,TemplateView
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView
from .forms import SubmissionForm,GradeUpdateForm,StudentSignUpForm, TeacherSignUpForm,ClassForm
from django.core.exceptions import PermissionDenied
from django.views.generic.edit import UpdateView

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home')

class TeacherRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_teacher

class ClassCreateView(LoginRequiredMixin, TeacherRequiredMixin, CreateView):
    model = classroom
    form_class = ClassForm
    template_name = 'craeteclass.html'
    success_url = reverse_lazy('class_list')

    def form_valid(self, form):
        form.instance.teacher = Teacher.objects.get(user=self.request.user)
        return super().form_valid(form)
    
class StudentSignUpView(CreateView):
    model = CustomUser
    form_class = StudentSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        print(1)
        return super().form_valid(form)
        
    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

class TeacherSignUpView(CreateView):
    model = CustomUser
    form_class = TeacherSignUpForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')
    def dispatch(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(*args, **kwargs)
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class UserAssignmentsView(LoginRequiredMixin, ListView):
    model = assignment
    template_name = 'assignmentlist.html'
    context_object_name = 'assignments'

    def get_queryset(self):
        user = self.request.user
        print(1)
        if user.is_teacher:
            return assignment.objects.filter(Class_room__classteacher=user.teacher)
        elif user.is_student:
            return assignment.objects.filter(submission_assignment__student=user.student)
        return assignment.objects.none()

class HomeView(TemplateView):

    def get_template_names(self):
        if self.request.user.is_authenticated:
            return ['dashboard.html']
        else:
            return ['home.html']

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        print(user.is_authenticated)
        if user.is_authenticated:
            if user.is_teacher:
                teacher = user.teacher
                classes = classroom.objects.filter(classteacher=teacher)
                assignments = assignment.objects.filter(Class_room__classteacher=teacher)
                submissions = Submission.objects.filter(assignment__Class_room__classteacher=teacher)
                context['classes'] = classes
                context['assignments'] = assignments
                context['submissions'] = submissions
            elif user.is_student:
                student = user.student
                classes = classroom.objects.filter(classstudent=student)
                assignments = assignment.objects.filter(Class_room__classstudent=student).distinct()
                submissions = Submission.objects.filter(student=student)
                context['classes'] = classes
                context['assignments'] = assignments
                context['submissions'] = submissions
            else:
                return classroom.objects.none()
        else:
            context['classes'] = classroom.objects.all()[:5]
        return context

class AssignmentDetailView(DetailView):
    model = assignment
    template_name = 'assignment_detail.html'
    context_object_name = 'assignment'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        assignment = self.get_object()

        if user.is_teacher and assignment.Class_room.classteacher == user.teacher:
            context['submissions'] = Submission.objects.filter(assignment=assignment)
        else:
            context['submissions'] = None

        return context

class ClassListView(ListView):
    model = classroom
    template_name = 'classlist.html'
    context_object_name = 'classes'

class ClassDetailView(DetailView):
    model = classroom
    template_name = 'class-details.html'
    context_object_name = 'class_detail'

    def post(self, request, *args, **kwargs):
        class_instance = get_object_or_404(classroom, pk=self.kwargs['pk'])
        user = request.user
        
        if user.is_student and user.student not in class_instance.classstudent.all():
            class_instance.classstudent.add(user.student)
        
        return HttpResponseRedirect(reverse('class_detail', args=[class_instance.pk]))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        class_instance = self.get_object()

        if user.is_teacher and class_instance.classteacher == user.teacher:
            context['assignments'] = assignment.objects.filter(Class_room=class_instance)
        elif user.is_student and user.student in class_instance.classstudent.all():
            context['assignments'] = assignment.objects.filter(Class_room=class_instance)
        else:
            context['assignments'] = None

        if user.is_student and user.student not in class_instance.classstudent.all():
            context['can_join'] = True
        else:
            context['can_join'] = False
        
        return context



class SubmissionCreateView(LoginRequiredMixin, CreateView):
    model = Submission
    form_class = SubmissionForm
    template_name = 'submission.html'

    def dispatch(self, request, *args, **kwargs):
        self.assignment = get_object_or_404(assignment, pk=self.kwargs['pk'])
        user = request.user
        
        if not user.is_student or user.student not in self.assignment.Class_room.classstudent.all():
            return redirect('home')
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.student = self.request.user.student
        form.instance.assignment = self.assignment
        return super().form_valid(form)

    def get_success_url(self):
        return self.assignment.get_absolute_url()
"""
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_teacher:
            teacher = user.teacher
            classes = classroom.objects.filter(classteacher=teacher)
            assignments = assignment.objects.filter(Class_room__classteacher=teacher)
            submissions = Submission.objects.filter(assignment__Class_room__classteacher=teacher)
            context['classes'] = classes
            context['assignments'] = assignments
            context['submissions'] = submissions

        elif user.is_student:
            student = user.student
            classes = classroom.objects.filter(classstudent=student)
            assignments = assignment.objects.filter(Class_room__classstudents=student).distinct()
            submissions = Submission.objects.filter(student=student)
            context['classes'] = classes
            context['assignments'] = assignments
            context['submissions'] = submissions

        return context
"""
class GradeUpdateView(LoginRequiredMixin, UpdateView):
    model = Submission
    form_class = GradeUpdateForm
    template_name = 'submission_edit.html'
    context_object_name = 'submission'
    success_url = reverse_lazy('dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.submission = get_object_or_404(Submission, pk=self.kwargs['pk'])
        user = request.user
        
        if not user.is_teacher or self.submission.assignment.Class_room.classteacher != user.teacher:
            raise PermissionDenied
        
        return super().dispatch(request, *args, **kwargs)

class JoinClassView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        class_instance = get_object_or_404(classroom, pk=self.kwargs['pk'])
        user = request.user
        
        if user.is_student and user.student not in class_instance.classstudent.all():
            class_instance.classstudent.add(user.student)
        
        return HttpResponseRedirect(reverse('class_detail', args=[class_instance.pk]))

class SignUpView(TemplateView):
    template_name = 'init signup.html'
    def dispatch(self, request, *args, **kwargs):

        if self.request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

from .forms import AssignmentForm

class AssignmentCreateView(LoginRequiredMixin, CreateView):
    model = assignment
    form_class = AssignmentForm
    template_name = 'assignment_form.html'
    
    def dispatch(self, request, *args, **kwargs):
        self.class_instance = get_object_or_404(classroom, pk=self.kwargs['pk'])
        user = request.user
        
        if not user.is_teacher or self.class_instance.teacher != user.teacher:
            raise PermissionDenied  # Raise PermissionDenied instead of redirecting
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.class_room = self.class_instance
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('class_detail', args=[self.class_instance.pk])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['class_instance'] = self.class_instance
        return context

class ClassStudentsView(LoginRequiredMixin, DetailView):
    model = classroom
    template_name = 'student_list.html'
    context_object_name = 'class_detail'
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        class_instance = self.get_object()

        if user.is_teacher and class_instance.teacher == user.teacher:
            context['students'] = class_instance.students.all()
        elif user.is_student and user.student in class_instance.students.all():
            context['students'] = class_instance.students.all()
        else:
            raise PermissionDenied

        return context