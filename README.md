## Deployment on AWS

This project is deployed on an AWS EC2 instance using Docker containers.
Access the application via the public IP and port: http://51.20.185.234:8000/.

All required ports are open in the EC2 Security Group, and Django is configured to allow connections from this IP.

## Full Docker workflow

### 1. Clone the repository
```sh
git clone git@github.com:yurakomarnitskyi/synergyway-task.git
cd synergyway-task
```

### 2. Build and start all containers
```sh
docker-compose up --build
```
This will start:
- Django (web)
- Celery worker
- Celery beat
- PostgreSQL
- Redis

### 3. Access the API
- Main API: http://localhost:8000/

#### How to test all API endpoints (full paths):
- List users: `GET http://localhost:8000/api/users/`
- Retrieve user: `GET http://localhost:8000/api/users/<id>/`
- List addresses: `GET http://localhost:8000/api/addresses/`
- Retrieve address: `GET http://localhost:8000/api/addresses/<id>/`
- List credit cards: `GET http://localhost:8000/api/creditcards/`
- Retrieve credit card: `GET http://localhost:8000/api/creditcards/<id>/`

You can test these endpoints using curl, httpie, Postman, or your browser (for GET requests).

> **Note:** All containers (web, db, redis, celery, celery-beat) must be running for the following commands.

### 4. Run tests
```sh
docker-compose exec web pytest app/user/tests.py
```

### 5. Lint code 
```sh
docker-compose exec web ruff check .
```
### 6. Lint and auto-fix code
```sh
docker-compose exec web ruff check . --fix
```

### 7. Format code
```sh
docker-compose exec web ruff format .
```

### 8. Stop all containers
```sh
docker-compose down
```

---

## Project logic
- Users, addresses, and credit cards are added automatically via Celery tasks.
- Data is fetched from jsonplaceholder and mockaroo APIs.
- All services (Django, Celery, DB, Redis) are managed by docker-compose.

---

## Requirements
- Docker, docker-compose

---

## Author
Yura Komarnitskyi

---

## Celery Beat schedule examples
- Every hour: `crontab(minute=0)`

Example usage in `app/app/celerybeat_schedule.py`:
```python
beat_schedule = {
    'fetch-next-user': {
        'task': 'user.tasks.fetch_and_save_next_user',
        'schedule': crontab(minute='*/15'),  # change to '*/30' or 0 as needed
    },
}
```
