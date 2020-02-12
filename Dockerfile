FROM python:3.8
ADD . ./opt/
WORKDIR /opt/
EXPOSE 5000
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["python","manage.py","runprodserver"]

# sudo docker build -t dmptool-api .
# docker run --name mydmptool-api -v /var/log/dmptool:/opt/log -v /home/dmptool/dbase-dmptool:/opt/db -v /home/dmptool/documents-dmptool:/opt/documents -p 5000:5000 --link mongodb:mongo -d dmptool-api
