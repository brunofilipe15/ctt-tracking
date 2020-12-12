FROM python:3.8

COPY . /app
WORKDIR /app

RUN apt-get -y update
RUN apt-get install -y chromium chromium-driver

# set display port to avoid crash
ENV DISPLAY=:99

RUN pip install --upgrade pip
RUN pip install selenium

#RUN pip install -r requirements.txt

CMD ["python", "./app.py"]