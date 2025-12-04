package com.pablo.projetoAciclo2Pablo;

import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Random;

@Service
public class ProducerService {

    private final RabbitTemplate rabbitTemplate;

    @Autowired
    public ProducerService(RabbitTemplate rabbitTemplate) {
        this.rabbitTemplate = rabbitTemplate;
    }

    public String sendMessage() {
        // 1. Gera um número aleatório
        int numero = new Random().nextInt(1000) + 1;
        
        // 2. Cria a mensagem
        String mensagem = String.format(
                "{\"numero\": %d, \"timestamp\": \"%s\"}",
                numero,
                LocalDateTime.now().toString()
        );

        // 3. Envia a mensagem para a fila
        rabbitTemplate.convertAndSend(RabbitMQConfig.QUEUE_NAME, mensagem);
        
        String log = String.format("Mensagem enviada para a fila '%s': %s", RabbitMQConfig.QUEUE_NAME, mensagem);
        System.out.println(log);
        
        return log;
    }
}
