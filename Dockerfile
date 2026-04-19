FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

# Copies over the project filesa
COPY . .

RUN uv sync

EXPOSE 4500

CMD ["uv", "run", "flask", "--debug", "run", "--host", "0.0.0.0", "--port", "4500"]