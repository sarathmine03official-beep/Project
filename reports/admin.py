from django.contrib import admin, messages
from django.utils.html import format_html
from django.urls import reverse, path
from django.shortcuts import render
from django.db.models import Sum

from .models import (
    Goal, Activity, Product, Doctor, Appointment, 
    DoctorSchedule, HealthCheckup, Order, DoctorBooking, 
    ChatSession, Message
)

# Product Model
admin.site.register(Product)

# Doctor Model
admin.site.register(Doctor)

# Goal and Activity
admin.site.register(Goal)
admin.site.register(Activity)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'date', 'time', 'department', 'symptoms')
    search_fields = ('name', 'phone')
    list_filter = ('date',)


# Doctor scheduling admin page
@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = (
        'appointment__name',
        'department',
        'customer_mobile',
        'schedule_date',
        'schedule_time',
        'status',
        'appointment',
    )
    list_filter = ('department', 'status', 'schedule_date')
    search_fields = ('doctor_name', 'customer_mobile', 'appointment__name', 'appointment__phone')

    def save_model(self, request, obj, form, change):
        # Auto-populate customer_mobile from appointment if blank
        if not obj.customer_mobile and obj.appointment and getattr(obj.appointment, 'phone', None):
            obj.customer_mobile = obj.appointment.phone

        super().save_model(request, obj, form, change)

        # Trigger SMS whenever status is 'Scheduled'
        if obj.status == 'Scheduled':
            success, result = obj.send_schedule_sms()
            if success:
                messages.success(
                    request,
                    f"Schedule saved! Confirmation SMS sent to {obj.customer_mobile}. (Twilio SID: {result})"
                )
            else:
                messages.warning(
                    request,
                    f"Schedule saved, but Twilio SMS could not be sent: {result}"
                )


@admin.register(HealthCheckup)
class HealthCheckupAdmin(admin.ModelAdmin):
    list_display = (
        'patient',
        'blood_sugar',
        'blood_pressure',
        'cholesterol',
        'health_status',
        'checked_on',
        'view_checkup'
    )

    def health_status(self, obj):
        sugar = obj.blood_sugar
        chol = obj.cholesterol

        try:
            systolic, diastolic = map(int, obj.blood_pressure.split('/'))
        except ValueError:
            systolic, diastolic = 0, 0

        if sugar < 100 and chol < 200 and systolic <= 120 and diastolic <= 80:
            color, status = 'green', 'Normal'
        elif sugar <= 160 or chol <= 230 or systolic <= 135:
            color, status = 'orange', 'Medium'
        else:
            color, status = 'red', 'High'

        return format_html('<b style="color:{};">{}</b>', color, status)

    health_status.short_description = 'Health Status'

    def view_checkup(self, obj):
        url = reverse('reports_healthcheckup_detail', args=[obj.id])
        return format_html(
            '<a class="button" href="{}" style="color:white; background:#007bff; padding:5px 10px; border-radius:5px;">View Checkup</a>',
            url
        )

    view_checkup.short_description = 'View Checkup'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'total_price', 'ordered_at')
    search_fields = ('user__username', 'product__name')
    list_filter = ('ordered_at',)
    change_list_template = 'admin/orders_changelist.html'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view)),
            path('sales-chart/', self.admin_site.admin_view(self.sales_chart_view)),
        ]
        return custom_urls + urls

    def dashboard_view(self, request):
        product_sales = (
            Order.objects.values('product__name')
            .annotate(total_sold=Sum('quantity'))
            .order_by('-total_sold')
        )
        labels = [item['product__name'] for item in product_sales]
        data = [item['total_sold'] for item in product_sales]
        return render(request, 'admin/dashboard.html', {'labels': labels, 'data': data})

    def sales_chart_view(self, request):
        product_sales = (
            Order.objects.values('product__name')
            .annotate(total_sold=Sum('quantity'))
            .order_by('-total_sold')
        )
        labels = [item['product__name'] for item in product_sales]
        data = [item['total_sold'] for item in product_sales]
        return render(request, 'admin/sales_chart.html', {'labels': labels, 'data': data})


# Special Doctor Appointments
@admin.register(DoctorBooking)
class DoctorBookingAdmin(admin.ModelAdmin):
    list_display = ('patient_fullname', 'doctor_ref', 'appointment_date', 'appointment_time', 'status')
    list_filter = ('doctor_ref', 'status', 'appointment_date')
    search_fields = ('patient_fullname', 'doctor_ref__name')


# AI Chatbot Admin Models
class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'text', 'created')
    can_delete = True

@admin.register(ChatSession)
class ChatSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'get_preview', 'message_count')
    inlines = [MessageInline]
    ordering = ('-created',)

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = 'Messages'

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'session', 'sender', 'preview_text', 'created')
    list_filter = ('sender', 'created')
    search_fields = ('text',)

    def preview_text(self, obj):
        return (obj.text[:50] + '...') if len(obj.text) > 50 else obj.text
    preview_text.short_description = 'Message'
