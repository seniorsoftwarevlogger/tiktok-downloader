FROM mcr.microsoft.com/playwright:focal

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN python3 -m playwright install

COPY . .

EXPOSE 8080

ENTRYPOINT ["python3", "server.py", "8080", "0.0.0.0"]
