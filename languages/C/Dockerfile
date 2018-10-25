FROM gcc:8.2.0

COPY build_program.sh run_program.sh /usr/bin/
RUN chmod 555 /usr/bin/*.sh
RUN useradd -d / -M -s /bin/bash user
USER user
CMD ["/bin/bash"]
