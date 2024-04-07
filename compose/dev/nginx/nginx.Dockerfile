FROM nginx:1.25.2-alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY /compose/dev/nginx/nginx.conf /etc/nginx/conf.d