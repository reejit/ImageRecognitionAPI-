FROM python:3.6
WORKDIR /usr/src/app
COPY requirements.txt ./
RUN pip3 install --default-timeout=100 future --no-cache-dir -r requirements.txt
COPY . .
CMD [ "python3", "app.py" ]
