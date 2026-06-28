from django.contrib import admin
from .models import Customer, Staff, Service, Appointment, AppointmentDetail, Payment


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'customer_name', 'gender', 'phone', 'email', 'created_at')
    search_fields = ('customer_name', 'phone', 'email')


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('staff_id', 'staff_name', 'position', 'phone', 'email')
    search_fields = ('staff_name', 'position')


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_id', 'service_name', 'price', 'duration')
    search_fields = ('service_name',)


class AppointmentDetailInline(admin.TabularInline):
    model = AppointmentDetail
    extra = 1


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('appointment_id', 'customer', 'staff', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('customer__customer_name', 'staff__staff_name')
    inlines = [AppointmentDetailInline]


@admin.register(AppointmentDetail)
class AppointmentDetailAdmin(admin.ModelAdmin):
    list_display = ('detail_id', 'appointment', 'service')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'appointment', 'amount', 'payment_method', 'payment_date')
    list_filter = ('payment_method', 'payment_date')
