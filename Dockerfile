FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

RUN apt-get update && apt-get install -y --no-install-recommends nodejs npm && rm -rf /var/lib/apt/lists/*

# Copies over the project filesa
COPY . .

RUN uv sync

RUN npm i

RUN npx @tailwindcss/cli -i ./static/css/input.css -o ./static/dist/output.css --minify

EXPOSE 4500

CMD sh -c "npx @tailwindcss/cli -i ./static/css/input.css -o ./static/dist/output.css --watch & uv run flask --debug run --host 0.0.0.0 --port 4500"