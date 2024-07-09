FROM --platform=linux/amd64 python:3.11.9-bookworm
ENV PYTHONPYCACHEPREFIX=/usr/src/pycache \
    PYTHONPATH=/app \
    PIP_ROOT_USER_ACTION=ignore \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1
WORKDIR /app

RUN apt-get -qq update && apt-get -qq install -y libssl-dev
RUN pip install --upgrade pip setuptools

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./static ./static
COPY ./templates ./templates
COPY *.py ./

EXPOSE 80
CMD ["python", "app.py"]
