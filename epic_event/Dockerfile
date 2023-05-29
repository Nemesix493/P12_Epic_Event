FROM python:3.10
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
#ENV PYTHONUNBUFFERED=1
#ENV PYTHONDONTWRITEBYTECODE=1
#RUN pip install gunicorn
EXPOSE 8000
CMD ["/bin/bash", "start.sh"]