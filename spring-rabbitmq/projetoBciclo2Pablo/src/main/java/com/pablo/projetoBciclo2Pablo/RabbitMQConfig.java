package com.pablo.projetoBciclo2Pablo;

import org.springframework.amqp.core.Queue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {

    // Fila única de comunicação (entrada e saída)

    public static final String QUEUE_NAME = "provac2Pablo.resultado";

    @Bean
    public Queue queue() {
        // Fila única de comunicação
        return new Queue(QUEUE_NAME, true); // durable = true
    }
}
