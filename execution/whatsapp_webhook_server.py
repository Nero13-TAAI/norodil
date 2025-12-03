"""
WhatsApp Webhook Server - Flask server to receive WhatsApp messages
Handles incoming webhooks from WhatsApp Business API providers
"""

from flask import Flask, request, jsonify
import config
from conversation_tracker import ConversationTracker
from ai_responder import AIResponder
from whatsapp_sender import WhatsAppSender
import logging
from datetime import datetime

# Initialize Flask app
app = Flask(__name__)

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/webhook.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize components
tracker = ConversationTracker(config.DATABASE_PATH)
ai_responder = AIResponder()
whatsapp_sender = WhatsAppSender()


@app.route('/webhook', methods=['GET'])
def verify_webhook():
    """
    Webhook verification for WhatsApp Business API
    Required by Meta/360Dialog to verify your webhook URL
    """
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')

    if mode == 'subscribe' and token == config.WEBHOOK_VERIFY_TOKEN:
        logger.info("Webhook verified successfully")
        return challenge, 200
    else:
        logger.warning("Webhook verification failed")
        return 'Verification failed', 403


@app.route('/webhook', methods=['POST'])
def handle_webhook():
    """
    Handle incoming WhatsApp messages
    Processes messages from all supported providers
    """
    try:
        data = request.get_json()
        logger.info(f"Received webhook: {data}")

        # Route to appropriate handler based on provider
        if config.WHATSAPP_API_PROVIDER == 'twilio':
            return handle_twilio_webhook(data)
        elif config.WHATSAPP_API_PROVIDER == 'meta':
            return handle_meta_webhook(data)
        elif config.WHATSAPP_API_PROVIDER == '360dialog':
            return handle_360dialog_webhook(data)
        else:
            logger.error(f"Unknown provider: {config.WHATSAPP_API_PROVIDER}")
            return jsonify({"error": "Unknown provider"}), 400

    except Exception as e:
        logger.error(f"Error handling webhook: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def handle_twilio_webhook(data):
    """Handle Twilio webhook format"""
    try:
        # Extract message details from Twilio format
        from_number = request.form.get('From', '').replace('whatsapp:', '')
        message_text = request.form.get('Body', '')
        message_id = request.form.get('MessageSid', '')

        if not from_number or not message_text:
            return jsonify({"error": "Missing required fields"}), 400

        process_incoming_message(from_number, message_text, message_id)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.error(f"Twilio webhook error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def handle_meta_webhook(data):
    """Handle Meta (Facebook) webhook format"""
    try:
        # Extract message from Meta's nested structure
        entry = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        messages = value.get('messages', [])

        if not messages:
            # This might be a status update, not a message
            return jsonify({"status": "no_message"}), 200

        message = messages[0]
        from_number = message.get('from', '')
        message_text = message.get('text', {}).get('body', '')
        message_id = message.get('id', '')

        if not from_number or not message_text:
            return jsonify({"error": "Missing required fields"}), 400

        # Add + for international format
        if not from_number.startswith('+'):
            from_number = '+' + from_number

        process_incoming_message(from_number, message_text, message_id)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.error(f"Meta webhook error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def handle_360dialog_webhook(data):
    """Handle 360Dialog webhook format"""
    try:
        # Similar to Meta format but with some differences
        messages = data.get('messages', [])

        if not messages:
            return jsonify({"status": "no_message"}), 200

        message = messages[0]
        from_number = message.get('from', '')
        message_text = message.get('text', {}).get('body', '')
        message_id = message.get('id', '')

        if not from_number or not message_text:
            return jsonify({"error": "Missing required fields"}), 400

        process_incoming_message(from_number, message_text, message_id)

        return jsonify({"status": "success"}), 200

    except Exception as e:
        logger.error(f"360Dialog webhook error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


def process_incoming_message(phone_number: str, message_text: str, message_id: str):
    """
    Process incoming message and decide on response strategy
    """
    logger.info(f"Processing message from {phone_number}: {message_text}")

    # Add message to database
    msg_db_id = tracker.add_incoming_message(phone_number, message_text, message_id)
    conversation_id = tracker.get_or_create_conversation(phone_number)

    # Check for emergency keywords
    if config.contains_emergency_keyword(message_text):
        logger.warning(f"Emergency keyword detected in message from {phone_number}")
        response = ai_responder.generate_emergency_response()
        send_response(phone_number, response, is_ai=True)
        # TODO: Send notification to therapist
        return

    # Check if outside business hours
    if not config.is_business_hours() and config.IMMEDIATE_RESPONSE_OUTSIDE_HOURS:
        logger.info("Outside business hours - sending immediate response")
        response = ai_responder.generate_outside_hours_response(message_text)
        send_response(phone_number, response, is_ai=True)
        return

    # Schedule AI response after delay
    logger.info(f"Scheduling AI response for message {msg_db_id} after {config.RESPONSE_DELAY}s")
    tracker.schedule_ai_response(msg_db_id, delay_seconds=config.RESPONSE_DELAY)


def send_response(phone_number: str, message: str, is_ai: bool = False):
    """Send a response via WhatsApp"""
    try:
        message_id = whatsapp_sender.send_message(phone_number, message)

        if message_id:
            # Log the outgoing message
            tracker.add_outgoing_message(phone_number, message, is_ai=is_ai, message_id=message_id)
            logger.info(f"Response sent to {phone_number}: {message_id}")
        else:
            logger.error(f"Failed to send response to {phone_number}")

    except Exception as e:
        logger.error(f"Error sending response: {e}", exc_info=True)


@app.route('/send', methods=['POST'])
def manual_send():
    """
    API endpoint to manually send messages (for testing or admin use)
    """
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        message = data.get('message')

        if not phone_number or not message:
            return jsonify({"error": "phone_number and message required"}), 400

        message_id = whatsapp_sender.send_message(phone_number, message)

        if message_id:
            tracker.add_outgoing_message(phone_number, message, is_ai=False, message_id=message_id)
            return jsonify({"status": "success", "message_id": message_id}), 200
        else:
            return jsonify({"error": "Failed to send"}), 500

    except Exception as e:
        logger.error(f"Manual send error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/stats', methods=['GET'])
def get_stats():
    """Get system statistics"""
    try:
        stats = tracker.get_statistics()
        stats['is_business_hours'] = config.is_business_hours()
        stats['response_delay'] = config.RESPONSE_DELAY
        return jsonify(stats), 200
    except Exception as e:
        logger.error(f"Stats error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "provider": config.WHATSAPP_API_PROVIDER,
        "ai_provider": config.AI_PROVIDER
    }), 200


if __name__ == '__main__':
    # Create logs directory
    import os
    os.makedirs('logs', exist_ok=True)

    logger.info("Starting WhatsApp Webhook Server...")
    logger.info(f"Provider: {config.WHATSAPP_API_PROVIDER}")
    logger.info(f"AI Provider: {config.AI_PROVIDER}")
    logger.info(f"Response Delay: {config.RESPONSE_DELAY}s")

    # Validate configuration
    try:
        config.validate_config()
        logger.info("✅ Configuration validated")
    except ValueError as e:
        logger.error(f"❌ Configuration error: {e}")
        exit(1)

    # Start server
    app.run(
        host=config.FLASK_HOST,
        port=config.FLASK_PORT,
        debug=config.FLASK_DEBUG
    )
