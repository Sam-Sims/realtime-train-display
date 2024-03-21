FROM python:3.12.2-alpine3.19

WORKDIR /train-board
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ARG RTT_USER
ARG RTT_PASS
ARG STATION
ENV RTT_USER=$RTT_USER
ENV RTT_PASS=$RTT_PASS
ENV STATION=$STATION

RUN echo "RTT_USER: $RTT_USER RTT_PASS: $RTT_PASS STATION: $STATION"

CMD ["python", "/train-board/src/rtt.py"]