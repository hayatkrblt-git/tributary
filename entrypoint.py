
"""Dependencies Defined

gunicorn==21.2.0:
"gunicorn" is a Python web server that can run web applications written in Flask, Django, and other frameworks.
"21.2.0" is the specific version of gunicorn that your project requires. The "==21.2.0" means that your project is compatible with this exact version.
Flask==3.0.0:
"Flask" is a lightweight web framework for building web applications in Python.
"3.0.0" is the specific version of Flask that your project requires.
loguru==0.7.2:
"loguru" is a Python logging library that simplifies logging in your application.
"0.7.2" is the specific version of loguru that your project requires.
requests==2.31.0:
"requests" is a Python library for making HTTP requests to web services or APIs.
"2.31.0" is the specific version of the "requests" library that your project requires.
redis==5.0.1:
"redis" is a Python client library for interacting with Redis, which is an in-memory data store.
"5.0.1" is the specific version of the "redis" library that your project requires."""
import json
import redis as redis
from Flask import Flask, request
from loguru import logger

HISTORY_LENGTH = 10
DATA_KEY = "engine_temperature"

@app.route('/record', methods=['POST'])
def record_engine_temperature():
    payload = request.get_json(force=True)
    logger.info(f"(*) record request --- {json.dumps(payload)} (*)")

    engine_temperature = payload.get("engine_temperature")
    logger.info(f"engine temperature to record is: {engine_temperature}")

    database = redis.Redis(host="redis", port=6379, db=0, decode_responses=True)
    database.lpush(DATA_KEY, engine_temperature)
    logger.info(f"stashed engine temperature in redis: {engine_temperature}")

    while database.llen(DATA_KEY) > HISTORY_LENGTH:
        database.rpop(DATA_KEY)
    engine_temperature_values = database.lrange(DATA_KEY, 0, -1)
    logger.info(f"engine temperature list now contains these values: {engine_temperature_values}")

    logger.info(f"record request successful")
    return {"success": True}, 200
