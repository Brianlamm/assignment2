import requests
import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from status import Status
import datetime
import yaml
import logging
import logging.config
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
import json
from flask_cors import CORS, cross_origin
import os
from os import path

with open('log_conf.yml', 'r') as f: 
    log_config = yaml.safe_load(f.read()) 
    logging.config.dictConfig(log_config)

logger = logging.getLogger('basicLogger')

with open('app_conf.yml', 'r') as f: 
    app_config = yaml.safe_load(f.read())

site_root = os.path.realpath(os.path.dirname(__file__))
event_file = os.path.join(site_root, 'health.json')

# json functions
def to_json(file, payload):
    """
    Takes payload data and writes it to a JSON file. JSON file should be initialized with {"subs": []}
    :param: file: file path
    :type: str
    :param: payload: data to be written to the file
    :type: str
    """

    # Open file as write and dump JSON payload to file
    with open(file, mode='w') as json_file:
        json.dump(payload, json_file)

def clear_json(file):
    # Object to initialize file with
    init_data = {"data": []}
    with open(file, mode='w+') as f:
        # Seek beginning of file and rewrite the file
        f.seek(0)
        f.truncate()
        f.write(json.dumps(init_data))

def json_init():
    # Try block to check if file exists, or if file is corrupted
    try:
        with open(event_file) as json_file:
            data = json.load(json_file)
        print(f'json file successfully returned')
        return data
    except json.JSONDecodeError or TypeError:
        data = clear_json(event_file)
        print(f'json file cleared')
        return data
    except FileNotFoundError:
        data = {"data": []}
        with open(event_file, mode='w+') as f:
            f.write(json.dumps(data))
        print(f'json file initialized')
        return data

def get_health():
    '''Returns stats data'''
    receiver = requests.get(f'{app_config["eventstore"]["receiver"]}', timeout=4)
    logger.info(f'receiver response is: {receiver.status_code}')
    storage = requests.get(f'{app_config["eventstore"]["storage"]}', timeout=4)
    logger.info(f'storage response is: {storage.status_code}')
    processing = requests.get(f'{app_config["eventstore"]["processing"]}', timeout=4)
    logger.info(f'processing response is: {processing.status_code}')
    audit= requests.get(f'{app_config["eventstore"]["audit"]}', timeout=4)
    logger.info(f'audit response is: {audit.status_code}')
    now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    r = receiver.status_code
    s = storage.status_code
    p = processing.status_code
    a = audit.status_code

    status_codes = [r, s, p, a]

    for i in range(len(status_codes)):
        if status_codes[i] < 400:
            status_codes[i] = 'running'
        else:
            status_codes[i] = 'down'

    payload = {
        "receiver": status_codes[0],
        "storage": status_codes[1],
        "processing": status_codes[2],
        "audit": status_codes[3],
        "last_update": now
    }
 
    to_json(event_file, payload)
    logger.info(f'payload written to json file')
    logger.info(f'payload: \n{payload}')
    return payload, 200

def init_scheduler(): 
    sched = BackgroundScheduler(daemon=True) 
    sched.add_job(get_health,
                  'interval', 
                  seconds=app_config['scheduler']['period_sec']) 
    sched.start()

app = connexion.FlaskApp(__name__, specification_dir='')
app.add_api('openapi.yml', base_path="/health", strict_validation=True, validate_responses=True) 

if "TARGET_ENV" not in os.environ or os.environ["TARGET_ENV"] != "test":
    CORS(app.app)
    app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__": 
    # run our standalone gevent server 
    init_scheduler() 
    app.run(port=8120, use_reloader=False)