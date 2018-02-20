FROM python:3.5
ADD . /api_endpoint
WORKDIR /api_endpoint
EXPOSE 5000
RUN pip3 install -r requirements.txt
ENTRYPOINT ["python3", "app.py"]
