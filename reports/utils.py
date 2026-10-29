import os
import re
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def get_openai_client():
    api_key = getattr(settings, 'OPENAI_API_KEY', '') or os.getenv('OPENAI_API_KEY', '')
    api_key = api_key.strip()
    if not api_key:
        return None
    try:
        from openai import OpenAI
        return OpenAI(api_key=api_key)
    except Exception as e:
        logger.error(f"Error initializing OpenAI client: {e}")
        return None


def get_fallback_healthcare_response(user_input):
    """
    Intelligent healthcare assistant fallback when OpenAI API is unavailable,
    quota is exhausted, or network is offline.
    """
    query = user_input.lower().strip()

    # 1. Emergency Detection
    emergency_keywords = [
        'chest pain', 'heart attack', 'cannot breathe', 'hard to breathe', 
        'shortness of breath', 'unconscious', 'severe bleeding', 'stroke', 
        'sudden numbness', 'loss of speech', 'coughing blood', 'poison'
    ]
    if any(k in query for k in emergency_keywords):
        return (
            "🚨 **URGENT MEDICAL ALERT**\n\n"
            "Your message mentions symptoms that could indicate a life-threatening medical emergency.\n\n"
            "**Immediate Actions:**\n"
            "• Call emergency services immediately (such as 102/108/112 or your local emergency line).\n"
            "• Go to the nearest emergency room or hospital immediately.\n"
            "• Do not attempt to drive yourself if you are feeling faint, dizzy, or in severe pain.\n\n"
            "*Disclaimer: This AI assistant cannot handle active medical emergencies.*"
        )

    # 2. Fever & High Temperature
    if any(k in query for k in ['fever', 'temperature', 'chills', 'shivering']):
        return (
            "🌡️ **Fever Management Advice**\n\n"
            "A fever is usually the body's natural response to fighting off an infection.\n\n"
            "**General Self-Care Tips:**\n"
            "• **Hydration:** Drink plenty of fluids like water, herbal teas, coconut water, or clear broths to prevent dehydration.\n"
            "• **Rest:** Give your body ample rest and avoid strenuous physical activities.\n"
            "• **Cooling:** Wear lightweight, breathable clothing and use a lukewarm sponge bath if comfortable (avoid cold baths).\n"
            "• **Over-the-counter Care:** Common fever reducers like Paracetamol / Acetaminophen may be used according to package instructions.\n\n"
            "**When to See a Doctor:**\n"
            "• Fever exceeds 102°F (38.9°C) or lasts more than 3 days.\n"
            "• Accompanied by severe headache, stiff neck, persistent vomiting, or rash.\n\n"
            "*Disclaimer: Please consult a licensed physician for diagnosis and prescription medications.*"
        )

    # 3. Headache & Migraine
    if any(k in query for k in ['headache', 'migraine', 'head pain', 'throbbing head']):
        return (
            "🧠 **Headache & Migraine Guidance**\n\n"
            "**Recommended Relief Measures:**\n"
            "• **Rest in a Quiet, Dark Room:** Sensory overload can worsen headaches and migraines.\n"
            "• **Hydrate:** Dehydration is a very common trigger; drink 1-2 glasses of water.\n"
            "• **Cold or Warm Compress:** Place a cold pack on your forehead or a warm cloth on your neck/shoulders.\n"
            "• **Reduce Screen Time:** Take breaks from computer and phone screens.\n\n"
            "**When to Seek Immediate Medical Help:**\n"
            "• Sudden, severe 'thunderclap' headache.\n"
            "• Headache accompanied by vision changes, confusion, fever, or neck stiffness.\n\n"
            "*Disclaimer: Persistent headaches should be evaluated by a healthcare professional.*"
        )

    # 4. Cold, Cough & Sore Throat
    if any(k in query for k in ['cold', 'cough', 'sore throat', 'runny nose', 'congestion', 'flu', 'phlegm']):
        return (
            "🫁 **Cold, Cough & Respiratory Comfort**\n\n"
            "**Home Care & Remedies:**\n"
            "• **Warm Salt Water Gargle:** Gargle with 1/2 teaspoon of salt in warm water 2-3 times daily for sore throat.\n"
            "• **Steam Inhalation:** Inhaling warm steam can help relieve sinus and nasal congestion.\n"
            "• **Honey and Warm Tea:** A spoonful of honey in warm water or ginger tea soothes cough and throat irritation (not for infants under 1 year).\n"
            "• **Fluids & Rest:** Keep your body well-hydrated to thin mucus secretions.\n\n"
            "**When to Consult a Physician:**\n"
            "• Cough lasting longer than 2 weeks or coughing up thick yellow/green phlegm or blood.\n"
            "• High fever or wheezing/difficulty breathing.\n\n"
            "*Disclaimer: For persistent symptoms, consider booking an appointment with an ENT specialist or general physician.*"
        )

    # 5. Blood Pressure & Hypertension
    if any(k in query for k in ['blood pressure', 'bp', 'hypertension', 'systolic', 'diastolic']):
        return (
            "💓 **Blood Pressure Information**\n\n"
            "**Healthy Blood Pressure Ranges:**\n"
            "• **Normal:** Less than 120/80 mmHg\n"
            "• **Elevated:** Systolic 120-129 and Diastolic < 80 mmHg\n"
            "• **Hypertension (Stage 1):** Systolic 130-139 or Diastolic 80-89 mmHg\n"
            "• **Hypertension (Stage 2):** Systolic 140 or higher or Diastolic 90 or higher mmHg\n\n"
            "**Lifestyle Tips for Healthy BP:**\n"
            "• **Dietary Sodium:** Limit salt intake to less than 2,000 mg per day.\n"
            "• **DASH Diet:** Eat plenty of vegetables, fruits, whole grains, and lean proteins.\n"
            "• **Regular Exercise:** Aim for at least 30 minutes of moderate activity most days.\n"
            "• **Stress Reduction:** Practice deep breathing, meditation, and ensure 7-8 hours of sleep.\n\n"
            "*Disclaimer: Never stop or adjust prescribed blood pressure medication without consulting your doctor.*"
        )

    # 6. Diabetes & Blood Sugar
    if any(k in query for k in ['diabetes', 'sugar', 'blood sugar', 'glucose', 'insulin']):
        return (
            "🩸 **Blood Sugar & Diabetes Support**\n\n"
            "**Standard Blood Sugar Ranges (Typical Reference):**\n"
            "• **Fasting (Before meals):** 70 - 99 mg/dL (Normal), 100 - 125 mg/dL (Prediabetes), 126+ mg/dL (Diabetes)\n"
            "• **Postprandial (2 hours after meal):** Less than 140 mg/dL\n\n"
            "**Management & Dietary Guidance:**\n"
            "• **Complex Carbohydrates:** Choose whole grains, oats, and legumes instead of refined white flour and sugar.\n"
            "• **Fiber Rich Foods:** High fiber helps slow glucose absorption and stabilize blood sugar.\n"
            "• **Regular Physical Activity:** Walking 15-30 minutes after meals improves insulin sensitivity.\n"
            "• **Regular Monitoring:** Keep a log of your fasting and post-meal glucose readings.\n\n"
            "*Disclaimer: Consult your endocrinologist or diabetologist for customized diet and medical plans.*"
        )

    # 7. Stomach Pain, Acidity, Digestion & Nausea
    if any(k in query for k in ['stomach', 'acidity', 'gas', 'indigestion', 'nausea', 'vomit', 'diarrhea', 'constipation', 'belly']):
        return (
            "🌿 **Digestive Health & Stomach Comfort**\n\n"
            "**Tips for Relieving Digestive Discomfort:**\n"
            "• **Small, Frequent Meals:** Avoid heavy, spicy, fried, or highly acidic foods.\n"
            "• **Stay Hydrated:** Sip warm water, oral rehydration solutions (ORS), or peppermint/chamomile tea.\n"
            "• **BRAT Diet for Upset Stomach:** Bananas, Rice, Applesauce, and Toast are gentle on the digestive tract.\n"
            "• **Posture:** Stay upright for at least 2 hours after eating; avoid lying down immediately after meals.\n\n"
            "**Warning Signs (Seek Medical Attention):**\n"
            "• Severe, localized abdominal pain (e.g., lower right side).\n"
            "• Inability to keep fluids down for over 24 hours, or blood in stool/vomit.\n\n"
            "*Disclaimer: Persistent abdominal symptoms require physical examination by a physician.*"
        )

    # 8. Diet, Nutrition & Weight Management
    if any(k in query for k in ['diet', 'nutrition', 'food', 'weight loss', 'calories', 'healthy eating']):
        return (
            "🥗 **Healthy Nutrition & Diet Guidance**\n\n"
            "**Core Principles of Balanced Nutrition:**\n"
            "• **Plate Balance:** Aim for 1/2 plate vegetables/fruits, 1/4 plate lean protein (pulses, eggs, tofu, fish, chicken), and 1/4 plate whole grains.\n"
            "• **Healthy Fats:** Incorporate nuts, seeds, olive oil, and avocado in moderate portions.\n"
            "• **Hydration:** Aim for 2.5 - 3 liters of clean water daily.\n"
            "• **Mindful Eating:** Limit ultra-processed snacks, sugary sodas, and excess sodium.\n\n"
            "You can track your calories and fitness goals anytime on the **Exercise Dashboard**!\n\n"
            "*Disclaimer: A personalized nutrition plan from a registered dietitian is recommended for specific medical conditions.*"
        )

    # 9. Exercise, Fitness & Workouts
    if any(k in query for k in ['exercise', 'workout', 'fitness', 'cardio', 'gym', 'running', 'walking']):
        return (
            "🏃‍♂️ **Fitness & Exercise Recommendations**\n\n"
            "**Standard Health Guidelines:**\n"
            "• **Aerobic Activity:** At least 150 minutes of moderate aerobic exercise (e.g. brisk walking, cycling, swimming) per week.\n"
            "• **Strength Training:** Muscle-strengthening exercises targeting major muscle groups at least 2 days a week.\n"
            "• **Warm-up & Cool-down:** Always warm up 5-10 minutes before workouts and stretch afterwards to prevent injuries.\n"
            "• **Consistency:** Even 15-20 minutes daily makes a significant impact on cardiovascular and mental health!\n\n"
            "Log your daily exercises in our **Exercise Dashboard** to monitor your calorie burn and workout streaks.\n\n"
            "*Disclaimer: Consult your doctor before starting any intense new exercise routine if you have existing health conditions.*"
        )

    # 10. Booking Appointments & Hospital Doctors
    if any(k in query for k in ['doctor', 'appointment', 'book', 'hospital', 'specialist', 'clinic']):
        return (
            "👨‍⚕️ **Doctor Appointments & Hospital Services**\n\n"
            "You can easily connect with our qualified medical specialists through this portal:\n\n"
            "• **Book Appointment:** Visit the [Book Appointment](/book/) page to schedule a visit.\n"
            "• **Find Specialists:** Browse our [Doctors Directory](/doctors/) for cardiologists, pediatricians, orthopedics, and general physicians.\n"
            "• **Health Packages:** Check available preventive health packages under [Health Checkup](/healthcheckup/).\n\n"
            "If you need immediate in-person attention, please visit the nearest hospital branch."
        )

    # 11. General Greetings / Default Helpful Health Guide
    return (
        "👋 **Hello! I am your AI Healthcare Assistant.**\n\n"
        "I am here to support you with reliable health information, wellness advice, and portal assistance. Here are some topics you can ask me about:\n\n"
        "• 🩺 **Common Symptoms:** Advice on fever, cough, cold, headaches, or stomach upset\n"
        "• 💓 **Vitals & Monitoring:** Understanding blood pressure, blood sugar, and cholesterol\n"
        "• 🥗 **Lifestyle & Wellness:** Healthy nutrition, weight management, and workout routines\n"
        "• 📅 **Doctor Bookings:** How to schedule doctor appointments and checkup packages\n\n"
        "How can I assist you with your health today?\n\n"
        "*Disclaimer: This assistant provides general healthcare information for educational purposes and is not a substitute for professional medical diagnosis or treatment.*"
    )


def generate_response(user_input, recent_messages):
    """
    Generates a response using OpenAI GPT model if available,
    or falls back seamlessly to the intelligent healthcare knowledge base.
    """
    client = get_openai_client()

    if client:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are Dr. AI, an empathetic, highly knowledgeable, and professional healthcare assistant "
                    "for a modern healthcare portal. Provide concise, clear, evidence-based, and safe healthcare information. "
                    "Help users understand symptoms, general wellness, healthy diet, exercise, and when to seek medical attention. "
                    "Always maintain a warm, reassuring, and professional tone. "
                    "If symptoms suggest an emergency (e.g. chest pain, severe shortness of breath, sudden numbness, stroke symptoms), "
                    "urge the user to seek immediate emergency medical care. "
                    "End responses with a brief reminder that your advice is for informational purposes and they should consult a doctor."
                )
            }
        ]

        for message in recent_messages:
            role = "user" if getattr(message, 'sender', '') == "human" else "assistant"
            messages.append({
                "role": role,
                "content": getattr(message, 'text', '')
            })

        messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                timeout=20,
                max_tokens=600,
                temperature=0.7
            )
            ai_text = response.choices[0].message.content.strip()
            if ai_text:
                return ai_text
        except Exception as e:
            logger.warning(f"OpenAI completion failed: {e}. Utilizing smart healthcare fallback.")

    # Fallback to intelligent healthcare response engine
    return get_fallback_healthcare_response(user_input)


from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException


def format_phone_number(phone):
    """
    Cleans and standardizes an Indian mobile phone number into E.164 format (+91XXXXXXXXXX).
    """
    if not phone:
        return None

    # Remove all whitespace, hyphens, parentheses, and dots
    cleaned = re.sub(r'[\s\-\(\)\.]', '', str(phone).strip())

    if cleaned.startswith('+91'):
        digits = cleaned[3:]
        if len(digits) == 10 and digits.isdigit():
            return cleaned
        return cleaned

    if cleaned.startswith('91') and len(cleaned) == 12 and cleaned.isdigit():
        return '+' + cleaned

    if cleaned.startswith('0') and len(cleaned) == 11 and cleaned.isdigit():
        return '+91' + cleaned[1:]

    if len(cleaned) == 10 and cleaned.isdigit():
        return '+91' + cleaned

    # If it starts with + and has at least 10 digits
    if cleaned.startswith('+') and len(cleaned) >= 11:
        return cleaned

    return None


def send_appointment_sms(
    phone_number,
    patient_name,
    doctor_name,
    department,
    schedule_date,
    schedule_time,
    floor_number,
):
    """
    Sends a doctor appointment confirmation SMS via Twilio.
    """
    formatted_phone = format_phone_number(phone_number)
    if not formatted_phone:
        err_msg = f"Invalid phone number: {phone_number}"
        logger.warning(err_msg)
        return False, err_msg

    try:
        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN,
        )

        message_body = (
            f"Dear {patient_name}, your appointment has been "
            f"scheduled successfully.\n"
            f"Doctor: Dr. {doctor_name}\n"
            f"Department: {department}\n"
            f"Date: {schedule_date}\n"
            f"Time: {schedule_time}\n"
            f"Floor: {floor_number}\n"
            f"Thank you for choosing our hospital."
        )

        message = client.messages.create(
            body=message_body,
            from_=settings.TWILIO_PHONE_NUMBER,
            to=formatted_phone,
        )

        logger.info(f"Twilio SMS sent to {formatted_phone}: SID {message.sid}")
        return True, message.sid

    except TwilioRestException as exc:
        err_msg = f"Twilio SMS failed (Code {exc.code}): {exc.msg}"
        logger.exception(err_msg)
        return False, err_msg

    except Exception as error:
        err_msg = f"Unexpected SMS error: {error}"
        logger.exception(err_msg)
        return False, err_msg


def send_doctor_schedule_sms(schedule):
    """
    Helper function to send SMS for a DoctorSchedule instance.
    Automatically retrieves the patient's phone and details from the schedule/appointment.
    """
    # 1. Determine phone number: check customer_mobile first, fallback to appointment.phone
    phone = str(schedule.customer_mobile or '').strip()
    appointment = getattr(schedule, 'appointment', None)

    if not phone and appointment:
        phone = str(appointment.phone or '').strip()

    if not phone:
        return False, "No patient mobile number found on DoctorSchedule or Appointment."

    formatted_phone = format_phone_number(phone)
    if not formatted_phone:
        return False, f"Invalid mobile number format: '{phone}'."

    # Update customer_mobile on schedule if it was missing or unformatted
    if schedule.customer_mobile != formatted_phone:
        schedule.customer_mobile = formatted_phone
        schedule.save(update_fields=['customer_mobile'])

    patient_name = appointment.name if appointment else "Patient"

    return send_appointment_sms(
        phone_number=formatted_phone,
        patient_name=patient_name,
        doctor_name=schedule.doctor_name,
        department=schedule.department,
        schedule_date=schedule.schedule_date,
        schedule_time=schedule.schedule_time,
        floor_number=schedule.floor_number,
    )