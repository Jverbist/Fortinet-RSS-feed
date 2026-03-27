FROM debian:bookworm-slim

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y postfix ca-certificates rsyslog && \
    rm -rf /var/lib/apt/lists/*

COPY main.cf /etc/postfix/main.cf

CMD service rsyslog start && postfix start-fg
