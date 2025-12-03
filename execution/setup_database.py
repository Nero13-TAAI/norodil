"""
Setup Database - Initialize the SQLite database
Run this script once to create the database structure
"""

import os
import sys
from conversation_tracker import ConversationTracker
import config

def setup_database():
    """Initialize the database"""
    print("=" * 60)
    print("WhatsApp AI Automation - Database Setup")
    print("=" * 60)

    # Ensure data directory exists
    db_dir = os.path.dirname(config.DATABASE_PATH)
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
        print(f"✅ Created directory: {db_dir}")

    # Initialize database
    print(f"\nInitializing database: {config.DATABASE_PATH}")
    tracker = ConversationTracker(config.DATABASE_PATH)

    print("\n✅ Database initialized successfully!")
    print("\nDatabase structure created:")
    print("  - conversations: Track customer conversations")
    print("  - messages: Store all incoming and outgoing messages")
    print("  - ai_responses: Log AI response generation")
    print("  - pending_responses: Manage delayed responses")

    # Get statistics
    stats = tracker.get_statistics()
    print(f"\nDatabase statistics:")
    print(f"  - Total conversations: {stats['total_conversations']}")
    print(f"  - Total messages: {stats['total_messages']}")
    print(f"  - AI responses: {stats['ai_responses']}")
    print(f"  - Human responses: {stats['human_responses']}")

    print("\n" + "=" * 60)
    print("Setup complete! You can now start the webhook server.")
    print("=" * 60)


if __name__ == '__main__':
    try:
        setup_database()
    except Exception as e:
        print(f"\n❌ Error setting up database: {e}")
        sys.exit(1)
