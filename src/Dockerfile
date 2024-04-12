FROM python:3.10
LABEL authors="kr1sta1l"

COPY src/ /app/src/

WORKDIR /app

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r src/requirements.txt



ENTRYPOINT ["python", "src/main.py"]

# to build the image:
# docker build -t auditorium_service .

# to run the image:
# docker run --network="kursach-network" --name auditorium_service -d -p 8000:8000 auditorium_service


