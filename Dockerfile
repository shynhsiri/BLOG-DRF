FROM python:3.9-alpine3.13
# container maintainer name
LABEL maintainer="shynhsiri" 

# Tells python to don't buffer the output, the output will directly printed in console which prevents delays
ENV PYTHONUNBUFFERED 1

# copy the needed files from local machine to the container & /tmp added the file into image
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
# working directory that the commands will run from
WORKDIR /app
# allow access to the port
EXPOSE 8000
# dev default
ARG DEV=false
# run will install some dependesies on our machine
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

ENV PATH="/py/bin:$PATH"

USER django-user