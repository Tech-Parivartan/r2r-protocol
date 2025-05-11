FROM python:3.10-slim

WORKDIR /app

COPY sdk/python/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY sdk/python/r2r_protocol ./r2r_protocol

CMD ["python", "-c", "from r2r_protocol import RobotClient; client = RobotClient(robot_id='docker_bot', host='host.docker.internal'); print('Ready')"]
