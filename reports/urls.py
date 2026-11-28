from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import CustomAuthenticationForm

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name="home"),
    path('services/', views.services, name="services"),
    path('docters/', views.docters, name="docters"),
    path('healthLibrary/', views.healthLibrary, name="healthLibrary"),
    path('about/', views.about, name="about"),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(form_class=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('healthcheckup/', views.healthcheckup, name="healthcheckup"),
    path('wellnesscart/', views.wellnesscart, name="wellnesscart"),
    path('dashboard/', views.dashboard, name="dashboard"),
    
    path("book/", views.book_appointment, name="book_appointment"),
    path("appointments/", views.view_appointments, name="view_appointments"),
    path("appointments/<int:id>/", views.appointment_details, name="appointment_detail"),
    path("appointments/<int:appointment_id>/assign/", views.assign_doctor, name="assign_doctor"),

    path("profile/", views.profile, name="profile"),
    path("goal_update/", views.goal_update, name='goal_update'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:id>/', views.product_detail, name='product_detail'),
    # Special Doctor Appointments methods
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('book/<int:doc_id>/', views.create_booking, name='create_booking'),
    path('bookings/<int:doc_id>/', views.view_doctor_bookings, name='view_doctor_bookings'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detailD'),

    # Health checkup detail in admin/reports
    path('admin/reports/healthcheckup/<int:pk>/', views.health_checkup_detail, name='reports_healthcheckup_detail'),
    
    path("ai_chat", views.ai_chat, name="ai_chat"),
    path("ai_chat/", views.ai_chat, name="ai_chat_slash"),
    # Activity methods
    path("activity/", views.add_activity, name="add_activity"),
    path('activity/<int:activity_id>/', views.edit_activity, name='edit_activity'),
    path("delete_activity/<int:activity_id>/", views.delete_activity, name="delete_activity"),
    
    # AI Chatbot methods
    path('new/', views.new_chat, name='new_chat'),
    path('chat/<str:id>/', views.chat_view, name='chat_view'),
    
    # Cart Model
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    # Buy & Order methods
    path('buy/<int:product_id>/', views.buy_now, name='buy_now'),
    path('order/<int:order_id>/', views.order_summary, name='order_summary'),
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('place_order/<int:order_id>/', views.place_order, name='place_order'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    
    # Admin dashboard & Analytics
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('sales-chart/', views.sales_chart_view, name='sales_chart'),
    path(
    'my-appointments/',
    views.my_appointments,
    name='my_appointments'
),
    path(
    'book/<int:doc_id>/',
    views.create_booking,
    name='create_booking'
),
]
