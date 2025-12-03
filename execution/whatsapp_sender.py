"""
WhatsApp Sender - Send messages via WhatsApp Business API
Supports multiple providers: Twilio, Meta, 360Dialog
"""

import requests
from twilio.rest import Client
import config
from typing import Optional

class WhatsAppSender:
    def __init__(self):
        self.provider = config.WHATSAPP_API_PROVIDER

        if self.provider == 'twilio':
            self.client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
            self.from_number = config.TWILIO_WHATSAPP_NUMBER
        elif self.provider == 'meta':
            self.api_key = config.WHATSAPP_API_KEY
            self.phone_number_id = config.WHATSAPP_PHONE_NUMBER_ID
        elif self.provider == '360dialog':
            self.api_key = config.WHATSAPP_API_KEY
        else:
            raise ValueError(f"Unsupported WhatsApp provider: {self.provider}")

    def send_message(self, to_number: str, message: str) -> Optional[str]:
        """
        Send WhatsApp message
        Returns: message_id if successful, None if failed
        """
        try:
            if self.provider == 'twilio':
                return self._send_via_twilio(to_number, message)
            elif self.provider == 'meta':
                return self._send_via_meta(to_number, message)
            elif self.provider == '360dialog':
                return self._send_via_360dialog(to_number, message)
        except Exception as e:
            print(f"Error sending message: {e}")
            return None

    def _send_via_twilio(self, to_number: str, message: str) -> Optional[str]:
        """Send message using Twilio API"""
        try:
            # Ensure number is in WhatsApp format
            if not to_number.startswith('whatsapp:'):
                to_number = f'whatsapp:{to_number}'

            message_obj = self.client.messages.create(
                body=message,
                from_=self.from_number,
                to=to_number
            )

            print(f"✅ Message sent via Twilio: {message_obj.sid}")
            return message_obj.sid

        except Exception as e:
            print(f"❌ Twilio error: {e}")
            return None

    def _send_via_meta(self, to_number: str, message: str) -> Optional[str]:
        """Send message using Meta (Facebook) WhatsApp Business API"""
        try:
            # Remove 'whatsapp:' prefix if present and '+' if present
            clean_number = to_number.replace('whatsapp:', '').replace('+', '')

            url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": clean_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            result = response.json()
            message_id = result.get('messages', [{}])[0].get('id')

            print(f"✅ Message sent via Meta: {message_id}")
            return message_id

        except Exception as e:
            print(f"❌ Meta API error: {e}")
            return None

    def _send_via_360dialog(self, to_number: str, message: str) -> Optional[str]:
        """Send message using 360Dialog API"""
        try:
            # Remove 'whatsapp:' prefix if present
            clean_number = to_number.replace('whatsapp:', '')

            url = "https://waba.360dialog.io/v1/messages"

            headers = {
                "D360-API-KEY": self.api_key,
                "Content-Type": "application/json"
            }

            payload = {
                "to": clean_number,
                "type": "text",
                "text": {
                    "body": message
                }
            }

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            result = response.json()
            message_id = result.get('messages', [{}])[0].get('id')

            print(f"✅ Message sent via 360Dialog: {message_id}")
            return message_id

        except Exception as e:
            print(f"❌ 360Dialog API error: {e}")
            return None

    def send_template_message(self, to_number: str, template_name: str,
                             language_code: str = "tr", components: list = None) -> Optional[str]:
        """
        Send WhatsApp template message (pre-approved messages)
        Useful for notifications and confirmations
        """
        if self.provider != 'meta':
            print("Template messages only supported for Meta provider")
            return None

        try:
            clean_number = to_number.replace('whatsapp:', '').replace('+', '')

            url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }

            payload = {
                "messaging_product": "whatsapp",
                "to": clean_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {
                        "code": language_code
                    }
                }
            }

            if components:
                payload["template"]["components"] = components

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()

            result = response.json()
            message_id = result.get('messages', [{}])[0].get('id')

            print(f"✅ Template message sent: {message_id}")
            return message_id

        except Exception as e:
            print(f"❌ Template message error: {e}")
            return None


def test_sender():
    """Test sending messages"""
    print("Testing WhatsApp Sender...")

    sender = WhatsAppSender()

    # Test message (use your own number for testing)
    test_number = "+905438247016"  # Replace with your test number
    test_message = "Bu bir test mesajıdır. NÖRODİL AI Automation System."

    print(f"\n📤 Sending test message to {test_number}")
    message_id = sender.send_message(test_number, test_message)

    if message_id:
        print(f"✅ Success! Message ID: {message_id}")
    else:
        print("❌ Failed to send message")


if __name__ == '__main__':
    # Uncomment to test (make sure your API credentials are set)
    # test_sender()
    print("WhatsApp Sender module loaded.")
    print(f"Provider: {config.WHATSAPP_API_PROVIDER}")
