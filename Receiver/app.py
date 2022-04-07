import requests
import connexion 
from connexion import NoContent
import yaml
import logging
import logging.config
import uuid
import datetime 
import json 
from pykafka import KafkaClient 
import os
import time

if "TARGET_ENV" in os.environ and os.environ["TARGET_ENV"] == "test":
    print("In Test Environment")
    app_conf_file = "/config/app_conf.yml"
    log_conf_file = "/config/log_conf.yml"
else:
    print("In Dev Environment")
    app_conf_file = "app_conf.yml"
    log_conf_file = "log_conf.yml"

with open(app_conf_file, 'r') as f:
    app_config = yaml.safe_load(f.read())
    
# External Logging Configuration
with open(log_conf_file, 'r') as f:
    log_config = yaml.safe_load(f.read())
    logging.config.dictConfig(log_config)
    
logger = logging.getLogger('basicLogger')

logger.info("App Conf File: %s" % app_conf_file)
logger.info("Log Conf File: %s" % log_conf_file)

hostname = "%s:%d" % (app_config["events"]["hostname"],   
                          app_config["events"]["port"]) 

count = 0
while count < app_config["connection"]["max_count"]:
    try:
        client = KafkaClient(hosts=hostname) 
        topic = client.topics[str.encode(app_config["events"]["topic"])] 
        break
        
    except:
        time.sleep(app_config["connection"]["wait"])
        count += 1

def get_health():
    return 200

def report_ticket_info(body):
    trace_id = str(uuid.uuid4())
    body["trace_id"] = trace_id 
    logging.info(f'Receive event ticket request with a trace id of {body["trace_id"]}')
    # headers = { "content-type": "application/json" }
    # response = requests.post("http://localhost:8090/report/ticket", 
    # json=body, headers=headers)
    # logging.info(f'Returned event ticket response (Id: {body["trace_id"]}) with status {response.status_code}')
    # hostname = "%s:%d" % (app_config["events"]["hostname"],  
    #                       app_config["events"]["port"]) 
    # client = KafkaClient(hosts=hostname) 
    # topic = client.topics[str.encode(app_config["events"]["topic"])] 
    producer = topic.get_sync_producer() 
    msg = { "type": "ticket",  
            "datetime" :    
            datetime.datetime.now().strftime( 
                "%Y-%m-%dT%H:%M:%S"),  
            "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))

    return NoContent, 201 
 
def report_sale_info(body):
    trace_id = str(uuid.uuid4())
    body["trace_id"] = trace_id 
    logging.info(f'Receive event ticket request with a trace id of {body["trace_id"]}')
    # headers = { "content-type": "application/json" }
    # response = requests.post("http://localhost:8090/report/sale", 
    # json=body, headers=headers)
    # logging.info(f'Returned event ticket response (Id: {body["trace_id"]}) with status {response.status_code}')
    # hostname = "%s:%d" % (app_config["events"]["hostname"],  
    #                       app_config["events"]["port"]) 
    # client = KafkaClient(hosts=hostname) 
    # topic = client.topics[str.encode(app_config["events"]["topic"])] 
    producer = topic.get_sync_producer() 
    msg = { "type": "sale",  
            "datetime" :    
            datetime.datetime.now().strftime( 
                "%Y-%m-%dT%H:%M:%S"),  
            "payload": body } 
    msg_str = json.dumps(msg) 
    producer.produce(msg_str.encode('utf-8'))

    return NoContent, 201 

app = connexion.FlaskApp(__name__, specification_dir='') 
app.add_api("openapi.yml",
base_path="/receiver",
strict_validation=True,  
validate_responses=True) 

if __name__ == "__main__": 
    app.run(port=8080)