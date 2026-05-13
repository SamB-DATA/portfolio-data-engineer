from confluent_kafka import Producer
import json
import time
import random
from datetime import datetime

conf = {
    'bootstrap.servers': 'redpanda:9092'
}

producer = Producer(conf)

topic = "client_tickets"

def generate_ticket(ticket_id):
    return {
        "ticket_id": ticket_id,
        "client_id": random.randint(1000, 9999),
        "created_at": datetime.utcnow().isoformat(),
        "request": random.choice([
            "Incident de synchronisation",
            "Bug application mobile",
            "Question sur abonnement"
        ]),
        "request_type": random.choice([
            "support_technique",
            "commercial"
        ]),
        "priority": random.choice([
            "faible",
            "moyenne",
            "haute"
        ])
    }

# 🔥 Attendre que Kafka soit prêt
print("⏳ Attente de Redpanda...")

connected = False
while not connected:
    try:
        producer.list_topics(timeout=5)
        connected = True
        print("✅ Connecté à Redpanda")
    except Exception:
        print("❌ Redpanda pas prêt, retry...")
        time.sleep(2)

# Envoi des messages
ticket_id = 1

while True:
    ticket = generate_ticket(ticket_id)

    producer.produce(
        topic,
        key=str(ticket_id),
        value=json.dumps(ticket)
    )

    producer.flush()

    print(f"📤 Ticket envoyé : {ticket}")

    ticket_id += 1
    time.sleep(2)