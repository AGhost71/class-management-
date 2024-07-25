from django.contrib import admin
from django.urls import path,include
from .views import HomeView,StudentSignUpView,TeacherSignUpView,AssignmentDetailView,UserAssignmentsView,CustomLoginView,ClassListView,ClassDetailView,SubmissionCreateView,GradeUpdateView,JoinClassView,SignUpView,ClassCreateView

urlpatterns = [
    path('home/',HomeView.as_view(),name='home'),
    path('student_signup/', StudentSignUpView.as_view(), name='student_signup'),
    path('teacher_signup/', TeacherSignUpView.as_view(), name='teacher_signup'),
    path('assignment/<int:pk>/', AssignmentDetailView.as_view(), name='assignment_detail'),
    path('assignments/', UserAssignmentsView.as_view(), name='user_assignments'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('class_list/', ClassListView.as_view(), name='class_list'),
    path('class/<int:pk>/', ClassDetailView.as_view(), name='class_detail'),
    path('create_submission/<int:pk>/', SubmissionCreateView.as_view(), name='create_submission'),
#   path('dashboard/',DashboardView.as_view(), name='dashboard'),
    path('update_grade/<int:pk>/', GradeUpdateView.as_view(), name='update_grade'),
    path('join_class/<int:pk>/', JoinClassView.as_view(), name='join_class'),
    path('signup/',SignUpView.as_view(),name='signup'),
    path('craete_class/',ClassCreateView.as_view(),name='create_class'),
    path('class/<int:pk>/students/', ClassDetailView.as_view(), name='student_list'),
]
