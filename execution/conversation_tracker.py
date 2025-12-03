"""
Conversation Tracker - Database management for WhatsApp conversations
Tracks message history, response status, and AI interaction metadata
"""

import sqlite3
import os
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import json

class ConversationTracker:
    def __init__(self, db_path='data/conversations.db'):
        self.db_path = db_path
        self._ensure_database_exists()

    def _ensure_database_exists(self):
        """Create database directory and file if they don't exist"""
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Create conversations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone_number TEXT NOT NULL,
                customer_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_message_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                notes TEXT,
                UNIQUE(phone_number)
            )
        ''')

        # Create messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                direction TEXT NOT NULL,
                message_text TEXT,
                message_id TEXT UNIQUE,
                received_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_ai_response BOOLEAN DEFAULT 0,
                ai_response_sent_at TIMESTAMP,
                human_response_pending BOOLEAN DEFAULT 1,
                human_responded_at TIMESTAMP,
                metadata TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        ''')

        # Create ai_responses table for tracking AI usage
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                conversation_id INTEGER NOT NULL,
                message_id INTEGER NOT NULL,
                prompt TEXT,
                response TEXT,
                model TEXT,
                tokens_used INTEGER,
                cost_estimate REAL,
                generated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                was_sent BOOLEAN DEFAULT 0,
                error TEXT,
                FOREIGN KEY (conversation_id) REFERENCES conversations(id),
                FOREIGN KEY (message_id) REFERENCES messages(id)
            )
        ''')

        # Create pending_responses table for delayed responses
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pending_responses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message_id INTEGER NOT NULL,
                conversation_id INTEGER NOT NULL,
                scheduled_for TIMESTAMP NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'pending',
                processed_at TIMESTAMP,
                FOREIGN KEY (message_id) REFERENCES messages(id),
                FOREIGN KEY (conversation_id) REFERENCES conversations(id)
            )
        ''')

        # Create indexes for performance
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_messages_received ON messages(received_at)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_pending_scheduled ON pending_responses(scheduled_for, status)')

        conn.commit()
        conn.close()

    def get_or_create_conversation(self, phone_number: str, customer_name: Optional[str] = None) -> int:
        """Get existing conversation or create new one"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('SELECT id FROM conversations WHERE phone_number = ?', (phone_number,))
        result = cursor.fetchone()

        if result:
            conversation_id = result[0]
            # Update last message time
            cursor.execute('UPDATE conversations SET last_message_at = ? WHERE id = ?',
                         (datetime.now(), conversation_id))
        else:
            cursor.execute('''
                INSERT INTO conversations (phone_number, customer_name, created_at, last_message_at)
                VALUES (?, ?, ?, ?)
            ''', (phone_number, customer_name, datetime.now(), datetime.now()))
            conversation_id = cursor.lastrowid

        conn.commit()
        conn.close()
        return conversation_id

    def add_incoming_message(self, phone_number: str, message_text: str,
                            message_id: str, metadata: Optional[Dict] = None) -> int:
        """Record an incoming message from customer"""
        conversation_id = self.get_or_create_conversation(phone_number)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO messages
            (conversation_id, direction, message_text, message_id, received_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (conversation_id, 'incoming', message_text, message_id, datetime.now(),
              json.dumps(metadata) if metadata else None))

        message_db_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return message_db_id

    def add_outgoing_message(self, phone_number: str, message_text: str,
                            is_ai: bool = False, message_id: Optional[str] = None) -> int:
        """Record an outgoing message (human or AI)"""
        conversation_id = self.get_or_create_conversation(phone_number)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO messages
            (conversation_id, direction, message_text, message_id, received_at,
             is_ai_response, human_response_pending)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (conversation_id, 'outgoing', message_text, message_id, datetime.now(),
              is_ai, False))

        message_db_id = cursor.lastrowid

        # Mark all pending messages in this conversation as human-responded
        if not is_ai:
            cursor.execute('''
                UPDATE messages
                SET human_response_pending = 0, human_responded_at = ?
                WHERE conversation_id = ? AND human_response_pending = 1
            ''', (datetime.now(), conversation_id))

            # Cancel any pending AI responses
            cursor.execute('''
                UPDATE pending_responses
                SET status = 'cancelled', processed_at = ?
                WHERE conversation_id = ? AND status = 'pending'
            ''', (datetime.now(), conversation_id))

        conn.commit()
        conn.close()

        return message_db_id

    def schedule_ai_response(self, message_id: int, delay_seconds: int = 300) -> int:
        """Schedule an AI response for a message after delay"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get conversation_id for this message
        cursor.execute('SELECT conversation_id FROM messages WHERE id = ?', (message_id,))
        result = cursor.fetchone()
        if not result:
            conn.close()
            raise ValueError(f"Message {message_id} not found")

        conversation_id = result[0]
        scheduled_for = datetime.now() + timedelta(seconds=delay_seconds)

        cursor.execute('''
            INSERT INTO pending_responses (message_id, conversation_id, scheduled_for)
            VALUES (?, ?, ?)
        ''', (message_id, conversation_id, scheduled_for))

        pending_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return pending_id

    def get_pending_responses(self) -> List[Dict]:
        """Get all pending responses that are due"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT pr.*, m.message_text, c.phone_number
            FROM pending_responses pr
            JOIN messages m ON pr.message_id = m.id
            JOIN conversations c ON pr.conversation_id = c.id
            WHERE pr.status = 'pending'
            AND pr.scheduled_for <= ?
        ''', (datetime.now(),))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return results

    def mark_pending_as_processed(self, pending_id: int, status: str = 'sent'):
        """Mark a pending response as processed"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE pending_responses
            SET status = ?, processed_at = ?
            WHERE id = ?
        ''', (status, datetime.now(), pending_id))

        conn.commit()
        conn.close()

    def get_ai_response_count(self, conversation_id: int) -> int:
        """Get number of AI responses sent in a conversation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT COUNT(*) FROM messages
            WHERE conversation_id = ? AND is_ai_response = 1 AND direction = 'outgoing'
        ''', (conversation_id,))

        count = cursor.fetchone()[0]
        conn.close()

        return count

    def get_conversation_history(self, phone_number: str, limit: int = 10) -> List[Dict]:
        """Get recent message history for a conversation"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('''
            SELECT m.* FROM messages m
            JOIN conversations c ON m.conversation_id = c.id
            WHERE c.phone_number = ?
            ORDER BY m.received_at DESC
            LIMIT ?
        ''', (phone_number, limit))

        results = [dict(row) for row in cursor.fetchall()]
        conn.close()

        return results[::-1]  # Reverse to get chronological order

    def log_ai_response(self, conversation_id: int, message_id: int,
                       prompt: str, response: str, model: str,
                       tokens_used: int = 0, was_sent: bool = True,
                       error: Optional[str] = None):
        """Log AI response generation for monitoring"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Rough cost estimate (update based on actual pricing)
        cost_per_1k_tokens = 0.002 if 'gpt-4' in model else 0.0005
        cost_estimate = (tokens_used / 1000) * cost_per_1k_tokens

        cursor.execute('''
            INSERT INTO ai_responses
            (conversation_id, message_id, prompt, response, model,
             tokens_used, cost_estimate, was_sent, error)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (conversation_id, message_id, prompt, response, model,
              tokens_used, cost_estimate, was_sent, error))

        conn.commit()
        conn.close()

    def get_statistics(self) -> Dict:
        """Get usage statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        stats = {}

        # Total conversations
        cursor.execute('SELECT COUNT(*) FROM conversations')
        stats['total_conversations'] = cursor.fetchone()[0]

        # Total messages
        cursor.execute('SELECT COUNT(*) FROM messages')
        stats['total_messages'] = cursor.fetchone()[0]

        # AI responses sent
        cursor.execute('SELECT COUNT(*) FROM messages WHERE is_ai_response = 1')
        stats['ai_responses'] = cursor.fetchone()[0]

        # Human responses
        cursor.execute('SELECT COUNT(*) FROM messages WHERE is_ai_response = 0 AND direction = "outgoing"')
        stats['human_responses'] = cursor.fetchone()[0]

        # Pending responses
        cursor.execute('SELECT COUNT(*) FROM pending_responses WHERE status = "pending"')
        stats['pending_responses'] = cursor.fetchone()[0]

        # Total AI cost estimate
        cursor.execute('SELECT SUM(cost_estimate) FROM ai_responses')
        result = cursor.fetchone()[0]
        stats['total_ai_cost'] = result if result else 0.0

        conn.close()
        return stats

    def is_conversation_active(self, phone_number: str) -> bool:
        """Check if conversation has recent activity"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
            SELECT last_message_at FROM conversations
            WHERE phone_number = ?
        ''', (phone_number,))

        result = cursor.fetchone()
        conn.close()

        if not result:
            return False

        last_message = datetime.fromisoformat(result[0])
        # Consider conversation active if last message was within 24 hours
        return (datetime.now() - last_message).total_seconds() < 86400


if __name__ == '__main__':
    # Test the database
    print("Testing ConversationTracker...")

    tracker = ConversationTracker('data/test_conversations.db')

    # Test adding messages
    test_phone = '+905551234567'
    msg_id = tracker.add_incoming_message(test_phone, 'Merhaba, randevu almak istiyorum', 'msg_001')
    print(f"Added incoming message with ID: {msg_id}")

    # Schedule AI response
    pending_id = tracker.schedule_ai_response(msg_id, delay_seconds=300)
    print(f"Scheduled AI response with ID: {pending_id}")

    # Get statistics
    stats = tracker.get_statistics()
    print(f"\nStatistics: {stats}")

    print("\n✅ Database tests passed!")
