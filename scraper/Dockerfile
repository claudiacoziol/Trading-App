FROM python:3.9
WORKDIR /scraper
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .
CMD ["python3", "scraper.py"]