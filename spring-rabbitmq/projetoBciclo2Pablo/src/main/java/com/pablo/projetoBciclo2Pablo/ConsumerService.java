package com.pablo.projetoBciclo2Pablo;

import org.springframework.amqp.rabbit.annotation.RabbitListener;

import org.springframework.stereotype.Service;

import java.time.LocalDateTime;

@Service
public class ConsumerService {

    // Não precisa mais do RabbitTemplate injetado, pois não há reenvio.
    // O Consumidor apenas consome e processa.

    @RabbitListener(queues = RabbitMQConfig.QUEUE_NAME)
    public void receiveMessage(String message) {
        System.out.println("==================================================");
        System.out.println("  MENSAGEM RECEBIDA");
        System.out.println("==================================================");
        System.out.println("  Timestamp Recebimento: " + LocalDateTime.now());
        System.out.println("  Fila: " + RabbitMQConfig.QUEUE_NAME);
        System.out.println("  Conteúdo: " + message);
        
        try {
            // Simulação de processamento: verificar se o número é par ou ímpar
            // Nota: Em um cenário real, você faria o parsing do JSON para obter o número.
            // Aqui, apenas verificamos se a mensagem contém um número para simular.
            
            // Exemplo de parsing simples (requer biblioteca JSON, mas para fins de demonstração):
            int startIndex = message.indexOf("\"numero\":") + 9;
            int endIndex = message.indexOf(",", startIndex);
            if (endIndex == -1) {
                endIndex = message.indexOf("}", startIndex);
            }
            
            String numeroStr = message.substring(startIndex, endIndex).trim();
            int numero = Integer.parseInt(numeroStr);
            
            String resultado = (numero % 2 == 0) ? "PAR" : "ÍMPAR";
            
            System.out.println("  Número Processado: " + numero);
            System.out.println("  Resultado: " + resultado);
            
        } catch (Exception e) {
            System.err.println("  Erro ao processar mensagem: " + e.getMessage());
        }
        
        System.out.println("==================================================");
    }
}
