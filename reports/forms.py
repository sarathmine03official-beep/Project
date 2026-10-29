from django import forms
from django.contrib.auth.models import User
from .models import Appointment
from .models import Goal

from django import forms
from django.contrib.auth.models import User
from .models import Goal, Activity
from .models import HealthCheckup

class UserUpdateForm(forms.ModelForm):
    phone_number = forms.CharField(
        max_length=15,
        required=False
    )

    address = forms.CharField(
        widget=forms.Textarea,
        required=False
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        



from django import forms
from django.contrib.auth.models import User

class GoalUpdateForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['total_workout', 'calories_burned', 'duration_hrs', 'streak_days']
        labels = {
            'total_workout': 'Workouts',
            'calories_burned': 'Calories Burned',
            'duration_hrs': 'Hours',
            'streak_days': 'Days',
        }


# forms.py

from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = [
            "name",
            "date",
            "phone",
            "department",
            "email",
            "gender",
            "symptoms",
            "time",
        ]

        
class ActivityForm (forms.ModelForm):
    class Meta:
        model = Activity
        fields=['exercise','duration','calories']
        labels={
            'exercise':'Exercise Name',
            'duration':'Duration Minutes',
            'calories':'Calories Burned',
        }
        
#Create a Model for Health Checkup     
class HealthCheckupForm(forms.ModelForm):
    class Meta:
        model = HealthCheckup
        fields = ['patient', 'blood_sugar', 'blood_pressure', 'cholesterol']
        widgets = {
            'blood_sugar': forms.NumberInput(attrs={'placeholder': 'Enter mg/dL'}),
            'blood_pressure': forms.TextInput(attrs={'placeholder': 'e.g. 120/80'}),
            'cholesterol': forms.NumberInput(attrs={'placeholder': 'Enter mg/dL'}),
        }
        

#Doctor scheduling admin page
from .models import DoctorSchedule

class DoctorScheduleForm(forms.ModelForm):
    class Meta:
        model = DoctorSchedule
        fields = [
            'doctor_name',
            'customer_mobile',
            'department',
            'floor_number',
            'schedule_date',
            'schedule_time',
            'status',
        ]
        widgets = {
            'schedule_date': forms.DateInput(attrs={'type': 'date'}),
            'schedule_time': forms.TimeInput(attrs={'type': 'time'}),
            'customer_mobile': forms.TextInput(attrs={'placeholder': 'Patient 10-digit mobile number'}),
        }

        
# AI Chatbot methods
class ChatForm(forms.Form):
    user_input = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Type your health question, symptoms, or concerns...',
            'class': 'flex-grow w-full px-4 py-3 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent text-gray-800 placeholder-gray-400 text-sm shadow-sm transition',
            'id': 'chat-input',
            'autocomplete': 'off'
        })
    )

# custom authentication Login and Register
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.safestring import mark_safe 

# Create the Custom Icon form
class CustomPasswordInput(forms.PasswordInput):
    def render(self, name, value, attrs=None, renderer=None):
        # Render the normal Django input field first
        input_html = super().render(name, value, attrs, renderer)
        
        # Define the Tailwind SVG toggle button
        toggle_html = """
        <button type="button" onclick="togglePassword(this)" class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-blue-600 transition focus:outline-none" title="Toggle password visibility">
            <svg class="h-5 w-5 eye-open" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
            </svg>
            <svg class="h-5 w-5 eye-closed hidden" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21" />
            </svg>
        </button>
        """
        
        # Wrap them both in a relative container so the absolute button sits inside the input
        final_html = f'<div class="relative w-full">{input_html}{toggle_html}</div>'
        
        # mark_safe tells Django this HTML is safe to render on the page
        return mark_safe(final_html)

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 mt-1','placeholder': 'Enter your username'}),label='Profile Name')
    email = forms.EmailField(required=True,widget=forms.EmailInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 mt-1','placeholder': 'Enter your email'}),label='Email')
    password1 = forms.CharField(widget=CustomPasswordInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 mt-1','placeholder': 'Enter password'}),label='Password')
    password2 = forms.CharField(widget=CustomPasswordInput(attrs={'class': 'w-full border border-gray-300 rounded-lg px-4 py-2 mt-1','placeholder': 'Confirm password'}),label='Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Tailwind classes to username and password fields
        for field_name, field in self.fields.items():
            base_classes = 'w-full border border-gray-300 rounded-lg px-4 py-2 mt-1 ''focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500'
             
            if 'password' in field_name.lower():
                field.widget = CustomPasswordInput(attrs={'class':f'{base_classes}pr-10'})
            else:
                field.widget.attrs.update({'class':base_classes})


        



