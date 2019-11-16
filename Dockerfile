FROM python
ADD . /app
RUN pip3 install -r /app/requirements.txt
CMD python /app/app.py