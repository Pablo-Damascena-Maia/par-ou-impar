import pika
import json
import time
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

def verificar_par_impar(numero):
    """Verifica se um número é par ou ímpar"""
    if numero % 2 == 0:
        return "PAR"
    else:
        return "ÍMPAR"

def callback_numero(ch, method, properties, body):
    """Callback para processar números recebidos do microserviço A"""
    try:
        # Decodificar mensagem
        mensagem = json.loads(body)
        numero = mensagem['numero']
        timestamp_envio = mensagem['timestamp_envio']
        id_mensagem = mensagem['id_mensagem']
        
        # Verificar se é par ou ímpar
        resultado = verificar_par_impar(numero)
        
        print(f"\n{'='*60}")
        print(f"📥 NÚMERO RECEBIDO")
        print(f"ID: {id_mensagem}")
        print(f"Número: {numero}")
        print(f"Enviado em: {timestamp_envio}")
        print(f"{'='*60}")
        
        print(f"🔍 Processando... Resultado: {resultado}")
        
        # Criar resposta
        resposta = {
            'numero': numero,
            'resultado': resultado,
            'timestamp_resposta': datetime.now().isoformat(),
            'id_mensagem': id_mensagem
        }
        
        # Enviar resposta para fila de respostas
        ch.basic_publish(
            exchange='',
            routing_key='fila_respostas',
            body=json.dumps(resposta),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        
        print(f"📤 Resposta enviada: {resultado}")
        print(f"{'='*60}\n")
        
        # Confirmar processamento
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except json.JSONDecodeError as e:
        print(f"✗ Erro ao decodificar JSON: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    except Exception as e:
        print(f"✗ Erro ao processar mensagem: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def main():
    """Microserviço B - Recebe números e responde par/ímpar"""
    print("="*60)
    print("  MICROSERVIÇO B - CONSUMIDOR")
    print("  Recebe números e responde PAR ou ÍMPAR")
    print("="*60)
    
    # Conectar ao RabbitMQ
    connection = get_rabbitmq_connection()
    channel = connection.channel()
    
    # Fila para receber números do microserviço A
    fila_numeros = 'fila_numeros'
    channel.queue_declare(queue=fila_numeros, durable=True)
    
    # Fila para enviar respostas ao microserviço A
    fila_respostas = 'fila_respostas'
    channel.queue_declare(queue=fila_respostas, durable=True)
    
    print(f"✓ Fila de recebimento: '{fila_numeros}'")
    print(f"✓ Fila de resposta: '{fila_respostas}'")
    
    # Configurar QoS
    channel.basic_qos(prefetch_count=1)
    
    print("\n⏳ Aguardando números do Microserviço A...\n")
    
    # Configurar consumidor
    channel.basic_consume(
        queue=fila_numeros,
        on_message_callback=callback_numero,
        auto_ack=False
    )
    
    try:
        # Iniciar consumo
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n\n✓ Microserviço B encerrado pelo usuário")
        channel.stop_consuming()
    except Exception as e:
        print(f"\n✗ Erro no microserviço B: {e}")
        channel.stop_consuming()
    finally:
        connection.close()
        print("✓ Conexão fechada")

if __name__ == "__main__":
    main()
