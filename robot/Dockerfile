from java

RUN mkdir /app
ADD https://github.com/ontodev/robot/releases/download/v1.6.0/robot.jar /app
WORKDIR /home

ENTRYPOINT ["/usr/bin/java", "-jar", "/app/robot.jar"]
CMD ["--help"]
