FROM alpine:3.20
RUN apk add --no-cache curl
COPY lab/trusted/run.sh /run.sh
RUN chmod +x /run.sh
ENTRYPOINT ["/run.sh"]
