FROM python
COPY . ./app
WORKDIR /app
RUN pip install kafka-python
RUN pip install pymongo[srv]
CMD [ "python","rtm.py" ]
