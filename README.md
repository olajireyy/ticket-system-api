# 🎟️ Eventure: High-Performance Ticketing API

Eventure is a robust, scalable, and high-performance event ticketing system built with **Django 5.0** and **Django Rest Framework**. It is designed to handle high-concurrency ticket sales, ensuring data integrity while maintaining blazing-fast response times.

---

## 🚀 Key Features

-   **🛡️ Concurrency Protection**: Uses PostgreSQL's `SELECT FOR UPDATE` to prevent overselling tickets during high-traffic events.
-   **⚡ Performance Caching**: Implements **Redis** caching for event listings, reducing database load and speeding up responses.
-   **✉️ Async Notifications**: Leverages **Celery** and **Redis** to send ticket purchase confirmations in the background.
-   **🚦 Smart Throttling**: Protects the API from bots and abuse with custom rate limiting (e.g., 1 purchase per minute per user).
-   **🐳 Fully Dockerized**: Single-command setup for development and deployment using Docker and Docker Compose.

---

## 🛠️ Tech Stack

-   **Backend**: [Django 5.0](https://www.djangoproject.com/) & [Django Rest Framework](https://www.django-rest-framework.org/)
-   **Database**: [PostgreSQL 16](https://www.postgresql.org/)
-   **Cache & Message Broker**: [Redis 7](https://redis.io/)
-   **Task Queue**: [Celery 5.3](https://docs.celeryq.dev/)
-   **Containerization**: [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
-   **Testing**: [Pytest](https://pytest.org/)

---

## 📦 Getting Started

### Prerequisites

-   Docker and Docker Compose installed on your machine.

### Installation & Setup

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/olajireyy/eventure-ticket-system-api
.git
    cd eventure
    ```

2.  **Spin up the infrastructure**:
    ```bash
    docker-compose up --build
    ```
    This command starts the database, Redis, the Django API, and the Celery worker.

3.  **Run Migrations**:
    ```bash
    docker-compose exec web python manage.py migrate
    ```

4.  **Create a Superuser** (optional, for admin access):
    ```bash
    docker-compose exec web python manage.py createsuperuser
    ```

5.  **Access the API**:
    -   API Root: `http://localhost:8000/api/`
    -   Admin Panel: `http://localhost:8000/admin/`

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Features |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/events/` | List all available events | Redis Cached |
| `POST` | `/api/events/<id>/buy/` | Purchase a ticket for an event | Concurrency Lock, Throttled |

### Example: Buying a Ticket
```bash
curl -X POST http://localhost:8000/api/events/1/buy/ \
     -H "Content-Type: application/json" \
     -d '{"email": "buyer@example.com"}'
```

---

## 🧪 Testing

The project uses `pytest` for comprehensive testing, including concurrency checks.

```bash
docker-compose exec web pytest
```

---

## 🧠 Architecture Highlights

### How Concurrency is Handled
To prevent two people from buying the last ticket at the exact same time, Eventure uses database-level locking:
```python
with transaction.atomic():
    locked_event = Event.objects.select_for_update().get(id=self.id)
    if locked_event.available_tickets > 0:
        # Proceed with purchase
```

### Smart Caching Strategy
-   **GET Requests**: The event list is stored in Redis for 5 minutes.
-   **Cache Invalidation**: When a ticket is successfully purchased, the cache is automatically invalidated to ensure users always see accurate availability.

---

## 📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
