# ⚡ Quick Start Guide
## Get Your WhatsApp AI Running in 15 Minutes

---

## 📝 Checklist

Before you start, you need:

- [ ] Python 3.8+ installed
- [ ] WhatsApp Business API account (Twilio recommended)
- [ ] OpenAI or Anthropic API key
- [ ] 15 minutes of time

---

## 🚀 5-Step Setup

### Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to project
cd c:\Users\TAREK\OneDrive\Desktop\ShiftsTab\clinic

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install packages
pip install -r requirements.txt
```

### Step 2: Get API Keys (5 minutes)

**WhatsApp (Twilio):**
1. Go to https://www.twilio.com/try-twilio
2. Sign up for free trial ($15 credit)
3. Navigate to: Console → Messaging → Try WhatsApp
4. Copy: Account SID, Auth Token, WhatsApp Number

**OpenAI:**
1. Go to https://platform.openai.com
2. Sign up
3. Go to API Keys
4. Create new key
5. Copy it (starts with `sk-`)

### Step 3: Configure (3 minutes)

```bash
# Copy example config
copy .env.example .env

# Edit with your credentials
notepad .env
```

Fill in:
```env
TWILIO_ACCOUNT_SID=AC...
TWILIO_AUTH_TOKEN=...
OPENAI_API_KEY=sk-...
```

### Step 4: Initialize Database (1 minute)

```bash
cd execution
python setup_database.py
```

### Step 5: Start System (1 minute)

**Option A - Windows (Easy):**
```bash
start.bat
```

**Option B - Manual:**

Terminal 1:
```bash
python execution/whatsapp_webhook_server.py
```

Terminal 2:
```bash
python execution/background_monitor.py
```

---

## ✅ Verify It's Working

1. **Check server**: Visit http://localhost:5000/health
2. **Expose to internet**:
   ```bash
   ngrok http 5000
   ```
3. **Configure webhook**: Add ngrok URL to Twilio console
4. **Test**: Send WhatsApp message to 0543 824 7016
5. **Wait 5 minutes** → AI should respond!

---

## 🎯 Test Messages

Try these:
- "Merhaba, randevu almak istiyorum"
- "Ücretler ne kadar?"
- "Çocuğum 3 yaşında ve konuşmuyor"

---

## 🐛 Common Issues

**"Configuration errors"**
→ Check .env file has all required values

**"Can't connect to database"**
→ Run: `python execution/setup_database.py`

**"Webhook not receiving messages"**
→ Make sure ngrok is running and URL is in Twilio

---

## 📚 Next Steps

Once working:
1. Read full setup guide: [AI-AUTOMATION-SETUP.md](AI-AUTOMATION-SETUP.md)
2. Deploy to production server
3. Customize AI responses
4. Monitor and optimize

---

**Need help?** Check the logs:
- `logs/webhook.log`
- `logs/background_monitor.log`
