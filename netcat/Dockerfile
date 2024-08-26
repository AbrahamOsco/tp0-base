FROM alpine:latest
RUN apk add --no-cache netcat-openbsd
COPY ./netcat/test_echo_server.sh /
RUN chmod +x test_echo_server.sh
ENTRYPOINT ["./test_echo_server.sh"]
