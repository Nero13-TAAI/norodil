
# WhatsApp AI Automation Setup Guide
## NÖRODİL Dil ve Konuşma Merkezi

Complete guide to set up automated AI responses for your WhatsApp Business.

---

## 🎯 What This System Does

**Automatically responds to patient messages when you don't reply within 5 minutes.**

### Features:
- ✅ 5-minute delay before AI responds (you have time to reply manually)
- ✅ Intelligent responses using GPT-4 or Claude AI
- ✅ Tracks conversation history for context
- ✅ Automatic outside-hours responses
- ✅ Emergency keyword detection
- ✅ Limits AI responses (escalates to human after 3 AI messages)
- ✅ Complete conversation logging
- ✅ Professional, context-aware responses

---

## 📋 Prerequisites

### 1. WhatsApp Business API Access
You need **WhatsApp Business API** (not the regular WhatsApp Business app).

**Options:**
- **Twilio** (Recommended for beginners) - https://www.twilio.com/whatsapp
- **Meta** (Facebook) - https://business.whatsapp.com
- **360Dialog** - https://www.360dialog.com

**Cost:** ~$0.005-0.04 per message (varies by provider)

### 2. AI API Access
Choose one:
- **OpenAI** (GPT-4) - https://platform.openai.com
- **Anthropic** (Claude) - https://www.anthropic.com

**Cost:** ~$0.03-0.10 per conversation

### 3. Server/Hosting
You need a server to run the webhook:
- **DigitalOcean** (Recommended) - $6/month
- **Heroku** - $7/month
- **AWS/Google Cloud** - Variable pricing

### 4. Python Knowledge
Basic understanding helpful but not required (everything is automated).

---

## 🚀 Quick Start (Step-by-Step)

### Step 1: Install Python and Dependencies

```bash
# 1. Make sure Python 3.8+ is installed
python --version

# 2. Navigate to the clinic directory
cd c:\Users\TAREK\OneDrive\Desktop\ShiftsTab\clinic

# 3. Create virtual environment
python -m venv venv

# 4. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# 5. Install dependencies
pip install -r requirements.txt
```

### Step 2: Get WhatsApp Business API Credentials

#### Option A: Twilio (Easiest)

1. Sign up at https://www.twilio.com/try-twilio
2. Go to Console → Messaging → Try it out → Send a WhatsApp message
3. Follow setup wizard to activate your phone number for WhatsApp
4. Get your credentials:
   - Account SID
   - Auth Token
   - WhatsApp Phone Number (format: whatsapp:+905438247016)

#### Option B: Meta (More features)

1. Create Facebook Business Account
2. Set up WhatsApp Business API
3. Get:
   - Access Token
   - Phone Number ID
4. Complete business verification

### Step 3: Get AI API Key

#### Option A: OpenAI (Recommended)

1. Sign up at https://platform.openai.com
2. Go to API Keys section
3. Create new API key
4. Copy it (starts with `sk-...`)

#### Option B: Anthropic Claude

1. Sign up at https://console.anthropic.com
2. Get API key
3. Copy it (starts with `sk-ant-...`)

### Step 4: Configure Environment Variables

```bash
# 1. Copy example env file
copy .env.example .env

# 2. Edit .env file with your credentials
notepad .env
```

Fill in your credentials:

```env
# WhatsApp (Twilio example)
WHATSAPP_API_PROVIDER=twilio
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+905438247016

# AI (OpenAI example)
AI_PROVIDER=openai
OPENAI_API_KEY=sk-xxxxxxxxxxxxx
AI_MODEL=gpt-4o-mini

# Automation
RESPONSE_DELAY=300
MAX_AI_RESPONSES=3
```

### Step 5: Initialize Database

```bash
# Navigate to execution folder
cd execution

# Run setup script
python setup_database.py
```

You should see:
```
✅ Database initialized successfully!
```

### Step 6: Test Configuration

```bash
# Test that everything is configured correctly
python config.py
```

Should show:
```
✅ All configuration validated successfully!
```

### Step 7: Start the Webhook Server

```bash
# Start the Flask server
python whatsapp_webhook_server.py
```

You should see:
```
🚀 Starting WhatsApp Webhook Server...
✅ Configuration validated
* Running on http://0.0.0.0:5000
```

### Step 8: Expose to Internet (for development)

Use ngrok to expose your local server:

```bash
# Install ngrok from https://ngrok.com
# Then run:
ngrok http 5000
```

You'll get a URL like: `https://abc123.ngrok.io`

### Step 9: Configure Webhook URL

#### For Twilio:
1. Go to Twilio Console → Phone Numbers → Your WhatsApp Number
2. Under "Messaging", set:
   - **When a message comes in**: `https://your-ngrok-url.ngrok.io/webhook`
   - Method: POST
3. Save

#### For Meta:
1. Go to App Dashboard → WhatsApp → Configuration
2. Set Webhook URL: `https://your-ngrok-url.ngrok.io/webhook`
3. Verify Token: (use the token from your .env file)
4. Subscribe to messages webhook

### Step 10: Start Background Monitor

Open a **second terminal** and run:

```bash
cd execution
python background_monitor.py
```

You should see:
```
🚀 Background monitor started
Check interval: 30s
Response delay: 300s
```

### Step 11: Test the System!

1. Send a WhatsApp message to your business number: **0543 824 7016**
2. Wait 5 minutes without replying
3. AI should automatically respond!

Test message: "Merhaba, randevu almak istiyorum"

---

## 🎮 How to Use

### Normal Operation

1. **Webhook Server** (Terminal 1):
   ```bash
   python whatsapp_webhook_server.py
   ```

2. **Background Monitor** (Terminal 2):
   ```bash
   python background_monitor.py
   ```

### Manual Response (Override AI)

Just reply via WhatsApp Business app **within 5 minutes**. The AI won't send a message.

### Check Statistics

Visit: http://localhost:5000/stats

Or run:
```bash
python -c "from conversation_tracker import ConversationTracker; import json; print(json.dumps(ConversationTracker().get_statistics(), indent=2))"
```

---

## 🌐 Production Deployment

### Option 1: DigitalOcean (Recommended)

1. Create a Droplet (Ubuntu 22.04)
2. SSH into server
3. Clone your project
4. Install dependencies
5. Use supervisor to keep processes running

```bash
# Install supervisor
sudo apt-get install supervisor

# Create config files
sudo nano /etc/supervisor/conf.d/whatsapp_webhook.conf
```

Config file:
```ini
[program:whatsapp_webhook]
directory=/home/clinic/
command=/home/clinic/venv/bin/python execution/whatsapp_webhook_server.py
autostart=true
autorestart=true
user=clinic
redirect_stderr=true
stdout_logfile=/home/clinic/logs/webhook.log

[program:background_monitor]
directory=/home/clinic/
command=/home/clinic/venv/bin/python execution/background_monitor.py
autostart=true
autorestart=true
user=clinic
redirect_stderr=true
stdout_logfile=/home/clinic/logs/monitor.log
```

Start services:
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all
```

### Option 2: Heroku

1. Create `Procfile`:
```
web: gunicorn execution.whatsapp_webhook_server:app
worker: python execution/background_monitor.py
```

2. Deploy:
```bash
heroku create norodil-whatsapp
git push heroku main
heroku ps:scale web=1 worker=1
```

---

## 🔧 Customization

### Change Response Delay

Edit `.env`:
```env
RESPONSE_DELAY=180  # 3 minutes instead of 5
```

### Modify AI Responses

Edit `execution/config.py` → `SYSTEM_PROMPT` section to change AI behavior.

### Add Custom Logic

Edit `execution/whatsapp_webhook_server.py` → `process_incoming_message()` function.

---

## 📊 Monitoring

### View Logs

```bash
# Webhook server logs
tail -f logs/webhook.log

# Background monitor logs
tail -f logs/background_monitor.log
```

### Check Database

```bash
sqlite3 data/conversations.db
```

SQL queries:
```sql
-- Recent messages
SELECT * FROM messages ORDER BY received_at DESC LIMIT 10;

-- AI response stats
SELECT COUNT(*), is_ai_response FROM messages GROUP BY is_ai_response;

-- Pending responses
SELECT * FROM pending_responses WHERE status = 'pending';
```

---

## 🐛 Troubleshooting

### "Configuration errors" on startup

**Solution:** Make sure all required API keys are in `.env` file.

### "Webhook verification failed"

**Solution:** Check that `WEBHOOK_VERIFY_TOKEN` in `.env` matches the token you set in Twilio/Meta console.

### AI not responding after 5 minutes

**Solutions:**
1. Check background monitor is running
2. Check logs: `tail -f logs/background_monitor.log`
3. Verify: `SELECT * FROM pending_responses WHERE status = 'pending';`

### "Failed to send message"

**Solutions:**
1. Check WhatsApp API credentials
2. Verify phone number format
3. Check API balance/billing
4. Review `logs/webhook.log` for errors

### Messages not reaching webhook

**Solutions:**
1. Test webhook URL directly: `curl https://your-url/health`
2. Check ngrok is running (for development)
3. Verify webhook URL in Twilio/Meta console
4. Check firewall settings

---

## 💰 Cost Estimates

### Monthly Costs (100 conversations, 500 messages)

- **WhatsApp API**: $10-20 (Twilio)
- **AI API**: $15-30 (OpenAI GPT-4o-mini)
- **Server**: $6 (DigitalOcean)
- **Total**: ~$31-56/month

### Cost Optimization

1. Use GPT-4o-mini instead of GPT-4 (10x cheaper)
2. Limit AI responses per conversation (MAX_AI_RESPONSES=3)
3. Use template messages for common responses (free on WhatsApp)

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** to git
2. **Use strong webhook verification token**
3. **Enable HTTPS** in production
4. **Rotate API keys** regularly
5. **Monitor logs** for suspicious activity
6. **Backup database** regularly

```bash
# Backup database
cp data/conversations.db data/backup_$(date +%Y%m%d).db
```

---

## 📞 Support & Maintenance

### Daily Tasks
- Review AI responses for quality
- Check error logs

### Weekly Tasks
- Review conversation statistics
- Update AI prompts if needed
- Backup database

### Monthly Tasks
- Review API costs
- Update dependencies: `pip install --upgrade -r requirements.txt`
- Check for system updates

---

## 🎓 Advanced Features

### Add Template Messages

For faster, free responses, create WhatsApp message templates and use them instead of AI for common queries.

### Multi-Language Support

Modify `SYSTEM_PROMPT` to handle multiple languages:
```python
SYSTEM_PROMPT = """
Detect the language of the incoming message and respond in the same language.
Support: Turkish, English, Kurdish, Arabic
"""
```

### Integration with Calendar

Connect to Google Calendar to check actual availability:
```python
# Add in whatsapp_webhook_server.py
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Check calendar availability before confirming appointments
```

### Analytics Dashboard

Create a web dashboard to visualize:
- Response times
- AI vs Human response ratio
- Most common questions
- Conversation trends

---

## 📚 Additional Resources

- [Twilio WhatsApp Docs](https://www.twilio.com/docs/whatsapp)
- [Meta WhatsApp Business API](https://developers.facebook.com/docs/whatsapp)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

---

## ✅ Quick Reference

### Start System
```bash
# Terminal 1
python execution/whatsapp_webhook_server.py

# Terminal 2
python execution/background_monitor.py
```

### Stop System
Press `Ctrl+C` in both terminals

### Check Status
```bash
curl http://localhost:5000/health
curl http://localhost:5000/stats
```

### Test Send Message
```bash
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"phone_number": "+905438247016", "message": "Test"}'
```

---

**🎉 Congratulations! Your WhatsApp AI automation is now set up and running!**

For questions or issues, review the logs in `logs/` directory or check the troubleshooting section above.
