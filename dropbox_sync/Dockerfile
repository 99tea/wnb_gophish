FROM debian:latest

WORKDIR /app

COPY sync_to_dropbox.sh ./

RUN apt update && apt install -y rclone

CMD ["sh", "sync_to_dropbox.sh"]
