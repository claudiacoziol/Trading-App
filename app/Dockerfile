FROM python:3.9
WORKDIR /app
ENV FLASK_APP=.
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .
RUN chmod u+x entrypoint.sh
EXPOSE 5000
ENTRYPOINT ["entrypoint.sh"]