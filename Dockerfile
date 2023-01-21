FROM mcr.microsoft.com/playwright:focal

RUN apt-get update && apt-get install -y python3-pip

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt
RUN python3 -m playwright install

COPY . .

ENTRYPOINT ["python3", "bot.py"]
