FROM python
COPY . ./app
WORKDIR /app
RUN apt update && apt install  openssh-server sudo -y
RUN useradd -rm -d /home/ubuntu -s /bin/bash -g root -G sudo -u 1000 test 
RUN  echo 'test:test' | chpasswd
EXPOSE 22
RUN service ssh start
RUN pip install kafka-python
RUN pip install pymongo[srv]
RUN pip install requests
RUN pip install psutil
RUN pip install Flask
RUN pip install multithreading
CMD [ "python","script.py" ]
