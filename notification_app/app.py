from flask import Flask, jsonify, request
import pika
import json

app = Flask(__name__)

# RabbitMQ connection
def get_rabbit_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='notifications')
    return channel

@app.route('/notifications', methods=['POST'])
def send_notification():
    data = request.get_json()
    
    # Validation
    if not all(k in data for k in ['user_id', 'message', 'notification_type']):
        return jsonify({"error": "Missing fields"}), 400
    
    if data['notification_type'] not in ['email', 'sms', 'in_app']:
        return jsonify({"error": "Invalid type"}), 400
    
    # Send to RabbitMQ
    try:
        channel = get_rabbit_channel()
        channel.basic_publish(
            exchange='',
            routing_key='notifications',
            body=json.dumps(data)
        )
        return jsonify({"status": "queued", "id": data.get('user_id')}), 202
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)