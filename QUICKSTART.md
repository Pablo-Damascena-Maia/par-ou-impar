# Guia de Início Rápido

## 🚀 Executar o Projeto

### Opção 1: Script Automatizado

```bash
./start.sh
```

### Opção 2: Docker Compose

```bash
docker-compose up --build
```

---

## 🔄 Como Funciona

**Comunicação Bidirecional:**

1. **Microserviço A** envia número → **Microserviço B**
2. **Microserviço B** responde "PAR" ou "ÍMPAR" → **Microserviço A**

```
A ──(número)──▶ B
A ◀──(resposta)── B
```

---

## 📊 Acessar Painel RabbitMQ

Abra no navegador:

```
http://localhost:15672
```

**Login:**
- Usuário: `admin`
- Senha: `admin`

**O que ver:**
- Aba **Queues**: Veja as filas `fila_numeros` e `fila_respostas`
- Aba **Connections**: Conexões ativas dos microserviços

---

## 🛑 Parar os Serviços

Pressione `Ctrl + C` no terminal ou execute:

```bash
docker-compose down
```

---

## 📝 O que Você Verá

### Terminal do Microserviço A (Producer)

```
==========================================================
  MICROSERVIÇO A - PRODUTOR
  Envia números e aguarda respostas
==========================================================
✓ Conectado ao RabbitMQ em rabbitmq:5672
✓ Fila de envio: 'fila_numeros'
✓ Fila de resposta: 'fila_respostas'

🚀 Iniciando envio de números...

📤 [1] Enviado: 42 | 2025-12-04T08:33:15.123456

============================================================
📥 RESPOSTA RECEBIDA
ID: 1
Número: 42
Resultado: PAR
Respondido em: 2025-12-04T08:33:15.234567
============================================================
```

### Terminal do Microserviço B (Consumer)

```
==========================================================
  MICROSERVIÇO B - CONSUMIDOR
  Recebe números e responde PAR ou ÍMPAR
==========================================================
✓ Conectado ao RabbitMQ em rabbitmq:5672
✓ Fila de recebimento: 'fila_numeros'
✓ Fila de resposta: 'fila_respostas'

⏳ Aguardando números do Microserviço A...

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

---

## 🧪 Testar Resiliência

### Teste 1: Parar Microserviço B

```bash
# Parar o consumer
docker-compose stop consumer

# Aguardar 30 segundos (mensagens se acumulam na fila_numeros)

# Reiniciar o consumer
docker-compose start consumer

# Observar processamento das mensagens acumuladas
```

### Teste 2: Parar Microserviço A

```bash
# Parar o producer
docker-compose stop producer

# Microserviço B aguardará novas mensagens

# Reiniciar o producer
docker-compose start producer

# Comunicação retomada
```

---

## 🔧 Comandos Úteis

### Ver logs em tempo real

```bash
# Todos os serviços
docker-compose logs -f

# Apenas producer
docker-compose logs -f producer

# Apenas consumer
docker-compose logs -f consumer

# Apenas RabbitMQ
docker-compose logs -f rabbitmq
```

### Reiniciar um serviço

```bash
docker-compose restart producer
docker-compose restart consumer
```

### Ver status dos containers

```bash
docker-compose ps
```

---

## 📚 Documentação Completa

Consulte o arquivo [README.md](README.md) para documentação detalhada sobre:
- Arquitetura completa
- Fluxo de comunicação
- Conceitos aplicados
- Troubleshooting
- Possíveis melhorias
