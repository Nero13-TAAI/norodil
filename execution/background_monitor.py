"""
Background Monitor - Continuously checks for pending AI responses
Sends automated responses when delay period has elapsed
"""

import time
import logging
from datetime import datetime
import config
from conversation_tracker import ConversationTracker
from ai_responder import AIResponder
from whatsapp_sender import WhatsAppSender

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/background_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class BackgroundMonitor:
    def __init__(self):
        self.tracker = ConversationTracker(config.DATABASE_PATH)
        self.ai_responder = AIResponder()
        self.whatsapp_sender = WhatsAppSender()
        self.running = False

    def start(self, check_interval=30):
        """
        Start monitoring for pending responses
        check_interval: How often to check (in seconds)
        """
        self.running = True
        logger.info("🚀 Background monitor started")
        logger.info(f"Check interval: {check_interval}s")
        logger.info(f"Response delay: {config.RESPONSE_DELAY}s")

        try:
            while self.running:
                self.process_pending_responses()
                time.sleep(check_interval)

        except KeyboardInterrupt:
            logger.info("Monitor stopped by user")
            self.stop()
        except Exception as e:
            logger.error(f"Monitor error: {e}", exc_info=True)
            self.stop()

    def stop(self):
        """Stop the monitor"""
        self.running = False
        logger.info("Background monitor stopped")

    def process_pending_responses(self):
        """Check for and process pending responses"""
        try:
            # Get all pending responses that are due
            pending = self.tracker.get_pending_responses()

            if not pending:
                logger.debug("No pending responses")
                return

            logger.info(f"Found {len(pending)} pending response(s)")

            for item in pending:
                self.handle_pending_response(item)

        except Exception as e:
            logger.error(f"Error processing pending responses: {e}", exc_info=True)

    def handle_pending_response(self, pending_item: dict):
        """Handle a single pending response"""
        try:
            pending_id = pending_item['id']
            message_id = pending_item['message_id']
            conversation_id = pending_item['conversation_id']
            phone_number = pending_item['phone_number']
            message_text = pending_item['message_text']

            logger.info(f"Processing pending response {pending_id} for {phone_number}")

            # Check if human has already responded
            # Get the last message from this conversation
            history = self.tracker.get_conversation_history(phone_number, limit=5)

            # Check if there's any outgoing message after this incoming message
            incoming_time = pending_item['received_at']
            for msg in history:
                if msg['direction'] == 'outgoing' and msg['received_at'] > incoming_time:
                    # Human already responded, cancel AI response
                    logger.info(f"Human already responded, cancelling AI response {pending_id}")
                    self.tracker.mark_pending_as_processed(pending_id, status='cancelled')
                    return

            # Generate AI response
            logger.info(f"Generating AI response for message: {message_text[:50]}...")
            response_text = self.ai_responder.generate_response(
                phone_number=phone_number,
                message_text=message_text,
                conversation_id=conversation_id,
                message_id=message_id
            )

            if not response_text:
                logger.error(f"Failed to generate response for pending {pending_id}")
                self.tracker.mark_pending_as_processed(pending_id, status='failed')
                return

            # Send the response
            logger.info(f"Sending AI response to {phone_number}")
            sent_message_id = self.whatsapp_sender.send_message(phone_number, response_text)

            if sent_message_id:
                # Log as sent successfully
                self.tracker.add_outgoing_message(
                    phone_number=phone_number,
                    message_text=response_text,
                    is_ai=True,
                    message_id=sent_message_id
                )
                self.tracker.mark_pending_as_processed(pending_id, status='sent')
                logger.info(f"✅ AI response sent successfully: {sent_message_id}")
            else:
                logger.error(f"Failed to send AI response for pending {pending_id}")
                self.tracker.mark_pending_as_processed(pending_id, status='failed')

        except Exception as e:
            logger.error(f"Error handling pending response: {e}", exc_info=True)
            try:
                self.tracker.mark_pending_as_processed(pending_id, status='error')
            except:
                pass

    def get_status(self):
        """Get monitor status"""
        stats = self.tracker.get_statistics()
        return {
            "running": self.running,
            "timestamp": datetime.now().isoformat(),
            "is_business_hours": config.is_business_hours(),
            **stats
        }


def main():
    """Main function to run the monitor"""
    logger.info("=" * 60)
    logger.info("WhatsApp AI Automation - Background Monitor")
    logger.info(f"Business: {config.BUSINESS_INFO['name']}")
    logger.info(f"WhatsApp Provider: {config.WHATSAPP_API_PROVIDER}")
    logger.info(f"AI Provider: {config.AI_PROVIDER}")
    logger.info("=" * 60)

    # Validate configuration
    try:
        config.validate_config()
        logger.info("✅ Configuration validated")
    except ValueError as e:
        logger.error(f"❌ Configuration error:\n{e}")
        return

    # Create logs directory
    import os
    os.makedirs('logs', exist_ok=True)

    # Start monitor
    monitor = BackgroundMonitor()

    try:
        monitor.start(check_interval=30)  # Check every 30 seconds
    except KeyboardInterrupt:
        logger.info("\nShutting down gracefully...")
        monitor.stop()


if __name__ == '__main__':
    main()
