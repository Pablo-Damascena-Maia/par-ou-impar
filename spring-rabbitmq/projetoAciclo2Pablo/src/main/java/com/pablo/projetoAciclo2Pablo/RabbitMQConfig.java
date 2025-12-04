package com.pablo.projetoAciclo2Pablo;

import org.springframework.amqp.core.Queue;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class RabbitMQConfig {

    public static final String QUEUE_NAME = "provac2Pablo.resultado";

    @Bean
    public Queue queue() {
        // A fila será criada no RabbitMQ se ainda não existir
        return new Queue(QUEUE_NAME, true); // durable = true
    }
}
