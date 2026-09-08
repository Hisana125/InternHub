from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.student_register, name='student_register'),
    path('success/', views.student_success, name='student_success'),

    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),

    # Student Profile Management
    path('profile/', views.student_profile, name='student_profile_self'),
    path('profile/edit/', views.student_edit, name='student_edit_self'),
    path('students/', views.student_list, name='student_list'),
    path('students/<int:id>/', views.student_profile, name='student_profile'),
    path('students/edit/<int:id>/', views.student_edit, name='student_edit'),
    path('students/delete/<int:id>/', views.student_delete, name='student_delete'),

    # Notifications
    path('notifications/', views.student_notifications, name='student_notifications'),
    path('notifications/<int:id>/read/', views.mark_notification_read, name='mark_notification_read'),
    path('notifications/read-all/', views.mark_all_notifications_read, name='mark_all_notifications_read'),
    path('notifications/<int:id>/delete/', views.delete_notification, name='delete_notification'),
]