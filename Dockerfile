FROM python:3.8-alpine

# Install packages
RUN apk add --no-cache --update mariadb mariadb-client supervisor gcc musl-dev mariadb-connector-c-dev

# Upgrade pip
RUN python -m pip install --upgrade pip

# Install dependencies
RUN pip install Flask flask_mysqldb pyjwt bcrypt colorama

# Setup app
RUN mkdir -p /app

# Switch working environment
WORKDIR /app

# Add application
COPY src .

# Setup supervisor
COPY config/supervisord.conf /etc/supervisord.conf

# Expose port the server is reachable on
EXPOSE 80

# Disable pycache
ENV PYTHONDONTWRITEBYTECODE=1

# create database and start supervisord
COPY --chown=root entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]