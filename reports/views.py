from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from twilio.rest import Client
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .models import Goal, Activity
from .forms import AppointmentForm
from twilio.rest import Client
from .models import Appointment, DoctorSchedule
from django.contrib import messages
from .forms import UserUpdateForm, GoalUpdateForm, ActivityForm, DoctorScheduleForm
from .models import Product




def home(request):
    data={
        'title':'Home Page',
    }
    return render(request,'home.html',context = data)

def services(request):
    data={
        'title':'Services Page',
    }
    return render(request,'services.html',context = data)
@login_required
def docters(request):
    data={
        'title':'Docters Page',
    }
    return render(request,'docters.html',context = data)
@login_required
def healthLibrary(request):
    data={
        'title':'Health Library',
    }
    return render(request,'healthLibrary.html',context = data)
@login_required
def about(request):
    data={
        'title':'About Page',
    }
    return render(request,'about.html',context = data)


def appoinment(request):
    data={
        'title':'Appoinment Page',
    }
    return render(request,'appoinment.html',context = data)
@login_required
def healthcheckup(request):
    data={
        'title':'Health Chekup Page',
    }
    return render(request,'healthcheckup.html',context = data)
@login_required
def wellnesscart(request):
    data={
        'title':'WellnessCart Page',
    }
    return render(request,'wellnesscart.html',context = data)


def dashboard(request):
    stats = Goal.objects.get_or_create(user=request.user)[0]  # ✅ lowercase 'user'
    thresholds = {
        'total_workout': 10,
        'calories_burned': 1000,
        'duration_hrs': 7,
        'streak_days': 5,
    }
    recent_activities = Activity.objects.filter(user=request.user).order_by('-date')  # ✅ lowercase 'user'
    data = {
        'title': 'Health Dashboard Page',
        'stats': stats,
        'thresholds': thresholds,
        'recent_activities': recent_activities,
    }
    return render(request, 'dashboard.html', context=data)

from .forms import ActivityForm
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            messages.success(request, 'Activity Added Successfully')
            return redirect('dashboard')
    else:
        form = ActivityForm()

    data = {
        'title': 'Add Activity',
        'Page_title': 'Log New Activity',
        'form': form
    }
    return render(request, 'add_activity.html', context=data)

def edit_activity(request,activity_id):
    activity = get_object_or_404(Activity, id=activity_id, user=request.user)
    if request.method == 'POST':
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request,'Activity Updated Sucessfully')
            return redirect('dashboard')
    else:
        form =ActivityForm(instance=activity)
    data={
        'title':'edit activity',
        'page_title':'Edit Activity',
        'form':form
    }
    return render(request,'add_activity.html', context=data)

def delete_activity(request, activity_id):
    activity = Activity.objects.get(id=activity_id, user=request.user)  # Ensure the activity belongs to the logged-in user

    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activity  deleted successfully!')
        return redirect('dashboard')




def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)

    context = {
        'title': 'Profile',
        'user_form': user_form,
    }
    return render(request, 'profile.html', context)



def goal_update(request):
    goal, created = Goal.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        goal_form = GoalUpdateForm(request.POST, instance=goal)
        if goal_form.is_valid():
            goal_form.save()
            messages.success(request, 'Your workout goals have been updated!')
            return redirect('goal_update')
    else:
        goal_form = GoalUpdateForm(instance=goal)

    context = {
        'title': 'Update Goals',
        'goal_form': goal_form,
    }
    return render(request, 'goal_update.html', context)

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration Successful')
            return redirect('home')
            
            
            #  # ✅ Send SMS using Twilio
            # mobile_number = form.cleaned_data.get('mobile')
            # client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            # message = client.messages.create(
            #     body=f"Hello {user.username}, your login was successful!",
            #     from_=settings.TWILIO_PHONE_NUMBER,
            #     to=f"+91{mobile_number}"  # India country code
            # )
            # return redirect('home')  # after registration, go to home page
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# views.py
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from twilio.rest import Client

from .models import Appointment
from .forms import AppointmentForm


@login_required
def book_appointment(request):
    if request.method == "POST":
        form = AppointmentForm(request.POST)

        if form.is_valid():
            # Appointment-ai first save pannama,
            # current login user-ai assign pannuvom
            appointment = form.save(commit=False)
            appointment.user = request.user
            appointment.save()

            # Twilio credentials environment variables-la irukkanum
            account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
            auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
            twilio_number = os.environ.get("TWILIO_PHONE_NUMBER")

            # SMS configuration irundhaal mattum send pannuvom
            if account_sid and auth_token and twilio_number:
                try:
                    client = Client(account_sid, auth_token)

                    client.messages.create(
                        body=(
                            f"Hi {appointment.name}, your appointment "
                            f"on {appointment.date} is confirmed!"
                        ),
                        from_=twilio_number,
                        to=f"+91{appointment.phone}"
                    )
                except Exception:
                    # SMS fail aanaalum appointment save aagiyirukkum
                    pass

            return redirect("view_appointments")

    else:
        form = AppointmentForm()

    return render(
        request,
        "appointment_form.html",
        {"form": form}
    )


@login_required
def view_appointments(request):
    appointments = Appointment.objects.filter(
        user=request.user
    ).order_by("-date", "-time")

    return render(
        request,
        "appointments.html",
        {"appointments": appointments}
    )



@login_required
def appointment_details(request, id):
    appointment = get_object_or_404(
        Appointment,
        pk=id,
        user=request.user
    )

    return render(
        request,
        "appointment_detail.html",
        {"appointment": appointment}
    )


@login_required
def assign_doctor(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    schedule_instance = getattr(appointment, 'schedule', None)

    if request.method == "POST":
        form = DoctorScheduleForm(request.POST, instance=schedule_instance)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.appointment = appointment
            # Auto-fill customer_mobile from appointment if blank
            if not schedule.customer_mobile and appointment.phone:
                schedule.customer_mobile = appointment.phone
            schedule.save()

            # Send SMS when status is Scheduled
            if schedule.status == 'Scheduled':
                success, result = schedule.send_schedule_sms()
                if success:
                    messages.success(
                        request,
                        f"Doctor scheduled successfully! Confirmation SMS sent to {schedule.customer_mobile}."
                    )
                else:
                    messages.warning(
                        request,
                        f"Doctor scheduled, but SMS could not be sent: {result}"
                    )
            else:
                messages.success(request, "Doctor schedule saved successfully.")

            return redirect("view_appointments")
    else:
        initial_data = {}
        if not schedule_instance:
            initial_data = {
                'customer_mobile': appointment.phone,
                'department': appointment.department,
            }
        form = DoctorScheduleForm(instance=schedule_instance, initial=initial_data)

    return render(request, "assign_doctor.html", {
        "form": form,
        "appointment": appointment,
        "schedule": schedule_instance,
    })




# Product Model create
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products.html', {'products': products})

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'product_detail.html', {'product': product})


# Special Doctor Appoinments methods
from .models import Doctor, DoctorBooking

def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})


def create_booking(request, doc_id):
    doctor = get_object_or_404(Doctor, id=doc_id)
    if request.method == 'POST':
        patient_fullname = request.POST.get('patient_fullname')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')

        booking = DoctorBooking(
            doctor_ref=doctor,
            patient_fullname=patient_fullname,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        )

        if booking.is_slot_open():
            booking.save()
            messages.success(request, 'Appointment booked successfully!')
            return redirect('view_doctor_bookings', doc_id=doctor.id)
        else:
            messages.error(request, 'This slot is already taken!')
    return render(request, 'book_appointment.html', {'doctor': doctor})

def view_doctor_bookings(request, doc_id):
    doctor = Doctor.objects.get(id=doc_id)
    appointments = DoctorBooking.objects.filter(doctor_ref=doctor)
    return render(request, 'appointments_list.html', {'appointments': appointments, 'doctor': doctor})

def appointment_detail(request, appointment_id):
    appointment = DoctorBooking.objects.select_related('doctor_ref').get(id=appointment_id)
    return render(request, 'appointment_detailD.html', {'appointment': appointment})






#Create a Model for Health Checkup
def calculate_health_status(blood_sugar, blood_pressure, cholesterol):
    if blood_sugar < 100 and cholesterol < 200 and blood_pressure == "120/80":
        return "Healthy"
    else:
        return "Needs Attention"

# views.py
from .models import HealthCheckup
def health_checkup_detail(request, pk):
    checkup = get_object_or_404(HealthCheckup, pk=pk)
    return render(request, 'admin/health_checkup_detail.html', {'checkup': checkup})

# ==========================================
# AI Chatbot Views
# ==========================================
import json
from django.http import JsonResponse
from .models import ChatSession, Message
from .forms import ChatForm
from .utils import generate_response

def ai_chat(request):
    """
    Lightweight API endpoint for querying the healthcare AI directly.
    """
    question = request.GET.get("question") or request.POST.get("question")
    if not question:
        return JsonResponse({"answer": "Please ask a health question."})

    answer = generate_response(question, [])
    return JsonResponse({"answer": answer})


def new_chat(request):
    """
    Creates a new chat session and redirects to the conversation interface.
    """
    session = ChatSession.objects.create()
    return redirect('chat_view', id=str(session.id))


def chat_view(request, id):
    """
    Main interactive AI Healthcare Chat view.
    Handles both AJAX/Fetch requests for smooth live messaging and standard HTML form POSTs.
    """
    session = get_object_or_404(ChatSession, id=id)

    if request.method == "POST":
        is_ajax = (
            request.headers.get('x-requested-with') == 'XMLHttpRequest' or
            'application/json' in request.content_type
        )

        user_input = ""
        if 'application/json' in request.content_type:
            try:
                body = json.loads(request.body.decode('utf-8'))
                user_input = body.get("user_input", "").strip()
            except Exception:
                user_input = ""
        else:
            form = ChatForm(request.POST)
            if form.is_valid():
                user_input = form.cleaned_data["user_input"].strip()

        if user_input:
            recent_messages = list(session.messages.order_by("-created")[:5])[::-1]
            ai_response = generate_response(user_input, recent_messages)

            user_msg = Message.objects.create(
                session=session,
                sender="human",
                text=user_input
            )

            ai_msg = Message.objects.create(
                session=session,
                sender="ai",
                text=ai_response
            )

            if is_ajax:
                return JsonResponse({
                    "status": "success",
                    "user_message": user_msg.text,
                    "user_time": user_msg.created.strftime("%H:%M"),
                    "ai_response": ai_msg.text,
                    "ai_time": ai_msg.created.strftime("%H:%M"),
                })

            return redirect("chat_view", id=session.id)

        if is_ajax:
            return JsonResponse({"status": "error", "message": "Empty message"}, status=400)

    form = ChatForm()
    chat_history = session.messages.order_by("created")
    recent_sessions = ChatSession.objects.order_by("-created")[:12]

    return render(
        request,
        "chat.html",
        {
            "session": session,
            "form": form,
            "chat_history": chat_history,
            "recent_sessions": recent_sessions,
            "title": "AI Healthcare Assistant",
        }
    )



# Create a Add to Cart Model
from .models import Cart
from .models import Product

def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_view')


def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart_item.delete()
    return redirect('cart_view')

# final order summary Buy methods
from .models import Order
from decimal import Decimal          
def buy_now(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    discount_rate = Decimal('0.12')
    total_price = product.price - (product.price * discount_rate)  # example discount
    order = Order.objects.create(
        user=request.user,
        product=product,
        total_price=total_price,
        address="User’s saved address",
        phone="User’s saved phone"
    )
    return redirect('order_summary', order_id=order.id)

def order_summary(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_summary.html', {'order': order})

# Payment Integration methods
def payment_page(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'payment.html', {'order': order})



def place_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    payment_method = request.POST.get('payment_method')

    if payment_method == 'upi':
        order.payment_status = 'Paid via UPI'
    elif payment_method == 'cod':
        order.payment_status = 'Cash on Delivery'
    else:
        order.payment_status = 'Pending'

    order.save()
    return redirect('order_success', order_id=order.id)

# reports/views.py
from django.shortcuts import render, get_object_or_404
from .models import Order

def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_success.html', {'order': order})

# final order summary Buy methods
from django.shortcuts import render
from django.db.models import Sum
from .models import Order

def admin_dashboard(request):
    # Aggregate product sales
    product_sales = (
        Order.objects.values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')
    )

    # Prepare data for chart
    labels = [item['product__name'] for item in product_sales]
    data = [item['total_sold'] for item in product_sales]

    context = {
        'labels': labels,
        'data': data,
    }
    return render(request, 'admin/dashboard.html', context)

from django.shortcuts import render
from django.db.models import Sum
from .models import Order

def sales_chart_view(request):
    # Aggregate product sales
    product_sales = (
        Order.objects.values('product__name')
        .annotate(total_sold=Sum('quantity'))
        .order_by('-total_sold')
    )

    labels = [item['product__name'] for item in product_sales]
    data = [item['total_sold'] for item in product_sales]

    context = {
        'labels': labels,
        'data': data,
        'title': 'Product Sales Chart'
    }
    return render(request, 'admin/sales_chart.html', context)


from .forms import CustomUserCreationForm
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration Sucessful')
            return redirect ('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})