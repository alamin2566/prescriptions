from django.contrib import admin
from django.urls import path
from prescription import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Authentication
    path('signup/', views.SignupPage, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('logout/', views.LogoutPage, name='logout'),

    # Home
    path('', views.LoginPage, name='login'),
    path('', views.Homepage, name='home'),
    path('home/', views.Homepage, name='home'),

    # Prescription-related
    path('prescription/', views.prescription_view, name='prescription'),

    # Conditional views
    path('receipt/<int:pk>/', views.prescription_receipt, name='prescription_receipt'),
    path('list/', views.prescription_list, name='prescription_list'),
    path('header-edit/', views.header_edit_view, name='header_edit'),
    path('ajax/get-templates/', views.get_templates, name='get_templates'),

]
