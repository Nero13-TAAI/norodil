# WhatsApp AI Automation System
## Complete Project Overview

---

## 🎯 What Was Built

A fully automated WhatsApp response system that:

1. **Receives** incoming WhatsApp messages via webhook
2. **Waits 5 minutes** to give you time to reply manually
3. **Generates intelligent AI responses** using GPT-4 or Claude
4. **Sends automated replies** if you haven't responded
5. **Tracks everything** in a database for monitoring

---

## 📁 Project Structure

```
clinic/
├── 📄 index.html                    # Your clinic website
├── 📄 styles.css                    # Website styling
├── 📄 script.js                     # Website interactivity
├── 📄 logo.jpg                      # Your clinic logo
│
├── 📂 directives/                   # SOPs and instructions
│   └── whatsapp_ai_automation.md   # Complete automation directive
│
├── 📂 execution/                    # Core Python scripts
│   ├── config.py                   # Configuration management
│   ├── conversation_tracker.py     # Database operations
│   ├── ai_responder.py             # AI response generation
│   ├── whatsapp_sender.py          # Send WhatsApp messages
│   ├── whatsapp_webhook_server.py  # Receive webhooks (Flask)
│   ├── background_monitor.py       # Monitor pending responses
│   └── setup_database.py           # Initialize database
│
├── 📄 requirements.txt              # Python dependencies
├── 📄 .env.example                  # Environment variables template
├── 📄 .gitignore                    # Git ignore rules
├── 📄 start.bat                     # Windows startup script
│
├── 📖 AI-AUTOMATION-SETUP.md       # Complete setup guide
├── 📖 QUICK-START.md               # 15-minute quick start
├── 📖 whatsapp-business-setup.md   # WhatsApp Business config
├── 📄 quick-replies-reference.txt  # Quick replies for manual use
│
├── 📂 data/                         # Database (created on first run)
│   └── conversations.db
│
└── 📂 logs/                         # Log files (created on first run)
    ├── webhook.log
    └── background_monitor.log
```

---

## 🔧 Core Components

### 1. Configuration System (`config.py`)
- Manages all settings and API credentials
- Business context for AI responses
- Working hours and emergency keywords
- Validates configuration on startup

### 2. Database Tracker (`conversation_tracker.py`)
- SQLite database for all conversations
- Tracks pending responses
- Logs AI interactions
- Provides statistics

### 3. AI Responder (`ai_responder.py`)
- Generates intelligent responses
- Supports OpenAI and Anthropic
- Uses conversation history for context
- Handles special cases (emergency, outside hours)

### 4. WhatsApp Integration
- **Sender** (`whatsapp_sender.py`): Sends messages via API
- **Webhook Server** (`whatsapp_webhook_server.py`): Receives incoming messages
- Supports Twilio, Meta, and 360Dialog

### 5. Background Monitor (`background_monitor.py`)
- Checks every 30 seconds for pending responses
- Sends AI responses after delay period
- Prevents duplicate responses if human replied

---

## 🌊 How It Works (Flow)

```
1. Patient sends WhatsApp message
   ↓
2. Webhook receives message → Saves to database
   ↓
3. Schedule AI response (5 minutes delay)
   ↓
4. [5 MINUTE WAIT]
   ↓
5. Background Monitor checks:
   - Did human respond? → Yes: Cancel AI
   - Still pending? → Generate AI response
   ↓
6. AI generates contextual response
   ↓
7. Send via WhatsApp API
   ↓
8. Log everything to database
```

---

## 🎮 Usage

### Start the System

**Windows:**
```bash
start.bat
```

**Manual:**
```bash
# Terminal 1 - Webhook Server
python execution/whatsapp_webhook_server.py

# Terminal 2 - Background Monitor
python execution/background_monitor.py
```

### Override AI Response
Just reply manually within 5 minutes - AI won't send.

### View Statistics
```bash
curl http://localhost:5000/stats
```

### Check Logs
```bash
tail -f logs/webhook.log
tail -f logs/background_monitor.log
```

---

## ⚙️ Configuration Options

Edit `.env` file:

```env
# Change response delay
RESPONSE_DELAY=300  # seconds (default: 5 minutes)

# Max AI responses before escalation
MAX_AI_RESPONSES=3  # default: 3

# AI model
AI_MODEL=gpt-4o-mini  # gpt-4o, gpt-4o-mini, claude-3-sonnet

# Auto-respond outside hours
IMMEDIATE_OUTSIDE_HOURS=True
```

---

## 🎯 Smart Features

### 1. **Context-Aware Responses**
AI knows about:
- Your clinic services
- Pricing policy
- Working hours
- Location
- Previous conversation

### 2. **Intelligent Escalation**
- Limits AI to 3 responses per conversation
- After 3 AI messages → escalates to human
- Detects emergency keywords → immediate notification

### 3. **Outside Hours Handling**
- Automatically responds outside business hours
- Informs patients of working hours
- Takes message for callback

### 4. **Human Priority**
- Always checks if human replied first
- Cancels AI response if human answered
- Never sends duplicate responses

### 5. **Conversation Tracking**
- Complete message history
- AI response logging
- Cost tracking
- Performance metrics

---

## 📊 Database Schema

**conversations**
- Track customer conversations
- Store contact info
- Conversation status

**messages**
- All incoming and outgoing messages
- Timestamps and metadata
- AI vs human responses

**ai_responses**
- AI generation logs
- Token usage and costs
- Error tracking

**pending_responses**
- Scheduled AI responses
- Processing status
- Delay management

---

## 💡 Example AI Responses

**Appointment Request:**
```
Merhaba! Randevu talebiniz için teşekkür ederiz 📅

Aşağıdaki bilgileri paylaşır mısınız?
- Adınız ve soyadınız
- Yaşınız (veya çocuğunuzun yaşı)
- Hangi konuda destek almak istersiniz?
- Tercih ettiğiniz gün ve saat

Bu otomatik yanıttır. Dkt. Veysi İkvan size kısa sürede dönüş yapacaktır.
```

**Pricing Question:**
```
Seans ücretlerimiz, danışanın ihtiyacına ve tedavi planına göre değişmektedir.

Size özel ücret bilgisi için terapi ihtiyacınızı ve yaşınızı paylaşırsanız, detaylı bilgi verebiliriz.

Bu otomatik yanıttır. Dkt. Veysi İkvan size kısa sürede dönüş yapacaktır.
```

**Outside Hours:**
```
Merhaba! 👋

Mesajınız için teşekkür ederiz. Şu anda mesai saatleri dışındayız.

📅 Çalışma Saatlerimiz:
Cumartesi-Pazar: 09:00 - 20:00

Mesajınızı aldık ve çalışma saatlerimiz içinde size dönüş yapacağız.

İyi günler dileriz! 🌟
```

---

## 🔒 Security Features

1. **Webhook Verification Token**
   - Prevents unauthorized webhook calls
   - Validates incoming requests

2. **Environment Variables**
   - API keys never in code
   - .gitignore prevents commits

3. **Rate Limiting**
   - Prevents API abuse
   - Configurable limits

4. **Encryption**
   - Secure API communication
   - HTTPS in production

5. **Logging**
   - Complete audit trail
   - Error tracking

---

## 💰 Cost Breakdown

**Initial Setup:** Free (development)

**Monthly Operation (100 conversations):**
- WhatsApp API: $10-20
- AI API: $15-30
- Server: $6
- **Total: ~$31-56/month**

**Cost Optimization:**
- Use GPT-4o-mini (10x cheaper than GPT-4)
- Limit AI responses per conversation
- Use templates for common questions

---

## 📈 Monitoring & Analytics

### Built-in Statistics
- Total conversations
- Message counts
- AI vs human response ratio
- Token usage
- Cost estimates

### Logs
- All incoming/outgoing messages
- AI generation details
- Error tracking
- Performance metrics

### Database Queries
```sql
-- Recent conversations
SELECT * FROM messages ORDER BY received_at DESC LIMIT 20;

-- AI performance
SELECT
  COUNT(*) as total,
  AVG(tokens_used) as avg_tokens
FROM ai_responses;

-- Response times
SELECT
  AVG(julianday(human_responded_at) - julianday(received_at)) * 24 * 60 as avg_minutes
FROM messages
WHERE human_responded_at IS NOT NULL;
```

---

## 🚀 Deployment Options

### Development (Local + ngrok)
- Use ngrok to expose localhost
- Perfect for testing
- Free

### Production Options

**1. DigitalOcean ($6/month)**
- Simple droplet
- Supervisor for process management
- Recommended for beginners

**2. Heroku ($7/month)**
- Easy deployment
- Automatic scaling
- Built-in monitoring

**3. AWS/GCP**
- More complex
- Better for scale
- Variable pricing

---

## 🎓 Advanced Customization

### 1. Modify AI Behavior
Edit `execution/config.py` → `SYSTEM_PROMPT`

### 2. Add Custom Logic
Edit `execution/whatsapp_webhook_server.py` → `process_incoming_message()`

### 3. Custom Emergency Keywords
Edit `.env`:
```env
EMERGENCY_KEYWORDS=acil,urgent,emergency,help
```

### 4. Multi-Language Support
Update system prompt to handle multiple languages

### 5. Integration with Other Systems
- Google Calendar for appointments
- CRM systems
- Payment gateways
- Email notifications

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **QUICK-START.md** | 15-minute setup guide |
| **AI-AUTOMATION-SETUP.md** | Complete setup & deployment |
| **whatsapp-business-setup.md** | WhatsApp Business features |
| **quick-replies-reference.txt** | Manual quick replies |
| **directives/whatsapp_ai_automation.md** | Technical directive (SOP) |
| **PROJECT-OVERVIEW.md** | This file - system overview |

---

## ✅ Testing Checklist

Before going live:

- [ ] Configuration validated (`python config.py`)
- [ ] Database initialized (`python setup_database.py`)
- [ ] Webhook server starts without errors
- [ ] Background monitor starts without errors
- [ ] Test message received in webhook
- [ ] AI response generated successfully
- [ ] Response sent via WhatsApp API
- [ ] 5-minute delay works correctly
- [ ] Manual reply cancels AI response
- [ ] Emergency keywords detected
- [ ] Outside hours response works
- [ ] Statistics endpoint accessible
- [ ] Logs being written correctly

---

## 🎯 Key Success Metrics

**Technical:**
- 100% uptime during business hours
- <1s webhook response time
- <5s AI response generation
- 0 duplicate responses

**Business:**
- 90%+ patient satisfaction with AI responses
- 50%+ reduction in response time
- Increased engagement
- More appointment bookings

---

## 🛠️ Maintenance Schedule

**Daily:**
- Review AI responses for accuracy
- Check error logs

**Weekly:**
- Review conversation statistics
- Backup database
- Update AI prompts if needed

**Monthly:**
- Review API costs
- Update dependencies
- System health check
- Performance optimization

---

## 📞 Support

**Troubleshooting:**
1. Check logs in `logs/` directory
2. Review error messages
3. Consult documentation
4. Test individual components

**Common Issues:**
- Configuration errors → Check `.env`
- Database errors → Run `setup_database.py`
- Webhook issues → Verify URL in provider console
- AI errors → Check API key and balance

---

## 🎉 Summary

You now have:

✅ Professional clinic website
✅ WhatsApp Business setup guide
✅ Complete AI automation system
✅ Intelligent 5-minute delay logic
✅ Context-aware AI responses
✅ Comprehensive logging and monitoring
✅ Production-ready deployment guide
✅ Full documentation

**Next Steps:**
1. Follow QUICK-START.md to set up
2. Test with your WhatsApp number
3. Deploy to production server
4. Monitor and optimize

---

**Built with care for NÖRODİL Dil ve Konuşma Merkezi** 💙

System ready to handle patient inquiries 24/7 while maintaining your personal touch!
