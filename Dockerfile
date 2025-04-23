# Użyj obrazu Python jako bazowego
FROM python:3.10-slim

# Ustaw katalog roboczy
WORKDIR /app

# Skopiuj pliki aplikacji do kontenera
COPY . /app

# Zainstaluj zależności
RUN pip install --no-cache-dir -r requirements.txt

# Otwórz port aplikacji (np. 8000)
EXPOSE 8000

# Uruchom aplikację
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]