from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.core.exceptions import PermissionDenied

from .models import Customer, Staff, Service, Appointment, AppointmentDetail, Payment
from .forms import (
    CustomerForm, StaffForm, ServiceForm, AppointmentForm, CustomerAppointmentForm,
    AppointmentDetailFormSet, PaymentForm, UserForm, UserRegisterForm, CustomerRegisterForm,
)


def is_staff_user(user):
    return user.is_staff


def login_view(request):
    if request.user.is_authenticated:
        return redirect('salon_app:dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('salon_app:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'salon_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('salon_app:login')


def register_view(request):
    """Public self-registration: always creates a regular CUSTOMER account
    (a User + linked Customer profile). Staff/admin accounts are created
    separately by an existing staff member via the Users screen."""
    if request.user.is_authenticated:
        return redirect('salon_app:dashboard')
    if request.method == 'POST':
        form = CustomerRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request, f"Welcome, {user.username}! Your account has been created.")
            return redirect('salon_app:dashboard')
    else:
        form = CustomerRegisterForm()
    return render(request, 'salon_app/register.html', {'form': form})


@login_required(login_url='salon_app:login')
def dashboard(request):
    if not request.user.is_staff:
        return redirect('salon_app:my_appointments')

    context = {
        'customer_count': Customer.objects.count(),
        'staff_count': Staff.objects.count(),
        'service_count': Service.objects.count(),
        'appointment_count': Appointment.objects.count(),
        'pending_count': Appointment.objects.filter(status='Pending').count(),
        'revenue': Payment.objects.aggregate(total=Sum('amount'))['total'] or 0,
        'recent_appointments': Appointment.objects.select_related('customer', 'staff').order_by('-appointment_date', '-appointment_time')[:5],
    }
    return render(request, 'salon_app/dashboard.html', context)


# ---------- CUSTOMER ----------

@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def customer_list(request):
    customers = Customer.objects.all().order_by('-created_at')
    return render(request, 'salon_app/customer_list.html', {'customers': customers})


@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def customer_form(request, pk=None):
    customer = get_object_or_404(Customer, pk=pk) if pk else None
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Customer {'updated' if pk else 'created'} successfully.")
            return redirect('salon_app:customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'salon_app/customer_form.html', {'form': form, 'customer': customer})


@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def customer_delete(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        customer.delete()
        messages.success(request, "Customer deleted.")
        return redirect('salon_app:customer_list')
    return render(request, 'salon_app/confirm_delete.html', {
        'object': customer, 'cancel_url': 'salon_app:customer_list', 'title': 'customer'
    })


# ---------- STAFF ----------

@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def staff_list(request):
    staff = Staff.objects.all().order_by('staff_name')
    return render(request, 'salon_app/staff_list.html', {'staff': staff})


@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def staff_form(request, pk=None):
    staff_obj = get_object_or_404(Staff, pk=pk) if pk else None
    if request.method == 'POST':
        form = StaffForm(request.POST, instance=staff_obj)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Staff {'updated' if pk else 'created'} successfully.")
            return redirect('salon_app:staff_list')
    else:
        form = StaffForm(instance=staff_obj)
    return render(request, 'salon_app/staff_form.html', {'form': form, 'staff': staff_obj})


@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def staff_delete(request, pk):
    staff_obj = get_object_or_404(Staff, pk=pk)
    if request.method == 'POST':
        staff_obj.delete()
        messages.success(request, "Staff member deleted.")
        return redirect('salon_app:staff_list')
    return render(request, 'salon_app/confirm_delete.html', {
        'object': staff_obj, 'cancel_url': 'salon_app:staff_list', 'title': 'staff member'
    })


# ---------- SERVICE ----------

@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def service_list(request):
    services = Service.objects.all().order_by('service_name')
    return render(request, 'salon_app/service_list.html', {'services': services})


@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def service_form(request, pk=None):
    service = get_object_or_404(Service, pk=pk) if pk else None
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Service {'updated' if pk else 'created'} successfully.")
            return redirect('salon_app:service_list')
    else:
        form = ServiceForm(instance=service)
    return render(request, 'salon_app/service_form.html', {'form': form, 'service': service})


@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.success(request, "Service deleted.")
        return redirect('salon_app:service_list')
    return render(request, 'salon_app/confirm_delete.html', {
        'object': service, 'cancel_url': 'salon_app:service_list', 'title': 'service'
    })


# ---------- APPOINTMENT ----------

@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def appointment_list(request):
    appointments = Appointment.objects.select_related('customer', 'staff').prefetch_related(
        'details__service').order_by('-appointment_date', '-appointment_time')
    return render(request, 'salon_app/appointment_list.html', {'appointments': appointments})


@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def appointment_detail(request, appointment_id):
    appointment = get_object_or_404(
        Appointment.objects.select_related(
            'customer', 'staff').prefetch_related('details__service', 'payment'),
        pk=appointment_id
    )
    return render(request, 'salon_app/appointment_detail.html', {'appointment': appointment})


@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def appointment_form(request, pk=None):
    appointment = get_object_or_404(Appointment, pk=pk) if pk else None
    if request.method == 'POST':
        form = AppointmentForm(request.POST, instance=appointment)
        formset = AppointmentDetailFormSet(request.POST, instance=appointment)
        if form.is_valid() and formset.is_valid():
            appointment = form.save()
            formset.instance = appointment
            formset.save()
            messages.success(
                request, f"Appointment {'updated' if pk else 'created'} successfully.")
            return redirect('salon_app:appointment_list')
    else:
        form = AppointmentForm(instance=appointment)
        formset = AppointmentDetailFormSet(instance=appointment)
    return render(request, 'salon_app/appointment_form.html', {
        'form': form, 'formset': formset, 'appointment': appointment
    })


@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def appointment_delete(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        appointment.delete()
        messages.success(request, "Appointment deleted.")
        return redirect('salon_app:appointment_list')
    return render(request, 'salon_app/confirm_delete.html', {
        'object': appointment, 'cancel_url': 'salon_app:appointment_list', 'title': 'appointment'
    })


# ---------- PAYMENT ----------

@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def payment_list(request):
    payments = Payment.objects.select_related(
        'appointment__customer').order_by('-payment_date')
    return render(request, 'salon_app/payment_list.html', {'payments': payments})


@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def payment_form(request, pk=None):
    payment = get_object_or_404(Payment, pk=pk) if pk else None
    if request.method == 'POST':
        form = PaymentForm(request.POST, instance=payment)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Payment {'updated' if pk else 'recorded'} successfully.")
            return redirect('salon_app:payment_list')
    else:
        form = PaymentForm(instance=payment)
    return render(request, 'salon_app/payment_form.html', {'form': form, 'payment': payment})


@login_required(login_url='salon_app:login')
@user_passes_test(is_staff_user, login_url='salon_app:dashboard')
def payment_delete(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if request.method == 'POST':
        payment.delete()
        messages.success(request, "Payment deleted.")
        return redirect('salon_app:payment_list')
    return render(request, 'salon_app/confirm_delete.html', {
        'object': payment, 'cancel_url': 'salon_app:payment_list', 'title': 'payment'
    })


# ---------- USERS (login accounts) ----------

@login_required(login_url='salon_app:login')
@user_passes_test(lambda u: u.is_staff, login_url='salon_app:dashboard')
def user_list(request):
    users = User.objects.all().order_by('username')
    return render(request, 'salon_app/user_list.html', {'users': users})


@login_required(login_url='salon_app:login')
@user_passes_test(lambda u: u.is_staff, login_url='salon_app:dashboard')
def user_form(request, pk=None):
    user_obj = get_object_or_404(User, pk=pk) if pk else None
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_obj)
        if form.is_valid():
            form.save()
            messages.success(
                request, f"User {'updated' if pk else 'created'} successfully.")
            return redirect('salon_app:user_list')
    else:
        form = UserForm(instance=user_obj)
    return render(request, 'salon_app/user_form.html', {'form': form, 'user_obj': user_obj})


@login_required(login_url='salon_app:login')
@user_passes_test(lambda u: u.is_staff, login_url='salon_app:dashboard')
def user_delete(request, pk):
    user_obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if user_obj == request.user:
            messages.error(
                request, "You can't delete your own account while logged in.")
            return redirect('salon_app:user_list')
        user_obj.delete()
        messages.success(request, "User deleted.")
        return redirect('salon_app:user_list')
    return render(request, 'salon_app/confirm_delete.html', {
        'object': user_obj, 'cancel_url': 'salon_app:user_list', 'title': 'user'
    })


# ---------- CUSTOMER SELF-SERVICE (regular, non-staff users) ----------

def _get_own_customer_or_403(request):
    """Returns the Customer profile linked to the logged-in user, or creates one
    automatically for a non-staff account if it does not yet exist.
    Staff accounts without customer profiles are still denied access.
    """
    try:
        return request.user.customer_profile
    except Customer.DoesNotExist:
        if request.user.is_staff:
            raise PermissionDenied("This account has no customer profile.")
        customer_name = request.user.get_full_name().strip() or request.user.username
        return Customer.objects.create(
            user=request.user,
            customer_name=customer_name,
            gender=None,
            phone='',
            email=request.user.email or None,
        )


@login_required(login_url='salon_app:login')
def my_appointments(request):
    """A customer's own appointment list. Staff get redirected to the admin dashboard,
    and a customer can never see anyone else's appointments here."""
    if request.user.is_staff:
        return redirect('salon_app:dashboard')
    customer = _get_own_customer_or_403(request)
    appointments = Appointment.objects.filter(customer=customer).prefetch_related(
        'details__service', 'staff', 'payment'
    ).order_by('-appointment_date', '-appointment_time')
    return render(request, 'salon_app/my_appointments.html', {'appointments': appointments})


@login_required(login_url='salon_app:login')
def my_appointment_detail(request, appointment_id):
    if request.user.is_staff:
        return redirect('salon_app:appointment_detail', appointment_id=appointment_id)
    customer = _get_own_customer_or_403(request)
    appointment = get_object_or_404(
        Appointment.objects.select_related(
            'staff').prefetch_related('details__service', 'payment'),
        pk=appointment_id, customer=customer,
    )
    return render(request, 'salon_app/my_appointment_detail.html', {'appointment': appointment})


@login_required(login_url='salon_app:login')
def book_appointment(request, pk=None):
    """A customer books (or edits, while still Pending) their own appointment.
    The customer field is always forced to their own profile, and the status
    is always reset to 'Pending' here — never settable by the customer."""
    if request.user.is_staff:
        return redirect('salon_app:appointment_list')
    customer = _get_own_customer_or_403(request)

    appointment = None
    if pk:
        appointment = get_object_or_404(Appointment, pk=pk, customer=customer)
        if appointment.status != 'Pending':
            messages.error(
                request, "This appointment can no longer be changed.")
            return redirect('salon_app:my_appointment_detail', appointment_id=appointment.appointment_id)

    if request.method == 'POST':
        form = CustomerAppointmentForm(request.POST, instance=appointment)
        formset = AppointmentDetailFormSet(request.POST, instance=appointment)
        if form.is_valid() and formset.is_valid():
            appointment = form.save(commit=False)
            appointment.customer = customer
            appointment.status = 'Pending'
            appointment.save()
            formset.instance = appointment
            formset.save()
            messages.success(
                request, f"Appointment {'updated' if pk else 'booked'} successfully.")
            return redirect('salon_app:my_appointments')
    else:
        form = CustomerAppointmentForm(instance=appointment)
        formset = AppointmentDetailFormSet(instance=appointment)

    return render(request, 'salon_app/book_appointment.html', {
        'form': form, 'formset': formset, 'appointment': appointment
    })


@login_required(login_url='salon_app:login')
def my_appointment_cancel(request, pk):
    if request.user.is_staff:
        return redirect('salon_app:appointment_list')
    customer = _get_own_customer_or_403(request)
    appointment = get_object_or_404(Appointment, pk=pk, customer=customer)
    if request.method == 'POST':
        if appointment.status in ('Pending', 'Confirmed'):
            appointment.status = 'Cancelled'
            appointment.save()
            messages.success(request, "Appointment cancelled.")
        else:
            messages.error(request, "This appointment can't be cancelled.")
        return redirect('salon_app:my_appointments')
    return render(request, 'salon_app/confirm_delete.html', {
        'object': appointment, 'cancel_url': 'salon_app:my_appointments', 'title': 'appointment booking'
    })
