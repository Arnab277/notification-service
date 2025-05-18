import pika
import json
import time
import mysql.connector

# Database connection
def get_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='password',
        database='notification_db'
    )

def process_message(ch, method, properties, body):
    data = json.loads(body)
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            print(f"Processing (Attempt {attempt+1}): {data}")
            
            # Store in MySQL
            db = get_db()
            cursor = db.cursor()
            cursor.execute('''
                INSERT INTO notifications 
                (user_id, message, notification_type) 
                VALUES (%s, %s, %s)
            ''', (data['user_id'], data['message'], data['notification_type']))
            db.commit()
            print("✅ Successfully processed")
            break
            
        except Exception as e:
            print(f"❌ Attempt {attempt+1} failed: {e}")
            if attempt == max_retries - 1:
                print("🔥 All retries exhausted")
            time.sleep(2 ** attempt)  # Exponential backoff

# RabbitMQ setup
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='notifications')

print('🚀 Worker ready. Waiting for messages...')
channel.basic_consume(
    queue='notifications',
    on_message_callback=process_message,
    auto_ack=True
)
channel.start_consuming()
