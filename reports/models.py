from django.db import models
from django.contrib.auth.models import User

class Goal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_workout = models.IntegerField(default=0)
    calories_burned = models.IntegerField(default=0)
    duration_hrs = models.FloatField(default=0.0)
    streak_days = models.IntegerField(default=0)

    def __str__(self):
        return f"Goal for {self.user.username}"


class Activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    exercise = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)
    calories = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.exercise} on {self.date} for {self.user.username}"


    

# models.py

from django.db import models
from django.contrib.auth.models import User


class Appointment(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="appointments",null=True,blank=True)
    name = models.CharField(max_length=100)
    date = models.DateField()
    phone = models.CharField(max_length=15)
    department = models.CharField(max_length=50)
    email = models.EmailField()
    gender = models.CharField(max_length=10)
    symptoms = models.TextField()
    time = models.TimeField()

    def __str__(self):
        return f"{self.name} - {self.date} ({self.department})"

    
    # Product Model create
class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')  # image upload path
    category = models.CharField(max_length=50)
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
# Special Doctor Appoinments methods  
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.CharField(max_length=50)
    hospital = models.CharField(max_length=150)
    image = models.ImageField(upload_to='doctors/')
    
    def __str__(self):
        return self.name
    
    def get_full_info(self):
        return f"{self.name} - {self.specialization} ({self.experience})"
    
class DoctorBooking(models.Model):
    doctor_ref = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    patient_fullname = models.CharField(max_length=120, null=True, blank=True)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    created_on = models.DateTimeField(auto_now_add=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.patient_fullname} → {self.doctor_ref.name}"

    def is_slot_open(self):
        existing = DoctorBooking.objects.filter(
            doctor_ref=self.doctor_ref,
            appointment_date=self.appointment_date,
            appointment_time=self.appointment_time
        )
        return not existing.exists()



#Create a Model for Health Checkup
from django.db import models
from django.contrib.auth.models import User

class HealthCheckup(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    blood_sugar = models.DecimalField(max_digits=5, decimal_places=2)
    blood_pressure = models.CharField(max_length=10)
    cholesterol = models.DecimalField(max_digits=5, decimal_places=2)
    checked_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.username} - {self.checked_on.strftime('%Y-%m-%d')}"

###AI chatbot method integrate
# models.py
from django.db import models
from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question[:30]}"
    
#Doctor scheduling admin page
class DoctorSchedule(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="schedule")
    doctor_name = models.CharField(max_length=100)
    customer_mobile = models.CharField(max_length=15,blank=True,default='',verbose_name="Customer mobile number")
    department = models.CharField(max_length=50)
    floor_number = models.CharField(max_length=10)
    schedule_date = models.DateField()
    schedule_time = models.TimeField()
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Scheduled', 'Scheduled')],
        default='Scheduled'
    )

    def save(self, *args, **kwargs):
        # Auto-fill customer_mobile from appointment if blank
        if not self.customer_mobile and self.appointment and getattr(self.appointment, 'phone', None):
            self.customer_mobile = self.appointment.phone
        super().save(*args, **kwargs)

    def send_schedule_sms(self):
        """
        Sends appointment scheduling confirmation SMS via Twilio to the patient.
        Returns: (success: bool, detail: str)
        """
        from .utils import send_doctor_schedule_sms
        return send_doctor_schedule_sms(self)

    def __str__(self):
        return f"Dr. {self.doctor_name} - {self.schedule_date} {self.schedule_time}"

    
    
#AI Chatbot methods
import uuid

class ChatSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    
    def get_preview(self):
        first_msg = self.messages.filter(sender='human').first()
        if first_msg:
            return (first_msg.text[:35] + '...') if len(first_msg.text) > 35 else first_msg.text
        return f"Chat on {self.created.strftime('%b %d, %H:%M')}"

    def __str__(self):
        return f"Session {str(self.id)[:8]} ({self.created.strftime('%Y-%m-%d %H:%M')})"
    
class Message(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        preview =(self.text[:30] + '...') if len(self.text) >30 else self.text
        return f"{self.sender.capitalize()} @ {self.created.strftime('%Y-%m-%d %H:%M:%S')}:{preview}"



# Create a Add to Cart Model
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    
# final order summary Buy methods
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    phone = models.CharField(max_length=15)
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.product.name}"




