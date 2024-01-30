FROM postgres:16.1-bookworm

RUN apt-get update \
    && apt-get install -y gunicorn3 postgresql nano git python3-pip python3-poetry\
    && pip3 install --upgrade pip

ENV POSTGRES_USER=user
ENV POSTGRES_PASSWORD=secretpassword
ENV POSTGRES_HOST=127.0.0.1
ENV POSTGRES_INSTANCE=orders

WORKDIR /usr/orders

COPY . .

RUN poetry install

EXPOSE 5000

CMD ["poetry", "run", "warehouse-ddd"]