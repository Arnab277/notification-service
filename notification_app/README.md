# Notification Service Assignment

## How to Run
1. First install these:
   ```bash
   pip install flask pika mysql-connector-python
   ```

2. Open 3 separate command windows and run:

   **Window 1** (RabbitMQ):
   ```bash
   rabbitmq-server
   ```

   **Window 2** (Flask API):
   ```bash
   python app.py
   ```

   **Window 3** (Worker):
   ```bash
   python worker.py
   ```

## Testing the API
Send a test notification:
```bash
curl -X POST http://localhost:5000/notifications -H "Content-Type: application/json" -d "{\"user_id\":1,\"message\":\"Test\",\"notification_type\":\"email\"}"
```

Check notifications for user 1:
```bash
curl http://localhost:5000/users/1/notifications
```