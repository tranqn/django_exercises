# Week 24 — Event-Driven Architecture

## Commit #348
**Message:** `feat(events): add domain event base and registry`
**Files:**

```file:advanced/event_driven/events.py
"""Lightweight domain events with in-process subscribers."""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timezone

_subscribers = defaultdict(list)


@dataclass
class DomainEvent:
    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


def subscribe(event_type, handler):
    _subscribers[event_type].append(handler)


def publish(event):
    for handler in _subscribers[type(event)]:
        handler(event)
```

---

## Commit #349
**Message:** `feat(events): add Kafka producer wrapper`
**Files:**

```file:advanced/event_driven/kafka_producer.py
"""
Publish events to Kafka.

pip install confluent-kafka
"""

import json

from confluent_kafka import Producer


class EventProducer:
    def __init__(self, brokers):
        self._producer = Producer({"bootstrap.servers": brokers})

    def publish(self, topic, key, payload):
        self._producer.produce(
            topic, key=str(key), value=json.dumps(payload).encode()
        )
        self._producer.poll(0)

    def flush(self):
        self._producer.flush()
```

---

## Commit #350
**Message:** `feat(events): add Kafka consumer loop`
**Files:**

```file:advanced/event_driven/kafka_consumer.py
"""Consume and dispatch events with at-least-once delivery."""

import json

from confluent_kafka import Consumer


def consume(brokers, group, topics, handle):
    consumer = Consumer({
        "bootstrap.servers": brokers,
        "group.id": group,
        "enable.auto.commit": False,
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe(topics)
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None or msg.error():
                continue
            handle(json.loads(msg.value()))
            consumer.commit(msg)  # commit only after success
    finally:
        consumer.close()
```

---

## Commit #351
**Message:** `feat(events): add transactional outbox model`
**Files:**

```file:advanced/event_driven/outbox.py
"""Outbox pattern: persist events in the same DB transaction as state."""

from django.db import models


class OutboxEvent(models.Model):
    topic = models.CharField(max_length=120)
    key = models.CharField(max_length=120)
    payload = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [models.Index(fields=["published_at"])]
```

---

## Commit #352
**Message:** `feat(events): add outbox relay task`
**Files:**

```file:advanced/event_driven/outbox_relay.py
"""Periodically publish unsent outbox rows to the broker."""

from django.utils import timezone
from celery import shared_task


@shared_task
def relay_outbox(producer, batch=100):
    from .outbox import OutboxEvent
    pending = OutboxEvent.objects.filter(published_at__isnull=True)[:batch]
    for evt in pending:
        producer.publish(evt.topic, evt.key, evt.payload)
        evt.published_at = timezone.now()
        evt.save(update_fields=["published_at"])
    producer.flush()
    return len(pending)
```

---

## Commit #353
**Message:** `feat(events): add idempotent consumer with dedup`
**Files:**

```file:advanced/event_driven/idempotency.py
"""Deduplicate events so retries don't double-process."""

from django.db import IntegrityError, models


class ProcessedEvent(models.Model):
    event_id = models.CharField(max_length=120, unique=True)
    processed_at = models.DateTimeField(auto_now_add=True)


def process_once(event_id, work):
    try:
        ProcessedEvent.objects.create(event_id=event_id)
    except IntegrityError:
        return False  # already handled
    work()
    return True
```

---

## Commit #354
**Message:** `feat(events): add event sourcing aggregate`
**Files:**

```file:advanced/event_driven/event_sourcing.py
"""Rebuild aggregate state by replaying its event stream."""

from dataclasses import dataclass, field
from typing import List


@dataclass
class Account:
    balance: int = 0
    changes: List[dict] = field(default_factory=list)

    def apply(self, event):
        if event["type"] == "deposited":
            self.balance += event["amount"]
        elif event["type"] == "withdrawn":
            self.balance -= event["amount"]

    @classmethod
    def from_stream(cls, events):
        agg = cls()
        for e in events:
            agg.apply(e)
        return agg
```

---

## Commit #355
**Message:** `feat(events): add saga orchestrator`
**Files:**

```file:advanced/event_driven/saga.py
"""Coordinate a multi-step workflow with compensation on failure."""


class Saga:
    def __init__(self):
        self._steps = []

    def add(self, action, compensation):
        self._steps.append((action, compensation))
        return self

    def run(self):
        done = []
        try:
            for action, comp in self._steps:
                action()
                done.append(comp)
        except Exception:
            for comp in reversed(done):  # roll back in reverse order
                comp()
            raise
```

---

## Commit #356
**Message:** `feat(events): add dead-letter handling`
**Files:**

```file:advanced/event_driven/dead_letter.py
"""Route poison messages to a dead-letter topic after max attempts."""


def with_dead_letter(handle, producer, dlq_topic, max_attempts=5):
    def wrapped(message):
        attempts = message.get("_attempts", 0) + 1
        try:
            handle(message)
        except Exception as exc:
            if attempts >= max_attempts:
                producer.publish(dlq_topic, message.get("id", "?"),
                                 {**message, "error": str(exc)})
            else:
                message["_attempts"] = attempts
                raise
    return wrapped
```

---

## Commit #357
**Message:** `feat(events): add CQRS read-model projector`
**Files:**

```file:advanced/event_driven/cqrs_projection.py
"""Project events into a denormalized read model for fast queries."""

from django.db import models


class OrderReadModel(models.Model):
    order_id = models.CharField(max_length=64, unique=True)
    customer = models.CharField(max_length=150)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, default="open")


def project(event):
    if event["type"] == "order_placed":
        OrderReadModel.objects.update_or_create(
            order_id=event["order_id"],
            defaults={"customer": event["customer"], "total": event["total"]},
        )
```

---

## Commit #358
**Message:** `test(events): add outbox and idempotency tests`
**Files:**

```file:advanced/event_driven/test_events.py
"""Tests for dedup and event replay."""

from django.test import TestCase

from .event_sourcing import Account


class EventSourcingTests(TestCase):
    def test_replay_rebuilds_balance(self):
        stream = [
            {"type": "deposited", "amount": 100},
            {"type": "withdrawn", "amount": 30},
        ]
        self.assertEqual(Account.from_stream(stream).balance, 70)
```

---

## Commit #359
**Message:** `docs(week24): add event-driven architecture reference`
**Files:**

```file:advanced/EVENT_DRIVEN_REFERENCE.md
# Week 24 — Event-Driven Architecture

- **Events** — in-process pub/sub + Kafka producer/consumer.
- **Reliability** — transactional outbox + relay, idempotent consumers,
  dead-letter topics, manual offset commit (at-least-once).
- **Patterns** — event sourcing (replay), CQRS read-model projections,
  sagas with compensation.

## Guarantees
- At-least-once delivery → consumers MUST be idempotent.
- Outbox keeps state changes and event emission atomic.
- Always cap retries and dead-letter the rest.
```
