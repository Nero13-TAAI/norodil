# WhatsApp AI Automation Directive

## Goal
Build an automated AI response system for WhatsApp Business that monitors incoming messages and automatically replies using AI when no human response is given within 5 minutes.

## Business Context
- **Clinic**: NÖRODİL Dil ve Konuşma Merkezi
- **Therapist**: Dkt. Veysi İkvan
- **Phone**: 0543 824 7016
- **Working Hours**: Cumartesi-Pazar 09:00-20:00
- **Use Case**: Automatically handle patient inquiries during busy periods or when therapist is in session

## System Architecture

### Components
1. **WhatsApp Business API** - Receive and send messages
2. **Webhook Server** - Python Flask/FastAPI server to receive webhooks
3. **AI Engine** - OpenAI/Claude API for intelligent responses
4. **Database** - SQLite to track conversations and timing
5. **Background Worker** - Monitor pending messages and trigger AI responses

### Flow
```
Incoming Message → Webhook → Database (mark pending) → Wait 5 minutes
                                                      ↓
                            Manual Reply? → Yes → Mark as handled
                                          ↓ No
                            AI generates response → Send via WhatsApp API
```

## Inputs

### Required API Keys
- **WhatsApp Business API credentials** (Twilio/Meta/360Dialog)
- **AI API key** (OpenAI GPT-4 or Anthropic Claude)
- **Phone number**: 0543 824 7016 (verified with WhatsApp Business API)

### Configuration Variables
- `RESPONSE_DELAY`: 5 minutes (300 seconds)
- `AI_MODEL`: "gpt-4" or "claude-3-sonnet"
- `MAX_AI_RESPONSES_PER_CONVERSATION`: 3 (then require human)
- `BUSINESS_HOURS`: Cumartesi-Pazar 09:00-20:00
- `OUTSIDE_HOURS_IMMEDIATE_RESPONSE`: True

### Context Data for AI
- Business name and services
- Pricing policy (variable, contact via WhatsApp)
- Working hours
- Location
- Treatment areas
- Common FAQs

## Tools/Scripts

### Primary Scripts (in `/execution/`)
1. `whatsapp_webhook_server.py` - Flask server to receive WhatsApp webhooks
2. `ai_responder.py` - AI response generation with context
3. `conversation_tracker.py` - Database management for tracking conversations
4. `background_monitor.py` - Background worker to check pending messages
5. `whatsapp_sender.py` - Send messages via WhatsApp API
6. `config.py` - Configuration management

### Helper Scripts
- `setup_database.py` - Initialize SQLite database
- `test_ai_response.py` - Test AI responses locally
- `webhook_tester.py` - Test webhook locally with ngrok

## Outputs

### AI Response Behavior
- Friendly, professional tone
- Uses clinic context (services, hours, pricing policy)
- Provides accurate information
- Escalates complex medical questions to human
- Includes disclaimer: "Bu otomatik yanıttır. Kısa süre içinde size dönüş yapacağız."

### Message Types Handled
1. **Appointment requests** - Collect info, confirm will schedule
2. **Service inquiries** - Provide information about treatments
3. **Pricing questions** - Explain variable pricing, offer to discuss
4. **Location/hours** - Provide accurate details
5. **General questions** - Answer or escalate to human

### Logging
- All AI responses logged to database
- Conversation history maintained
- Performance metrics tracked

## Edge Cases

### Case 1: Multiple Messages Before 5 Minutes
**Scenario**: Patient sends 3 messages in 2 minutes
**Solution**: Reset 5-minute timer on each new message, wait for last message

### Case 2: Human Replies After AI Already Sent Response
**Scenario**: You reply at 4:59 but AI sends at 5:00
**Solution**: Mark conversation as human-handled, AI stops future auto-responses for this session

### Case 3: AI Already Responded, Patient Replies Again
**Scenario**: AI responded, patient asks follow-up
**Solution**:
- AI can respond up to MAX_AI_RESPONSES_PER_CONVERSATION times
- After that, sends: "Detaylı bilgi için terapistimiz size kısa sürede dönüş yapacak."

### Case 4: Outside Business Hours
**Scenario**: Message received at 22:00 (outside hours)
**Solution**: AI responds immediately with business hours info, takes message

### Case 5: Emergency/Urgent Keywords
**Scenario**: Message contains "acil", "urgent", "emergency"
**Solution**: Immediate notification sent, no AI response, human required

### Case 6: WhatsApp API Rate Limits
**Scenario**: Too many messages sent
**Solution**: Queue messages, implement exponential backoff

### Case 7: AI API Failure
**Scenario**: OpenAI/Claude API down or error
**Solution**: Send fallback message: "Mesajınızı aldık. Size en kısa sürede dönüş yapacağız."

### Case 8: Sensitive Medical Information
**Scenario**: Patient shares medical details
**Solution**: AI responds: "Bu tür bilgileri güvenlik nedeniyle terapi seansımızda görüşmeliyiz."

## Success Criteria
- ✅ AI responds within seconds after 5-minute delay
- ✅ 90%+ of routine questions answered accurately
- ✅ No duplicate responses when human replies
- ✅ Proper escalation of complex cases
- ✅ Professional, on-brand tone
- ✅ Zero downtime during business hours
- ✅ All conversations logged for review

## Monitoring & Maintenance
- Daily: Review AI responses for accuracy
- Weekly: Check conversation logs for patterns
- Monthly: Update AI context with new FAQs
- As needed: Adjust response delay time

## Security Considerations
- WhatsApp API credentials stored in `.env` (not committed)
- Patient data encrypted in database
- HIPAA/KVKK compliance for medical information
- No storage of sensitive medical details
- API keys rotated regularly

## Cost Estimates
- **WhatsApp Business API**: $0.005-0.04 per message (varies by provider)
- **AI API**: $0.03-0.10 per conversation (GPT-4/Claude)
- **Hosting**: $5-20/month (DigitalOcean/Heroku)
- **Estimated monthly**: $50-150 (depends on message volume)

## Implementation Phases

### Phase 1: Foundation (Day 1)
- Set up WhatsApp Business API
- Create webhook server
- Database schema
- Basic message receiving

### Phase 2: AI Integration (Day 2)
- AI prompt engineering with clinic context
- Response generation
- Testing with sample conversations

### Phase 3: Automation Logic (Day 3)
- 5-minute delay logic
- Background monitoring worker
- Human override detection

### Phase 4: Testing & Deployment (Day 4)
- Test all edge cases
- Deploy to cloud server
- Monitor initial conversations
- Fine-tune AI responses

### Phase 5: Optimization (Ongoing)
- Collect feedback
- Improve AI prompts
- Add new FAQs to context
- Performance optimization

## Rollback Plan
If AI responses are problematic:
1. Disable automated responses (keep manual mode)
2. Review conversation logs
3. Fix AI prompt/logic
4. Test thoroughly
5. Re-enable with monitoring

## Notes
- Start with conservative AI responses (less automation)
- Gradually increase AI autonomy as accuracy improves
- Always allow human override
- Patient satisfaction is priority #1