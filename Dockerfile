FROM ubuntu

RUN apt update && \
    apt install -y python3-pip
RUN pip3 install python-telegram-bot

COPY src /bot

CMD ["python3", "/bot/bullsNcows.py"]
