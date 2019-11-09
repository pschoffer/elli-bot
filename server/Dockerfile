FROM python:3-alpine
EXPOSE 5000
EXPOSE 5001

WORKDIR /usr/src/app

COPY *.py ./

RUN ["python", "setup.py", "install"]

ENTRYPOINT ["python", "app.py"]

