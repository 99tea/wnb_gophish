# Use the official Caddy image
FROM caddy:2.7

# Copy our Caddyfile into the container
COPY Caddyfile /etc/caddy/Caddyfile

# Copy static files (optional)
COPY site/ /var/www/html

# Use environment variables inside Caddy
ENV SERVER_IP=0.0.0.0
ENV ALLOWED_IP=127.0.0.1
ENV LANDING_DOMAINS=example.com
