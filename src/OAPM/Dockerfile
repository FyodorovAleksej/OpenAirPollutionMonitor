FROM python:3

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python setup.py install
CMD sleep 20 && air_pollution_dumper

