FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm supervisor && rm -rf /var/lib/apt/lists/*

# Copies over the project filesa
COPY . .

RUN uv sync

RUN npm i

RUN npx @tailwindcss/cli -i ./static/css/input.css -o ./static/dist/output.css --minify

EXPOSE 4500

CMD ["supervisord", "-n", "-c", "/app/supervisord.conf"]