FROM python:3.8
ADD . ./opt/
WORKDIR /opt/
EXPOSE 5000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","manage.py","runserver","-h","0.0.0.0"]

# docker build -t dmptool .
# docker run --name dmptool -e MYSQL_PASSWORD=password -p 5000:5000 --link servidor_mysql:mysql -d dmptool
