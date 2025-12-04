import pika
import json
import time
import random
import os
from datetime import datetime

def get_rabbitmq_connection():
    """Estabelece conexão com RabbitMQ com retry"""
    rabbitmq_host = os.getenv('RABBITMQ_HOST', 'localhost')
    rabbitmq_port = int(os.getenv('RABBITMQ_PORT', 5672))
    rabbitmq_user = os.getenv('RABBITMQ_USER', 'admin')
    rabbitmq_pass = os.getenv('RABBITMQ_PASS', 'admin')
    
    max_retries = 10
    retry_delay = 5
    
    for attempt in range(max_retries):
        try:
            credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_pass)
            parameters = pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                credentials=credentials,
                heartbeat=600,
                blocked_connection_timeout=300
            )
            connection = pika.BlockingConnection(parameters)
            print(f"✓ Conectado ao RabbitMQ em {rabbitmq_host}:{rabbitmq_port}")
            return connection
        except Exception as e:
            print(f"Tentativa {attempt + 1}/{max_retries} falhou: {e}")
            if attempt < max_retries - 1:
                print(f"Aguardando {retry_delay} segundos antes de tentar novamente...")
                time.sleep(retry_delay)
            else:
                raise

def callback_resposta(ch, method, properties, body):
    """Callback para receber respostas do consumidor"""
    try:
        resposta = json.loads(body)
        numero = resposta['numero']
        resultado = resposta['resultado']
        timestamp_resposta = resposta['timestamp_resposta']
        id_mensagem = resposta['id_mensagem']
        
        print(f"\n{'='*60}")
        print(f"📥 RESPOSTA RECEBIDA")
        print(f"ID: {id_mensagem}")
        print(f"Número: {numero}")
        print(f"Resultado: {resultado}")
        print(f"Respondido em: {timestamp_resposta}")
        print(f"{'='*60}\n")
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"✗ Erro ao processar resposta: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def main():
    """Microserviço A - Envia números e recebe respostas"""
    print("="*60)
    print("  MICROSERVIÇO A - PRODUTOR")
    print("  Envia números e aguarda respostas")
    print("="*60)
    
    # Conectar ao RabbitMQ
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    
    # Fila para enviar números ao microserviço B
    fila_envio = 'fila_numeros'
    channel.queue_declare(queue=fila_envio, durable=True)
    
    # Fila para receber respostas do microserviço B
    fila_resposta = 'fila_respostas'
    channel.queue_declare(queue=fila_resposta, durable=True)
    
    print(f"✓ Fila de envio: '{fila_envio}'")
    print(f"✓ Fila de resposta: '{fila_resposta}'")
    
    # Configurar consumidor para respostas
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue=fila_resposta,
        on_message_callback=callback_resposta,
        auto_ack=False
    )
    
    print("\n🚀 Iniciando envio de números...\n")
    
    contador = 0
    
    def enviar_numero():
        """Envia um número para o microserviço B"""
        nonlocal contador
        contador += 1
        
        # Gerar número aleatório
        numero = random.randint(1, 1000)
        
        # Criar mensagem
        mensagem = {
            'numero': numero,
            'timestamp_envio': datetime.now().isoformat(),
            'id_mensagem': contador
        }
        
        # Publicar na fila de envio
        channel.basic_publish(
            exchange='',
            routing_key=fila_envio,
            body=json.dumps(mensagem),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        
        print(f"📤 [{contador}] Enviado: {numero} | {mensagem['timestamp_envio']}")
    
    try:
        # Loop principal
        last_send_time = 0
        send_interval = 5  # Enviar a cada 5 segundos
        
        while True:
            # Processar respostas pendentes
            connection.process_data_events(time_limit=1)
            
            # Enviar novo número se passou o intervalo
            current_time = time.time()
            if current_time - last_send_time >= send_interval:
                enviar_numero()
                last_send_time = current_time
            
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\n\n✓ Microserviço A encerrado pelo usuário")
    except Exception as e:
        print(f"\n✗ Erro no microserviço A: {e}")
    finally:
        connection.close()
        print("✓ Conexão fechada")

if __name__ == "__main__":
    main()
