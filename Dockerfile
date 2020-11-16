FROM python:3.10.0a2-buster

WORKDIR ./terminal_game.py

#install dependencies
COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY ./terminal_game.py .

CMD ["python3","terminal_game.py"]  

