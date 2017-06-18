FROM python:3.6.1

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
ADD . /slack2sheet
WORKDIR /slack2sheet
RUN python setup.py install
EXPOSE 8080
CMD python -m slack2sheet /google/credentials.json $SHEET_URL