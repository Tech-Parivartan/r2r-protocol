FROM python:3.10-slim

WORKDIR /app

COPY sdk/python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sdk/python/ .

CMD ["python", "-c", "from r2r.client import RobotClient; client = RobotClient(robot_id='docker_bot'); print('Ready')"]
