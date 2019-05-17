FROM python:2
RUN	mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
COPY code/v1/ /usr/src/app/
RUN ls -lRa /usr/src/app/*
CMD ["gunicorn", "-w", "32", "-b", "0.0.0.0:6789", "api:app", "--preload"]