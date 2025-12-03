"""
AI Responder - Generate intelligent responses using OpenAI or Anthropic
Handles context, conversation history, and response generation
"""

import os
from typing import List, Dict, Optional
import openai
from anthropic import Anthropic
import config
from conversation_tracker import ConversationTracker

class AIResponder:
    def __init__(self):
        self.provider = config.AI_PROVIDER
        self.model = config.AI_MODEL
        self.tracker = ConversationTracker(config.DATABASE_PATH)

        if self.provider == 'openai':
            openai.api_key = config.OPENAI_API_KEY
            self.client = openai.OpenAI()
        elif self.provider == 'anthropic':
            self.client = Anthropic(api_key=config.ANTHROPIC_API_KEY)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def _build_conversation_history(self, phone_number: str) -> List[Dict]:
        """Build conversation history for context"""
        history = self.tracker.get_conversation_history(phone_number, limit=10)

        messages = []
        for msg in history:
            role = "assistant" if msg['direction'] == 'outgoing' else "user"
            messages.append({
                "role": role,
                "content": msg['message_text']
            })

        return messages

    def _generate_response_openai(self, messages: List[Dict]) -> tuple[str, int]:
        """Generate response using OpenAI"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": config.SYSTEM_PROMPT},
                    *messages
                ],
                temperature=0.7,
                max_tokens=500
            )

            content = response.choices[0].message.content
            tokens = response.usage.total_tokens

            return content, tokens

        except Exception as e:
            print(f"OpenAI API error: {e}")
            raise

    def _generate_response_anthropic(self, messages: List[Dict]) -> tuple[str, int]:
        """Generate response using Anthropic Claude"""
        try:
            # Convert messages to Claude format
            claude_messages = []
            for msg in messages:
                if msg['role'] != 'system':
                    claude_messages.append({
                        "role": msg['role'],
                        "content": msg['content']
                    })

            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                system=config.SYSTEM_PROMPT,
                messages=claude_messages
            )

            content = response.content[0].text
            tokens = response.usage.input_tokens + response.usage.output_tokens

            return content, tokens

        except Exception as e:
            print(f"Anthropic API error: {e}")
            raise

    def generate_response(self, phone_number: str, message_text: str,
                         conversation_id: int, message_id: int) -> Optional[str]:
        """Generate AI response for a message"""

        # Check if we've exceeded max AI responses for this conversation
        ai_count = self.tracker.get_ai_response_count(conversation_id)
        if ai_count >= config.MAX_AI_RESPONSES_PER_CONVERSATION:
            escalation_message = (
                f"Mesajınız için teşekkür ederiz! 🙏\n\n"
                f"Detaylı bilgi ve yardım için {config.BUSINESS_INFO['therapist']} "
                f"size çok kısa sürede dönüş yapacaktır.\n\n"
                f"Acil durumlar için: {config.BUSINESS_INFO['phone']}"
            )
            return escalation_message

        # Build conversation history
        history = self._build_conversation_history(phone_number)

        # Add current message
        history.append({
            "role": "user",
            "content": message_text
        })

        try:
            # Generate response based on provider
            if self.provider == 'openai':
                response_text, tokens = self._generate_response_openai(history)
            elif self.provider == 'anthropic':
                response_text, tokens = self._generate_response_anthropic(history)
            else:
                raise ValueError(f"Unsupported provider: {self.provider}")

            # Log the AI response
            self.tracker.log_ai_response(
                conversation_id=conversation_id,
                message_id=message_id,
                prompt=message_text,
                response=response_text,
                model=self.model,
                tokens_used=tokens,
                was_sent=True
            )

            return response_text

        except Exception as e:
            print(f"Error generating AI response: {e}")

            # Log the error
            self.tracker.log_ai_response(
                conversation_id=conversation_id,
                message_id=message_id,
                prompt=message_text,
                response="",
                model=self.model,
                was_sent=False,
                error=str(e)
            )

            # Return fallback message
            fallback = (
                f"Mesajınızı aldık! 📩\n\n"
                f"{config.BUSINESS_INFO['therapist']} size en kısa sürede "
                f"dönüş yapacaktır.\n\n"
                f"Acil durumlar için: {config.BUSINESS_INFO['phone']}"
            )
            return fallback

    def generate_outside_hours_response(self, message_text: str) -> str:
        """Generate automatic response for outside business hours"""
        return (
            f"Merhaba! 👋\n\n"
            f"Mesajınız için teşekkür ederiz. Şu anda mesai saatleri dışındayız.\n\n"
            f"📅 Çalışma Saatlerimiz:\n{config.BUSINESS_INFO['working_hours']}\n\n"
            f"Mesajınızı aldık ve çalışma saatlerimiz içinde size dönüş yapacağız.\n\n"
            f"Acil durumlar için: {config.BUSINESS_INFO['phone']}\n\n"
            f"İyi günler dileriz! 🌟\n\n"
            f"{config.BUSINESS_INFO['name']}"
        )

    def generate_emergency_response(self) -> str:
        """Generate response for emergency keywords"""
        return (
            f"⚠️ Acil durumunuz için üzgünüz.\n\n"
            f"Lütfen hemen şu numaradan arayın:\n"
            f"📞 {config.BUSINESS_INFO['phone']}\n\n"
            f"Veya acil sağlık hizmetleri için 112'yi arayabilirsiniz."
        )


def test_ai_responder():
    """Test the AI responder"""
    print("Testing AI Responder...")

    responder = AIResponder()

    # Test messages
    test_messages = [
        "Merhaba, randevu almak istiyorum",
        "Ücretler ne kadar?",
        "Çocuğum 3 yaşında ve henüz konuşmuyor",
        "Kekemelik tedavisi yapıyor musunuz?"
    ]

    for msg in test_messages:
        print(f"\n📩 Input: {msg}")
        try:
            response = responder._generate_response_openai([
                {"role": "user", "content": msg}
            ])
            print(f"🤖 Response: {response[0]}")
            print(f"📊 Tokens: {response[1]}")
        except Exception as e:
            print(f"❌ Error: {e}")

    # Test outside hours response
    print("\n⏰ Outside Hours Response:")
    print(responder.generate_outside_hours_response("Test message"))

    # Test emergency response
    print("\n⚠️ Emergency Response:")
    print(responder.generate_emergency_response())


if __name__ == '__main__':
    test_ai_responder()
