import pika
import sys

# Autentikasi RabbitMQ
credentials = pika.PlainCredentials('admin', 'admin123')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()

# Membuat queue yang 'durable' (tidak hilang saat server mati)
channel.queue_declare(queue='task_queue', durable=True)

# Mengambil pesan dari argumen terminal
message = ' '.join(sys.argv[1:]) or "Tugas Standar..."

# Mengirim pesan
channel.basic_publish(
    exchange='',
    routing_key='task_queue',
    body=message,
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE # Pesan disimpan ke disk
    )
)
print(f" [x] Mengirim '{message}'")
connection.close()
