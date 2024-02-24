FROM python:3.12-slim

ENV DAGSTER_HOME=/opt/dagster/app
WORKDIR $DAGSTER_HOME

COPY ./requirements.txt $DAGSTER_HOME

RUN pip install -r requirements.txt


COPY ./app $DAGSTER_HOME
COPY ./utils $DAGSTER_HOME/utils
COPY repository.py $DAGSTER_HOME

EXPOSE 4000
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "repository.py"]
