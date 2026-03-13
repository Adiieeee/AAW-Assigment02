import pika
import time

# Autentikasi RabbitMQ
credentials = pika.PlainCredentials('admin', 'admin123')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', credentials=credentials)
)
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Menunggu tugas. Tekan CTRL+C untuk keluar')

def callback(ch, method, properties, body):
    pesan = body.decode()
    print(f" [x] Menerima {pesan}")

    # Simulasi beban kerja: delay 1 detik untuk setiap titik (.)
    waktu_kerja = pesan.count('.')
    time.sleep(waktu_kerja)

    print(f" [x] Tugas '{pesan}' Selesai dikerjakan")
    # Konfirmasi (acknowledgment) bahwa tugas selesai
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Fair dispatch: Jangan beri tugas baru sebelum tugas lama selesai
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()
