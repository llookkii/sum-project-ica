# Use an official NGINX image
FROM nginx:alpine

# Copy static files to NGINX's default directory
COPY index.html /usr/share/nginx/html/
COPY css /usr/share/nginx/html/css/
COPY js /usr/share/nginx/html/js/

# Expose port 80
EXPOSE 80