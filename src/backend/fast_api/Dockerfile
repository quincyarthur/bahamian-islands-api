# 
FROM python:3.11
#
WORKDIR /usr/src/app
# 
COPY . .
#
RUN pip install --no-cache-dir --upgrade -r requirements.txt && chmod +x start_up.sh

CMD sh -c ./start_up.sh