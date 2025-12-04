package com.pablo.projetoBciclo2Pablo;

import org.springframework.amqp.core.Queue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {

    public static final String RESULT_QUEUE_NAME = "provac2Pablo.resultado";

    public static final String QUEUE_NAME = "provac2Pablo";

    @Bean
    public Queue queue() {
        // Fila de entrada (Produtor -> Consumidor)
        return new Queue(QUEUE_NAME, true); // durable = true
    }

    @Bean
    public Queue resultQueue() {
        // Fila de saída (Consumidor -> Outro Serviço)
        return new Queue(RESULT_QUEUE_NAME, true); // durable = true
    }
}
