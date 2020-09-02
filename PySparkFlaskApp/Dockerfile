FROM openjdk:8
RUN java -version
RUN ["apt-get", "update"]
RUN ["apt-get", "upgrade", "-y", "--fix-missing"]
RUN apt-get update && apt-get -y install python python3 python-pip python3-pip
WORKDIR /usr/src/app

COPY dependancies.txt ./

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --no-cache-dir -r dependancies.txt

COPY . .

CMD [ "python3", "./app.py" ]