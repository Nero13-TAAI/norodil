"""
Configuration management for WhatsApp AI Automation
Loads environment variables and provides configuration constants
"""

import os
from datetime import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ==================== API CREDENTIALS ====================

# WhatsApp Business API (choose your provider)
WHATSAPP_API_PROVIDER = os.getenv('WHATSAPP_API_PROVIDER', 'twilio')  # twilio, 360dialog, meta
WHATSAPP_API_KEY = os.getenv('WHATSAPP_API_KEY', '')
WHATSAPP_API_SECRET = os.getenv('WHATSAPP_API_SECRET', '')
WHATSAPP_PHONE_NUMBER = os.getenv('WHATSAPP_PHONE_NUMBER', '+905438247016')
WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID', '')  # For Meta API

# Twilio specific
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', '')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+905438247016')

# AI API (OpenAI or Anthropic)
AI_PROVIDER = os.getenv('AI_PROVIDER', 'openai')  # openai, anthropic
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
AI_MODEL = os.getenv('AI_MODEL', 'gpt-4o-mini')  # gpt-4o, gpt-4o-mini, claude-3-sonnet-20240229

# ==================== SERVER CONFIG ====================

# Flask server settings
FLASK_HOST = os.getenv('FLASK_HOST', '0.0.0.0')
FLASK_PORT = int(os.getenv('FLASK_PORT', '5000'))
FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Webhook verification token (for security)
WEBHOOK_VERIFY_TOKEN = os.getenv('WEBHOOK_VERIFY_TOKEN', 'norodil_secure_token_2024')

# ==================== AUTOMATION CONFIG ====================

# Response timing (in seconds)
RESPONSE_DELAY = int(os.getenv('RESPONSE_DELAY', '300'))  # 5 minutes = 300 seconds

# Maximum AI responses per conversation before requiring human
MAX_AI_RESPONSES_PER_CONVERSATION = int(os.getenv('MAX_AI_RESPONSES', '3'))

# Business hours (Turkey time)
BUSINESS_HOURS_START = time(9, 0)   # 09:00
BUSINESS_HOURS_END = time(20, 0)    # 20:00
BUSINESS_DAYS = [5, 6]  # Saturday=5, Sunday=6 (0=Monday)

# Respond immediately outside business hours
IMMEDIATE_RESPONSE_OUTSIDE_HOURS = os.getenv('IMMEDIATE_OUTSIDE_HOURS', 'True').lower() == 'true'

# Emergency keywords (immediate notification, no AI response)
EMERGENCY_KEYWORDS = ['acil', 'urgent', 'emergency', 'ivedi', 'hemen']

# ==================== DATABASE CONFIG ====================

DATABASE_PATH = os.getenv('DATABASE_PATH', 'data/conversations.db')

# ==================== BUSINESS CONTEXT ====================

BUSINESS_INFO = {
    'name': 'NÖRODİL Dil ve Konuşma Merkezi',
    'therapist': 'Uzman Terapist Ekibimiz',
    'phone': '0543 824 7016',
    'email': 'norodilkonusma@gmail.com',
    'address': 'Huzurevleri Mah. Şanlıurfa Bulv. Çavuşoğlu Plaza Kat: 2 No: 4, Kayapınar/Diyarbakır',
    'working_hours': 'Cumartesi-Pazar: 09:00 - 20:00',
    'services': [
        'Kekemelik Tedavisi',
        'Artikülasyon Bozuklukları',
        'Ses Bozuklukları',
        'Gecikmiş Dil ve Konuşma',
        'Otizm Spektrum Bozukluğu'
    ],
    'pricing_policy': 'Seans ücretleri danışanın ihtiyacına göre değişmektedir. Net ücret bilgisi için lütfen iletişime geçiniz.',
    'online_therapy': True
}

# ==================== AI PROMPT CONFIGURATION ====================

SYSTEM_PROMPT = f"""Sen {BUSINESS_INFO['name']} kliniğinin yardımcı asistanısın.

GÖREV:
- Hastalardan gelen mesajlara profesyonel, yardımsever ve dostane bir şekilde yanıt ver
- Dil ve konuşma terapisi hizmetleri hakkında doğru bilgi ver
- Randevu taleplerini kaydet ve teyit et
- Karmaşık tıbbi sorular için terapiste yönlendir

KLİNİK BİLGİLERİ:
- İsim: {BUSINESS_INFO['name']}
- Terapist: {BUSINESS_INFO['therapist']}
- Telefon: {BUSINESS_INFO['phone']}
- Adres: {BUSINESS_INFO['address']}
- Çalışma Saatleri: {BUSINESS_INFO['working_hours']}

HİZMETLER:
{chr(10).join(f'- {service}' for service in BUSINESS_INFO['services'])}

ÜCRET POLİTİKASI:
{BUSINESS_INFO['pricing_policy']}

İLETİŞİM KURALLARI:
1. Her zaman Türkçe yanıt ver
2. Profesyonel ama sıcak bir ton kullan
3. Kısa ve net cevaplar ver
4. Tıbbi teşhis koyma, sadece genel bilgi ver
5. Karmaşık durumları terapiste yönlendir
6. Emojileri ölçülü kullan (1-2 emoji per mesaj)
7. MUTLAKA şu cümleyi ekle: "Bu otomatik yanıttır. {BUSINESS_INFO['therapist']} size kısa sürede dönüş yapacaktır."

ÖRNEKLER:

Soru: "Randevu almak istiyorum"
Cevap: "Merhaba! Randevu talebiniz için teşekkür ederiz 📅

Aşağıdaki bilgileri paylaşır mısınız?
- Adınız ve soyadınız
- Yaşınız (veya çocuğunuzun yaşı)
- Hangi konuda destek almak istersiniz?
- Tercih ettiğiniz gün ve saat

Bu otomatik yanıttır. Dkt. Veysi İkvan size kısa sürede dönüş yapacaktır."

Soru: "Ücretler ne kadar?"
Cevap: "Seans ücretlerimiz, danışanın ihtiyacına ve tedavi planına göre değişmektedir.

Size özel ücret bilgisi için terapi ihtiyacınızı ve yaşınızı paylaşırsanız, detaylı bilgi verebiliriz.

Bu otomatik yanıttır. Dkt. Veysi İkvan size kısa sürede dönüş yapacaktır."

Soru: "Çocuğumda konuşma problemi var"
Cevap: "Anlıyorum, çocuğunuzun konuşma gelişimi konusunda destek almak istiyorsunuz.

Çocuğunuzun yaşını ve tam olarak hangi tür zorluklarla karşılaştığını öğrenebilir miyim? (örn: sesleri çıkaramama, geç konuşmaya başlama, kekemelik)

Detaylı değerlendirme için randevu oluşturabiliriz.

Bu otomatik yanıttır. Dkt. Veysi İkvan size kısa sürede dönüş yapacaktır."
"""

# ==================== LOGGING CONFIG ====================

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
LOG_FILE = os.getenv('LOG_FILE', 'logs/whatsapp_ai.log')

# ==================== RATE LIMITING ====================

# Maximum messages per minute to prevent abuse
MAX_MESSAGES_PER_MINUTE = int(os.getenv('MAX_MESSAGES_PER_MINUTE', '10'))

# ==================== VALIDATION ====================

def validate_config():
    """Validate that all required configuration is present"""
    errors = []

    # Check WhatsApp API credentials
    if WHATSAPP_API_PROVIDER == 'twilio':
        if not TWILIO_ACCOUNT_SID:
            errors.append("TWILIO_ACCOUNT_SID is required")
        if not TWILIO_AUTH_TOKEN:
            errors.append("TWILIO_AUTH_TOKEN is required")
    elif WHATSAPP_API_PROVIDER == 'meta':
        if not WHATSAPP_API_KEY:
            errors.append("WHATSAPP_API_KEY is required for Meta API")
        if not WHATSAPP_PHONE_NUMBER_ID:
            errors.append("WHATSAPP_PHONE_NUMBER_ID is required for Meta API")

    # Check AI API credentials
    if AI_PROVIDER == 'openai' and not OPENAI_API_KEY:
        errors.append("OPENAI_API_KEY is required")
    elif AI_PROVIDER == 'anthropic' and not ANTHROPIC_API_KEY:
        errors.append("ANTHROPIC_API_KEY is required")

    if errors:
        raise ValueError(f"Configuration errors:\n" + "\n".join(f"- {err}" for err in errors))

    return True

# ==================== UTILITY FUNCTIONS ====================

def is_business_hours(dt=None):
    """Check if current time is within business hours"""
    from datetime import datetime
    import pytz

    if dt is None:
        # Turkey timezone
        turkey_tz = pytz.timezone('Europe/Istanbul')
        dt = datetime.now(turkey_tz)

    # Check day of week
    if dt.weekday() not in BUSINESS_DAYS:
        return False

    # Check time
    current_time = dt.time()
    return BUSINESS_HOURS_START <= current_time <= BUSINESS_HOURS_END

def contains_emergency_keyword(message):
    """Check if message contains emergency keywords"""
    message_lower = message.lower()
    return any(keyword in message_lower for keyword in EMERGENCY_KEYWORDS)

if __name__ == '__main__':
    # Test configuration
    print("Configuration loaded successfully!")
    print(f"WhatsApp Provider: {WHATSAPP_API_PROVIDER}")
    print(f"AI Provider: {AI_PROVIDER}")
    print(f"Response Delay: {RESPONSE_DELAY}s")
    print(f"Business: {BUSINESS_INFO['name']}")
    print(f"Is business hours: {is_business_hours()}")

    try:
        validate_config()
        print("\n✅ All configuration validated successfully!")
    except ValueError as e:
        print(f"\n❌ Configuration errors:\n{e}")
