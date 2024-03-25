FROM python:3.12-slim

COPY --from=openjdk:8-jre-slim /usr/local/openjdk-8 /usr/local/openjdk-8
ENV JAVA_HOME /usr/local/openjdk-8
RUN update-alternatives --install /usr/bin/java java /usr/local/openjdk-8/bin/java 1

ENV DAGSTER_HOME=/opt/dagster/app
WORKDIR $DAGSTER_HOME

COPY ./requirements.txt $DAGSTER_HOME

RUN pip install -r requirements.txt


COPY .env $DAGSTER_HOME
COPY ./app $DAGSTER_HOME
COPY ./utils $DAGSTER_HOME/utils
COPY resources.py $DAGSTER_HOME
COPY credentials-admin.p12 $DAGSTER_HOME


EXPOSE 4000
CMD ["dagster", "api", "grpc", "-h", "0.0.0.0", "-p", "4000", "-f", "repository.py"]
