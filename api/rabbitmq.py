import pika
import dotenv
import os
def get_rabbit_connection():
    dotenv.load_dotenv()

    HOST = os.getenv("RABBIT_HOST")
    PORT = os.getenv("RABBIT_PORT")
    USERNAME = os.getenv("RABBIT_USERNAME")
    PASSWORD = os.getenv("RABBIT_PASSWORD")
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=HOST,
            port=PORT,
            credentials=pika.PlainCredentials(USERNAME, PASSWORD)
        )
    )

def get_rabbit_channel(connection):
    return connection.channel()



def send_message_rabbit(message):
    dotenv.load_dotenv()

    QUEUE = os.getenv("RABBIT_QUEUE")
    # отправка сообщения в RabbitMQ
    connection = get_rabbit_connection()
    channel = get_rabbit_channel(connection)
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE,
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )
    connection.close()


def write_rabbit_to_env_file(host, port, username, password, queue):

    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    if not dotenv_file:
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'), "w") as env_file:
            env_file.write("# .env file\n")
        dotenv_file = dotenv.find_dotenv()
        dotenv.load_dotenv(dotenv_file)



    variables = {
        'RABBIT_HOST': host,
        'RABBIT_PORT': port,
        'RABBIT_USERNAME': username,
        'RABBIT_PASSWORD': password,
        'RABBIT_QUEUE': queue,
    }

    for key, value in variables.items():
        os.environ[key] = value
        dotenv.set_key(dotenv_file, key, os.environ[key])

    print(f"Конфигурация RabbitMQ записана в .env")
