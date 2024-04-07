FROM nginx:1.25.2-alpine
RUN mkdir -p /app/drifti/static/
RUN rm /etc/nginx/conf.d/default.conf
COPY /compose/pro/nginx/nginx.conf /etc/nginx/conf.d