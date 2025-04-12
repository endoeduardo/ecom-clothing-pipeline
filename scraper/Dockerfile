FROM python:3.12

WORKDIR /app

COPY scraper_requirements.txt .

RUN pip install --no-cache-dir -r scraper_requirements.txt

RUN playwright install

COPY . .

EXPOSE 2001

# CMD ["python", "scraper/main.py"]
