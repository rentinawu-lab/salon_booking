from django.urls import path
from . import views

app_name = 'salon_app'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),

    path('', views.dashboard, name='dashboard'),

    # Users
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_form, name='user_add'),
    path('users/<int:pk>/edit/', views.user_form, name='user_edit'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Customers
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_form, name='customer_add'),
    path('customers/<int:pk>/edit/', views.customer_form, name='customer_edit'),
    path('customers/<int:pk>/delete/', views.customer_delete, name='customer_delete'),

    # Staff
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/add/', views.staff_form, name='staff_add'),
    path('staff/<int:pk>/edit/', views.staff_form, name='staff_edit'),
    path('staff/<int:pk>/delete/', views.staff_delete, name='staff_delete'),

    # Services
    path('services/', views.service_list, name='service_list'),
    path('services/add/', views.service_form, name='service_add'),
    path('services/<int:pk>/edit/', views.service_form, name='service_edit'),
    path('services/<int:pk>/delete/', views.service_delete, name='service_delete'),

    # Appointments
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/add/', views.appointment_form, name='appointment_add'),
    path('appointments/<int:appointment_id>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/<int:pk>/edit/', views.appointment_form, name='appointment_edit'),
    path('appointments/<int:pk>/delete/', views.appointment_delete, name='appointment_delete'),

    # Payments
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.payment_form, name='payment_add'),
    path('payments/<int:pk>/edit/', views.payment_form, name='payment_edit'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),

    # Customer self-service (regular, non-staff users)
    path('my-appointments/', views.my_appointments, name='my_appointments'),
    path('my-appointments/book/', views.book_appointment, name='book_appointment'),
    path('my-appointments/<int:appointment_id>/', views.my_appointment_detail, name='my_appointment_detail'),
    path('my-appointments/<int:pk>/edit/', views.book_appointment, name='my_appointment_edit'),
    path('my-appointments/<int:pk>/cancel/', views.my_appointment_cancel, name='my_appointment_cancel'),
]
