FROM python:3.9
WORKDIR /api
ENV FLASK_APP=.
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt
COPY . .
COPY entrypoint.sh entrypoint.sh
RUN chmod u+x entrypoint.sh
ENTRYPOINT ["entrypoint.sh"]