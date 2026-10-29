from django.urls import path
from .import views
from django.contrib.auth import views as auth_views
from .forms import CustomUserCreationForm, CustomAuthenticationForm



urlpatterns = [
    path('', views.register, name='register'),
    path('home/', views.home, name="home"),
    path('services/', views.services, name="services"),
    path('docters/', views.docters, name="docters"),
    path('healthLibrary/', views.healthLibrary, name="healthLibrary"),
    path('about/', views.about, name="about"),
    path('register/', views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('healthcheckup/', views.healthcheckup, name="healthcheckup"),
    path('wellnesscart/', views.wellnesscart, name="wellnesscart"),
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
    # Special Doctor Appoinments methods
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('book/<int:doc_id>/', views.create_booking, name='create_booking'),
    path('bookings/<int:doc_id>/', views.view_doctor_bookings, name='view_doctor_bookings'),
    path('appointment/<int:appointment_id>/', views.appointment_detail, name='appointment_detailD'),


    #health chekup form methods
    # urls.py
# urls.py
    path('admin/reports/healthcheckup/<int:pk>/', views.health_checkup_detail, name='reports_healthcheckup_detail'),
    
    path("ai_chat", views.ai_chat, name="ai_chat"),
    #Add Activty Url
    path("activity/",views.add_activity, name="add_activity"),
    path('activity/<int:activity_id>/', views.edit_activity, name='edit_activity'),
    path("delete_activity/<int:activity_id>/",views.delete_activity, name="delete_activity"),
    
    #AI Chatbot methods
    path('new/',views.new_chat, name='new_chat'),
    path('chat/<str:id>/',views.chat_view, name='chat_view'),
    
    # Create a Add to Cart Model
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_view, name='cart_view'),
    # Create a Add to Cart Remove Steps Methods
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    # final order summary Buy methods
    path('buy/<int:product_id>/', views.buy_now, name='buy_now'),
    path('order/<int:order_id>/', views.order_summary, name='order_summary'),
    # Payment Integration methods
    path('payment/<int:order_id>/', views.payment_page, name='payment_page'),
    path('place_order/<int:order_id>/', views.place_order, name='place_order'),
    path('order_success/<int:order_id>/', views.order_success, name='order_success'),
    # final order summary Buy methods
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('sales-chart/', views.sales_chart_view, name='sales_chart'),
    # Custom Authentication Forms method
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(form_class=CustomAuthenticationForm), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

]
