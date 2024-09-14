FROM python:3.9-slim

WORKDIR /bot

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "gemini_dc_bot/bot.py"]