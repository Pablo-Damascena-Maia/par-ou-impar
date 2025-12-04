# Projeto Ciclo 2 - Pablo Maia

## Verificador de Números Par/Ímpar com Microserviços e RabbitMQ

Este projeto implementa uma arquitetura de microserviços com **comunicação bidirecional** utilizando **RabbitMQ** como sistema de mensageria para verificação de números pares e ímpares.

---

## 📋 Descrição do Projeto

O sistema é composto por **dois microserviços** que se comunicam através de filas do RabbitMQ com **comunicação bidirecional**:

1. **Microserviço A (Producer)**: Gera números aleatórios, envia para o Microserviço B e aguarda respostas
2. **Microserviço B (Consumer)**: Recebe números, verifica se são pares ou ímpares, e **envia a resposta de volta** para o Microserviço A

---

## 🏗️ Arquitetura

```
┌─────────────────────┐                    ┌─────────────────────┐
│                     │                    │                     │
│  MICROSERVIÇO A     │                    │  MICROSERVIÇO B     │
│  (Producer)         │                    │  (Consumer)         │
│                     │                    │                     │
│  - Gera números     │                    │  - Recebe números   │
│  - Envia para B     │                    │  - Verifica par/    │
│  - Recebe respostas │                    │    ímpar            │
│                     │                    │  - Envia resposta   │
└─────────────────────┘                    └─────────────────────┘
         │                                           │
         │  1. Envia número                          │
         │─────────────────────────────────────────▶ │
         │         (fila_numeros)                    │
         │                                           │
         │                                           │
         │  2. Responde "PAR" ou "ÍMPAR"             │
         │ ◀─────────────────────────────────────────│
         │         (fila_respostas)                  │
         │                                           │
         ▼                                           ▼
    ┌────────────────────────────────────────────────────┐
    │              RABBITMQ MESSAGE BROKER               │
    │  - fila_numeros: A → B                            │
    │  - fila_respostas: B → A                          │
    └────────────────────────────────────────────────────┘
```

---

## 🔄 Fluxo de Comunicação

1. **Microserviço A** gera um número aleatório (1-1000)
2. **Microserviço A** envia o número para a fila `fila_numeros`
3. **Microserviço B** consome o número da fila `fila_numeros`
4. **Microserviço B** verifica se o número é PAR ou ÍMPAR
5. **Microserviço B** envia a resposta para a fila `fila_respostas`
6. **Microserviço A** recebe e exibe a resposta
7. O ciclo se repete a cada 5 segundos

---

## 🛠️ Tecnologias Utilizadas

- **Python 3.11**: Linguagem de programação
- **RabbitMQ 3**: Sistema de mensageria (message broker)
- **Pika 1.3.2**: Biblioteca Python para RabbitMQ
- **Docker**: Containerização dos serviços
- **Docker Compose**: Orquestração dos containers

---

## 📁 Estrutura do Projeto

```
projetociclo2PabloMaia/
├── producer/
│   ├── producer.py          # Microserviço A (envia e recebe)
│   ├── requirements.txt     # Dependências Python
│   └── Dockerfile          # Imagem Docker
├── consumer/
│   ├── consumer.py          # Microserviço B (recebe e responde)
│   ├── requirements.txt     # Dependências Python
│   └── Dockerfile          # Imagem Docker
├── docker-compose.yml       # Orquestração dos serviços
├── start.sh                # Script de inicialização
├── QUICKSTART.md           # Guia rápido
├── README.md               # Documentação completa
└── .gitignore             # Arquivos ignorados pelo Git
```

---

## 🚀 Como Executar o Projeto

### Pré-requisitos

- Docker instalado ([Instalar Docker](https://docs.docker.com/get-docker/))
- Docker Compose instalado ([Instalar Docker Compose](https://docs.docker.com/compose/install/))

### Passo 1: Clonar o Repositório

```bash
git clone https://github.com/Pablo-Damascena-Maia/par-ou-impar.git
cd par-ou-impar
```

### Passo 2: Iniciar os Serviços

**Opção 1: Usando script**
```bash
./start.sh
```

**Opção 2: Usando Docker Compose**
```bash
docker-compose up --build
```

### Passo 3: Visualizar a Comunicação

Você verá nos logs:

**Terminal do Microserviço A:**
```
📤 [1] Enviado: 42 | 2025-12-04T08:33:15.123456

============================================================
📥 RESPOSTA RECEBIDA
ID: 1
Número: 42
Resultado: PAR
Respondido em: 2025-12-04T08:33:15.234567
============================================================
```

**Terminal do Microserviço B:**
```
============================================================
📥 NÚMERO RECEBIDO
ID: 1
Número: 42
Enviado em: 2025-12-04T08:33:15.123456
============================================================
🔍 Processando... Resultado: PAR
📤 Resposta enviada: PAR
============================================================
```

### Passo 4: Acessar o Painel do RabbitMQ

Acesse o painel de gerenciamento em:

```
http://localhost:15672
```

**Credenciais:**
- Usuário: `admin`
- Senha: `admin`

No painel você pode visualizar:
- As duas filas: `fila_numeros` e `fila_respostas`
- Taxa de mensagens por segundo
- Mensagens em processamento

---

## 🔧 Configuração

### Variáveis de Ambiente

Configuradas no `docker-compose.yml`:

| Variável | Descrição | Valor Padrão |
|----------|-----------|--------------|
| `RABBITMQ_HOST` | Host do RabbitMQ | `rabbitmq` |
| `RABBITMQ_PORT` | Porta do RabbitMQ | `5672` |
| `RABBITMQ_USER` | Usuário do RabbitMQ | `admin` |
| `RABBITMQ_PASS` | Senha do RabbitMQ | `admin` |

### Portas Expostas

| Serviço | Porta | Descrição |
|---------|-------|-----------|
| RabbitMQ | 5672 | Porta AMQP para comunicação |
| RabbitMQ Management | 15672 | Interface web de gerenciamento |

---

## 📊 Funcionamento Detalhado

### Microserviço A (Producer)

**Responsabilidades:**
1. Gerar números aleatórios entre 1 e 1000
2. Enviar números para a fila `fila_numeros`
3. Aguardar e processar respostas da fila `fila_respostas`
4. Exibir resultados recebidos

**Mensagem enviada:**
```json
{
  "numero": 42,
  "timestamp_envio": "2025-12-04T08:33:15.123456",
  "id_mensagem": 1
}
```

**Intervalo de envio:** 5 segundos

### Microserviço B (Consumer)

**Responsabilidades:**
1. Consumir números da fila `fila_numeros`
2. Verificar se o número é PAR ou ÍMPAR (usando operador `%`)
3. Enviar resposta para a fila `fila_respostas`
4. Confirmar processamento (ACK)

**Mensagem de resposta:**
```json
{
  "numero": 42,
  "resultado": "PAR",
  "timestamp_resposta": "2025-12-04T08:33:15.234567",
  "id_mensagem": 1
}
```

---

## 🧪 Testando o Sistema

### Teste 1: Verificar Comunicação Completa

Após iniciar os serviços, observe:
- Microserviço A enviando números
- Microserviço B processando e respondendo
- Microserviço A recebendo respostas

### Teste 2: Monitorar Filas no RabbitMQ

1. Acesse http://localhost:15672
2. Vá em **Queues**
3. Observe as duas filas:
   - `fila_numeros`: Mensagens de A para B
   - `fila_respostas`: Mensagens de B para A

### Teste 3: Testar Resiliência

**Cenário 1: Parar Microserviço B**
```bash
docker-compose stop consumer
```
- Números se acumularão na `fila_numeros`
- Ao reiniciar, todos serão processados

**Cenário 2: Parar Microserviço A**
```bash
docker-compose stop producer
```
- Microserviço B aguardará novas mensagens
- Ao reiniciar A, comunicação será retomada

---

## 🛑 Parar os Serviços

**Parar serviços:**
```bash
docker-compose down
```

**Parar e remover volumes:**
```bash
docker-compose down -v
```

**Parar apenas um serviço:**
```bash
docker-compose stop producer
# ou
docker-compose stop consumer
```

---

## 📝 Conceitos Aplicados

### Comunicação Bidirecional
- Fluxo completo de requisição-resposta
- Duas filas independentes para cada direção
- Rastreamento de mensagens por ID

### RabbitMQ
- **Filas persistentes**: Mensagens sobrevivem a reinicializações
- **Confirmação manual (ACK)**: Garante processamento confiável
- **QoS (Quality of Service)**: Controla carga de trabalho
- **Message Broker**: Desacopla produtores e consumidores

### Microserviços
- **Desacoplamento**: Serviços independentes
- **Escalabilidade**: Possível escalar cada serviço separadamente
- **Resiliência**: Falhas isoladas não derrubam o sistema
- **Single Responsibility**: Cada serviço tem uma função específica

### Docker
- **Containerização**: Ambientes isolados e reproduzíveis
- **Orquestração**: Docker Compose gerencia múltiplos containers
- **Networking**: Comunicação entre containers via rede bridge

---

## 🔍 Troubleshooting

### Problema: Serviços não conectam ao RabbitMQ

**Causa:** RabbitMQ ainda está inicializando

**Solução:** Os microserviços têm retry automático (10 tentativas). Aguarde alguns segundos.

### Problema: Porta 5672 ou 15672 já em uso

**Solução:** Altere as portas no `docker-compose.yml`:

```yaml
ports:
  - "5673:5672"
  - "15673:15672"
```

### Problema: Mensagens não estão sendo processadas

**Solução:** Verifique os logs:

```bash
docker-compose logs producer
docker-compose logs consumer
docker-compose logs rabbitmq
```

### Problema: Docker Compose não encontrado

**Solução:** Instale o Docker Compose:

```bash
# Linux
sudo apt-get install docker-compose

# Mac/Windows
# Já vem incluído no Docker Desktop
```

---

## 📈 Possíveis Melhorias

- [ ] Adicionar persistência de resultados em banco de dados
- [ ] Implementar interface web para visualização
- [ ] Adicionar métricas e monitoramento (Prometheus/Grafana)
- [ ] Implementar testes automatizados
- [ ] Adicionar autenticação e segurança
- [ ] Escalar horizontalmente os microserviços
- [ ] Implementar dead letter queue para mensagens com erro

---

## 📚 Referências

- [RabbitMQ Documentation](https://www.rabbitmq.com/documentation.html)
- [RabbitMQ Tutorials](https://www.rabbitmq.com/getstarted.html)
- [Pika Documentation](https://pika.readthedocs.io/)
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)

---

## 👨‍💻 Autor

**Pablo Damascena Maia**

---

## 📄 Licença

Este projeto é de uso educacional.
