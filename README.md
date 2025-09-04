**# django-todo-app**
Please follow the steps to deploy the project:
If you setup the project as a root user (sudo su), then please avoid sudo in the commands.

**1. Project Structure and Virtual Environment:**
  cd /var/www/html
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  pip install gunicorn

**2. Django Settings Configuration:**
  Edit the settings.py file:
  # Add your EC2 public IP to ALLOWED_HOSTS
ALLOWED_HOSTS = ['your-ec2-public-ip', 'localhost', '127.0.0.1']

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# For production, set DEBUG to False
DEBUG = False

**3. Collect Static Files:**
   python manage.py collectstatic

**4. Create Gunicorn Service File:**
   sudo nano /etc/systemd/system/gunicorn.service
   Add the below configurations
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/var/www/html
ExecStart=/var/www/html/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/html/gunicorn.sock todo_project.wsgi:application

[Install]
WantedBy=multi-user.target

**5. Configure Nginx:**
   sudo nano /etc/nginx/sites-available/django-todo
Add the configurations into the nginx/sites-available/django-todo file:

server {
    listen 80;
    server_name your-ec2-public-ip;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /var/www/html;
    }
    
    location / {
        include proxy_params;
        proxy_pass http://unix:/var/www/html/gunicorn.sock;
    }
}

Enable the site:
sudo ln -s /etc/nginx/sites-available/django-todo /etc/nginx/sites-enabled/

**6. Set Proper Permissions**
sudo chown -R ubuntu:www-data /var/www/html
sudo chmod -R 755 /var/www/html

**7. Start and Enable Services**
# Start Gunicorn
sudo systemctl start gunicorn
sudo systemctl enable gunicorn

# Restart Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx

**8. Apply Database Migrations**
cd /var/www/html
source venv/bin/activate
python manage.py migrate

**9. Security Group Configuration**
Ensure your EC2 security group allows HTTP traffic (port 80) from anywhere (0.0.0.0/0).

**10. Test the Setup**
# Check Gunicorn status
sudo systemctl status gunicorn

# Check Nginx configuration
sudo nginx -t

# Check Nginx status
sudo systemctl status nginx


**Troubleshooting Tips**
If you encounter issues:

1. Check logs for errors:
# Nginx error logs
sudo tail -f /var/log/nginx/error.log

# Gunicorn logs
sudo journalctl -u gunicorn

2. If you get permission errors:
sudo chmod 755 /var/www/html
sudo chown -R ubuntu:www-data /var/www/html

3. If you need to make changes and restart:
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx












   
