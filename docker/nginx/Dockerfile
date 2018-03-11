# Build using last stable image
FROM nginx

# remove default conf file
RUN rm /etc/nginx/conf.d/default.conf

# add new conf file from near direction
ADD conf.d/ /etc/nginx/conf.d