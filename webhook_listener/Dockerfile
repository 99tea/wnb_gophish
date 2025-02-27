FROM python:3.9

WORKDIR /app

COPY get_webhooks.py start_webhook.sh ./

RUN pip install flask requests pandas

EXPOSE 5000

CMD ["sh", "start_webhook.sh"]
