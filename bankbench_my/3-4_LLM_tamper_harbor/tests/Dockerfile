FROM python:3.11-slim

WORKDIR /tests

COPY grader.py .
COPY test.sh .
RUN chmod +x test.sh

ENTRYPOINT ["/tests/test.sh"]
