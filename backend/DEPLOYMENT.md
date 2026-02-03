# Backend Deployment & Production Checklist

## Pre-Production Checklist

### Security
- [ ] Change `SECRET_KEY` in settings.py to a secure random value
- [ ] Set `DEBUG = False` in production
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Enable HTTPS/SSL certificates
- [ ] Update `CORS_ALLOWED_ORIGINS` with frontend URLs only
- [ ] Set secure cookie flags: `SESSION_COOKIE_SECURE = True`
- [ ] Configure CSRF protection properly

### Database
- [ ] Migrate from SQLite to PostgreSQL
- [ ] Set up database backups
- [ ] Configure database connection pooling
- [ ] Enable database logging/monitoring
- [ ] Run database optimization queries

### Static Files & Media
- [ ] Collect static files: `python manage.py collectstatic`
- [ ] Configure CDN for static assets
- [ ] Set up media file storage (S3, etc.)
- [ ] Configure proper file permissions

### Environment
- [ ] Create production `.env` file
- [ ] Set all required environment variables
- [ ] Review `requirements.txt` versions
- [ ] Consider using `requirements-lock.txt`

### Logging & Monitoring
- [ ] Configure Django logging
- [ ] Set up error tracking (Sentry, etc.)
- [ ] Enable access/request logging
- [ ] Set up alerts for critical errors
- [ ] Monitor server resources

### Testing
- [ ] Run full test suite: `python manage.py test`
- [ ] Load testing
- [ ] Security vulnerability scanning
- [ ] Database migration testing

---

## Production Deployment Options

### Option 1: Traditional VPS/Server

**Stack:**
- Gunicorn (WSGI server)
- Nginx (reverse proxy)
- PostgreSQL (database)
- Systemd (process management)

**Setup Steps:**
```bash
# Install dependencies
sudo apt-get install python3 python3-pip python3-venv postgresql nginx

# Create application directory
sudo mkdir -p /var/www/chemequip
sudo chown $USER:$USER /var/www/chemequip

# Clone and setup
cd /var/www/chemequip
git clone <your-repo> .
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Configure database
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create Gunicorn systemd service
sudo nano /etc/systemd/system/chemequip.service
```

**Gunicorn Configuration:**
```bash
[Unit]
Description=Chemical Equipment Visualizer
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/chemequip
Environment="PATH=/var/www/chemequip/venv/bin"
ExecStart=/var/www/chemequip/venv/bin/gunicorn chemequip_backend.wsgi:application --bind 127.0.0.1:8000 --workers 4

[Install]
WantedBy=multi-user.target
```

**Nginx Configuration:**
```nginx
upstream chemequip {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name your-domain.com;
    
    client_max_body_size 10M;
    
    location /static/ {
        alias /var/www/chemequip/staticfiles/;
    }
    
    location /media/ {
        alias /var/www/chemequip/media/;
    }
    
    location / {
        proxy_pass http://chemequip;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Option 2: Docker Containerization

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "chemequip_backend.wsgi:application", "--bind", "0.0.0.0:8000"]
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: chemequip
      POSTGRES_USER: chemequip_user
      POSTGRES_PASSWORD: secure_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    command: gunicorn chemequip_backend.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://chemequip_user:secure_password@db:5432/chemequip
    depends_on:
      - db

volumes:
  postgres_data:
```

### Option 3: Platform-as-a-Service (PaaS)

**Heroku:**
```bash
# Install Heroku CLI
# Create Procfile
web: gunicorn chemequip_backend.wsgi

# Create runtime.txt
python-3.11.8

# Add Postgres add-on
heroku addons:create heroku-postgresql:standard-0

# Deploy
git push heroku main
```

**PythonAnywhere:**
1. Upload code via git or web interface
2. Create virtual environment
3. Configure web app settings
4. Set environment variables
5. Reload web app

### Option 4: AWS Deployment

**Elastic Beanstalk:**
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.11 chemequip

# Create environment
eb create chemequip-env

# Deploy
eb deploy
```

**RDS for Database:**
- Create PostgreSQL RDS instance
- Update Django database configuration
- Run migrations: `eb ssh` → `python manage.py migrate`

---

## Production Configuration Updates

### settings.py Production Changes

```python
# Production settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    
    # Database - PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME'),
            'USER': os.environ.get('DB_USER'),
            'PASSWORD': os.environ.get('DB_PASSWORD'),
            'HOST': os.environ.get('DB_HOST'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
    
    # S3 Storage for media files
    if 'AWS_STORAGE_BUCKET_NAME' in os.environ:
        import storages
        DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
        STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
        MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
```

### Monitoring & Logging

```python
# logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': '/var/log/chemequip/django.log',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'sentry_sdk.integrations.logging.EventHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'sentry'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

---

## Performance Optimization

### Caching
```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Database Optimization
- Add database indexes on frequently queried fields
- Use `select_related()` and `prefetch_related()`
- Implement connection pooling
- Archive old datasets

### API Optimization
- Enable pagination (already configured)
- Implement rate limiting: `django-ratelimit`
- Enable GZIP compression in Nginx
- Use CloudFlare for CDN

---

## Backup & Disaster Recovery

### Database Backups
```bash
# PostgreSQL backup
pg_dump -h localhost -U user -d chemequip > backup.sql

# Automated daily backups
0 2 * * * pg_dump -h localhost -U user -d chemequip | gzip > /backups/chemequip_$(date +\%Y-\%m-\%d).sql.gz
```

### Media File Backups
- Store on S3 or other cloud storage
- Enable versioning
- Set up replication

### Recovery Procedures
1. Document recovery steps
2. Test backups regularly
3. Maintain offline backup copies
4. Document database schemas

---

## Monitoring & Alerts

### Key Metrics to Monitor
- CPU usage
- Memory usage
- Disk usage
- Database connection pool
- Request response time
- Error rates
- File upload failures

### Tools
- **Monitoring**: Prometheus, Grafana
- **Logging**: ELK Stack, CloudWatch
- **Error Tracking**: Sentry
- **APM**: New Relic, DataDog
- **Uptime**: UptimeRobot, Pingdom

---

## Security Hardening

### Additional Packages
```bash
pip install django-cors-headers  # Already included
pip install django-ratelimit     # Rate limiting
pip install django-extensions    # Useful utilities
pip install sentry-sdk          # Error tracking
pip install django-security    # Security utilities
```

### Headers Security
```python
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
}
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
```

### File Upload Security
- Validate file types (already done)
- Scan for malware
- Limit file size (already configured)
- Store outside web root

---

## Scaling Strategy

### Vertical Scaling
- Increase server resources (CPU, RAM)
- Upgrade database instance
- Increase worker processes

### Horizontal Scaling
- Load balancing with Nginx/HAProxy
- Multiple application servers
- Database replication/sharding
- Separate API from background tasks

### Background Tasks
```bash
pip install celery redis

# Long-running operations:
- PDF report generation
- Data analytics calculations
- Email notifications
```

---

## Maintenance Schedule

### Daily
- Monitor error logs
- Check server health
- Verify backups completed

### Weekly
- Review performance metrics
- Check security alerts
- Test disaster recovery

### Monthly
- Update dependencies: `pip list --outdated`
- Security patches
- Performance optimization
- Database maintenance

### Quarterly
- Major version updates
- Security audit
- Load testing
- Documentation review

---

## Rollback Procedure

```bash
# Keep previous versions tagged
git tag -a v1.0.0 -m "Production release"

# Quick rollback
git checkout v1.0.0-previous
python manage.py migrate  # Run migrations (if needed backward)
systemctl restart chemequip
```

---

## Support & Troubleshooting

### Common Issues

1. **Database Connection Timeout**
   - Check database credentials
   - Verify network connectivity
   - Increase connection pool size

2. **File Upload Failures**
   - Check disk space
   - Verify file permissions
   - Check upload size limits

3. **API Response Slow**
   - Enable caching
   - Optimize database queries
   - Add more worker processes

4. **Memory Leaks**
   - Monitor memory usage
   - Review code for leaks
   - Restart application regularly

---

**Once deployed to production, monitor continuously and optimize based on actual usage patterns.**
