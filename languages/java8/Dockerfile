FROM openjdk:8u181-alpine

COPY build_program.sh run_program.sh /usr/bin/
RUN chmod 555 /usr/bin/*.sh
RUN adduser -h / -s /bin/sh -D user
USER user
CMD ["/bin/sh"]
