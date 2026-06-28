from django.conf import settings
from django.db import models


class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='customer_profile', null=True, blank=True,
        help_text="The login account that owns this customer profile (self-registered customers)."
    )
    customer_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=15, blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Customer'

    def __str__(self):
        return self.customer_name


class Staff(models.Model):
    staff_id = models.AutoField(primary_key=True)
    staff_name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'Staff'

    def __str__(self):
        return self.staff_name


class Service(models.Model):
    service_id = models.AutoField(primary_key=True)
    service_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(help_text='Duration in minutes')

    class Meta:
        db_table = 'Service'

    def __str__(self):
        return self.service_name


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    appointment_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
        db_column='customer_id', related_name='appointments'
    )
    staff = models.ForeignKey(
        Staff, on_delete=models.CASCADE,
        db_column='staff_id', related_name='appointments'
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    class Meta:
        db_table = 'Appointment'

    def __str__(self):
        return f"Appointment #{self.appointment_id} - {self.customer.customer_name}"


class AppointmentDetail(models.Model):
    detail_id = models.AutoField(primary_key=True)
    appointment = models.ForeignKey(
        Appointment, on_delete=models.CASCADE,
        db_column='appointment_id', related_name='details'
    )
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE,
        db_column='service_id', related_name='appointment_details'
    )

    class Meta:
        db_table = 'Appointment_Detail'

    def __str__(self):
        return f"Detail #{self.detail_id} - {self.service.service_name}"


class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Cash', 'Cash'),
        ('Credit Card', 'Credit Card'),
        ('ABA', 'ABA'),
        ('KHQR', 'KHQR'),
    ]

    payment_id = models.AutoField(primary_key=True)
    appointment = models.OneToOneField(
        Appointment, on_delete=models.CASCADE,
        db_column='appointment_id', related_name='payment'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES, blank=True, null=True)
    payment_date = models.DateField()

    class Meta:
        db_table = 'Payment'

    def __str__(self):
        return f"Payment #{self.payment_id} - {self.amount}"
