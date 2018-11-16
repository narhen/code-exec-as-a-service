FROM python:3.7-alpine

COPY build_program.sh run_program.sh /usr/bin/
RUN chmod 555 /usr/bin/*.sh
RUN adduser -h / -H -D -s /bin/bash user
USER user
CMD ["/bin/sh"]
