from django.urls import path
from . import views

urlpatterns = [
    path('', views.internship_list, name='internship_list'),
    path('<int:id>/', views.internship_detail, name='internship_detail'),
    path('my_applications/', views.my_applications, name='my_applications'),
    path('<int:id>/apply/', views.apply_internship, name='apply_internship'),
    path('applications/<int:id>/withdraw/', views.withdraw_application, name='withdraw_application'),
]