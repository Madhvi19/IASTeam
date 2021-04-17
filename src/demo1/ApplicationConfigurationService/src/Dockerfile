FROM python
COPY . ./app
WORKDIR /app
RUN pip install kafka-python
RUN pip install pymongo[srv]
RUN pip install requests
RUN pip install psutil
RUN pip install Flask
CMD [ "python","script.py" ]
