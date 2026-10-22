#!/usr/bin/env bash
# Sets up web servers for the deployment of web_static

# Install Nginx if not already installed
if ! command -v nginx > /dev/null 2>&1; then
    apt-get update -y
    apt-get install -y nginx
fi

# Create required directories
mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/

# Create a fake HTML file to test Nginx configuration
printf '%s\n' \
"<html>" \
"  <head>" \
"  </head>" \
"  <body>" \
"    School" \
"  </body>" \
"</html>" > /data/web_static/releases/test/index.html

# Create or recreate symbolic link
rm -rf /data/web_static/current
ln -s /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group recursively
chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve /data/web_static/current/ to hbnb_static
if ! grep -q "location /hbnb_static" /etc/nginx/sites-available/default; then
    sed -i 's|server_name _;|server_name _;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t\tindex index.html index.htm;\n\t}|' /etc/nginx/sites-available/default
fi

# Restart Nginx
service nginx restart

exit 0
