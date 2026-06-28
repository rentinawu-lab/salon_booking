from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import (
    Customer, Staff, Service, Appointment, AppointmentDetail, Payment
)


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomerRegisterForm(UserCreationForm):
    """Registration form for a customer signing up on the public site.
    Creates a Django User (login account) plus its linked Customer profile."""
    email = forms.EmailField(required=False)
    customer_name = forms.CharField(max_length=100, label="Full name")
    gender = forms.ChoiceField(
        choices=[('', '---'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')],
        required=False,
    )
    phone = forms.CharField(max_length=15)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data.get('email', '')
        if commit:
            user.save()
            Customer.objects.create(
                user=user,
                customer_name=self.cleaned_data['customer_name'],
                gender=self.cleaned_data.get('gender') or None,
                phone=self.cleaned_data['phone'],
                email=self.cleaned_data.get('email') or None,
            )
        return user


class UserForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput, required=False,
        help_text="Leave blank to keep the current password when editing."
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']
        widgets = {
            'is_staff': forms.CheckboxInput(),
            'is_active': forms.CheckboxInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)
        elif not user.pk:
            # New user with no password supplied: set an unusable one
            user.set_unusable_password()
        if commit:
            user.save()
        return user


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['customer_name', 'gender', 'phone', 'email']
        widgets = {
            'gender': forms.Select(choices=[('', '---'), ('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
        }


class StaffForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ['staff_name', 'position', 'phone', 'email']


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_name', 'price', 'duration']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['customer', 'staff', 'appointment_date', 'appointment_time', 'status']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class CustomerAppointmentForm(forms.ModelForm):
    """Self-service booking form for a logged-in customer.
    No 'customer' or 'status' fields — those are set automatically by the view,
    so a customer can never book on someone else's behalf or set their own status."""
    class Meta:
        model = Appointment
        fields = ['staff', 'appointment_date', 'appointment_time']
        widgets = {
            'appointment_date': forms.DateInput(attrs={'type': 'date'}),
            'appointment_time': forms.TimeInput(attrs={'type': 'time'}),
        }


class AppointmentDetailForm(forms.ModelForm):
    class Meta:
        model = AppointmentDetail
        fields = ['service']


AppointmentDetailFormSet = inlineformset_factory(
    Appointment,
    AppointmentDetail,
    form=AppointmentDetailForm,
    extra=1,
    can_delete=True,
)


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['appointment', 'amount', 'payment_method', 'payment_date']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date'}),
        }
