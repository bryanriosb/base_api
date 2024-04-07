# drifti
ERP to small providers

## Characteristics
- Django REST Framework
- PostgreSQL
- Django Tenants (To SaaS architecture from schemas)
- Django Channel (Websocket)
- Celery (Workers to asynchronously tasks)
- Celery Beat (Periodic tasks to workers)
- Docker & Docker Compose

## Development
At this point, docker and docker compose must be installed.

Being at the root of the project directory.
```bash
  export COMPOSE_FILE=docker-compose.dev.yml
  docker compose up -d
```

### Database connection
In this point you can to connect to drifti database with same environment credentials.
Note: Docker compose change database port to 6433.
```text
Host: localhost
Port: 6433
Database Name: drifti
Database User: development
Database Password: XXXXXXX
```

### Configure Tenant Migrations to Shared Apps
Using django-tenants to configure tenant schemas.
```bash
docker compose run --rm django python manage.py makemigrations
```
```bash
docker compose run --rm django python manage.py migrate_schemas --shared
```

### Activate Python Console Ipython
```bash
docker compose run --rm django ipython
```

### Create tenant public
```python
import os;os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drifti.config.dev");import django;django.setup();from apps.customers.models import Client, Domain;tenant = Client(schema_name='public',name='Drifti',paid_until='2030-12-31',on_trial=False);tenant.save();domain = Domain(domain='localhost',tenant=tenant,is_primary=True);domain.save()
```

### Create Super User
```bash
docker compose run --rm django python manage.py create_tenant_superuser --schema=public --username=admin --email=admin@drifti.com
```

### Create Demo tenant
Only tenant can show the course application
1. Access to admin site `localhost:8000/manager`
2. login into with username and password of superuser
3. Into `CUSTOMERS` app click on `Clients`
4. Click on `Add Client` button
5. Set Client :
   1. Schema name: demo
   2. Name: Demo
   3. Paid until: 2025-12-31
   4. Save
6. Into `CUSTOMERS` app click on `Domains`
7. Click on `Add Domain` button
8. Set Domain:
   1. Domain: demo.localhost
   2. Tenant: select demo tenant
   3. Save
   
### Create Demo Tenant Super User
```bash
docker compose run --rm django python manage.py create_tenant_superuser --schema=demo --username=demo --email=demo@drifti.com
```

### Create Profile Demo User 
Necessary to tenant user different to public schema.
1. Access to admin site `demo.localhost:8000/manager`
2. login into with username and password of superuser
3. Into `USERS` app click on `Profiles`
4. Click on `Add Profile` button
5. Set Profile :
   1. User: demo
   2. Role: Administrator
   3. Completed: True
   4. Verified: True
   5. Terms & Policy
   6. Save

### Access to Swagger API Documentation
In browser add `demo.localhost:8000/api/v1/docs/`.
Use login endpoint and copy and add `access_token` value to `Authorize` 
button to show private endpoints.

### Development Logs
To show Django logs, run the following command:
```bash
  docker compose logs django -f --tail 20 # Django Service
  docker compose logs -f --tail 20 # All Services
```

