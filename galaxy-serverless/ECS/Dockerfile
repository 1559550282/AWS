FROM python:3.6
RUN mkdir /code  
WORKDIR /code  
ADD . /code/  
COPY ecs.py /code/
RUN pip install -r requirements.txt  

EXPOSE 5000  
CMD ["python", "/code/ecs.py"]`
