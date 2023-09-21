FROM python:3.8

RUN python -m pip install --upgrade pip

# Create app directory
WORKDIR /app
 
# Install app dependencies
COPY requirements.txt ./
 
RUN pip install -r requirements.txt
 
# Bundle app source
COPY . .
 
EXPOSE 8000
CMD [ "python", "src/main.py"]