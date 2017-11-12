FROM alpine

ENV PUZZLE_DOMAIN_NAME=puzzle.test.winstead.us

COPY requirements.txt /tmp/build/requirements.txt
COPY required-packages-alpine.txt /tmp/build/required-packages-alpine.txt
COPY businesscard_puzzle /businesscard_puzzle

 # Current bug with fetching the incremtnal python pkg
RUN xargs apk add --no-cache < /tmp/build/required-packages-alpine.txt && \
    python3 -m pip install incremental && \
    python3 -m pip install -r /tmp/build/requirements.txt && \
    rm -vfr /tmp/build

VOLUME /etc/letsencrypt

WORKDIR /
ENTRYPOINT /usr/bin/python3 -m businesscard_puzzle