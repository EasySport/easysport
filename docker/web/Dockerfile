# - start with python image
FROM python:3.6

# TODO: run uwsgi
# install all updates and UWSGI
RUN apt-get update && \
    apt-get install -y && \
    pip3 install uwsgi

# - set PYTHONBUFFERED value to 1
ENV PYTHONUNBUFFERED 1

# - add code folder inside
RUN mkdir /code

# - set the working directory for all further commands
WORKDIR /code

# - add file requirements.txt to /code/ inside image
ADD web/requirements.txt /code/

# - install all requirements
RUN pip install -r requirements.txt

# - copy all other files to /code/ directory
ADD ./web/ /code/

# post-install tasks
# RUN python manage.py migrate
# RUN python manage.py collectstatic