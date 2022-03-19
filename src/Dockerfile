FROM python:3.8.12-bullseye AS buildstage
WORKDIR /req
COPY requirements.txt .
RUN pip install -r requirements.txt -t .

FROM scratch as export-stage
COPY --from=buildstage /req .