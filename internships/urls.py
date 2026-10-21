from django.urls import path
from . import views

urlpatterns = [
    path('company/register/', views.company_register, name='company_register'),
    path('company/dashboard/', views.company_dashboard, name='company_dashboard'),
    path('company/post-internship/', views.company_post_internship, name='company_post_internship'),
    path('company/internship/<int:id>/edit/', views.company_edit_internship, name='company_edit_internship'),
    path('company/internship/<int:id>/delete/', views.company_delete_internship, name='company_delete_internship'),
    path('company/profile/edit/', views.company_profile_edit, name='company_profile_edit'),
    path('company/internship/<int:id>/applicants/', views.company_view_applicants, name='company_view_applicants'),
    path('company/application/<int:id>/update-status/', views.company_update_application_status, name='company_update_application_status'),
    path('', views.internship_list, name='internship_list'),
    path('my_applications/', views.my_applications, name='my_applications'),
    path('<int:id>/', views.internship_detail, name='internship_detail'),
    path('<int:id>/apply/', views.apply_internship, name='apply_internship'),
    path('applications/<int:id>/withdraw/', views.withdraw_application, name='withdraw_application'),
]