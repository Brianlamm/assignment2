import requests
import connexion
from connexion import NoContent
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from base import Base
from stats import Stats
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

if not path.exists(app_config["datastore"]["filename"]):
    import sqlite3 
 
    conn = sqlite3.connect(app_config["datastore"]["filename"]) 
    
    c = conn.cursor() 
    c.execute(''' 
            CREATE TABLE stats 
            (id INTEGER PRIMARY KEY ASC,  
            num_ticket_report INTEGER NOT NULL, 
            num_sale_report INTEGER NOT NULL, 
            min_sale_report INTEGER, 
            max_sale_report INTEGER, 
            last_updated VARCHAR(100) NOT NULL) 
            ''') 
    
    conn.commit() 
    conn.close()

DB_ENGINE = create_engine(f'sqlite:///{app_config["datastore"]["filename"]}')
Base.metadata.bind = DB_ENGINE
DB_SESSION = sessionmaker(bind=DB_ENGINE)

def get_stats(): 
    """ Gets new sale reports after the timestamp """ 
 
    session = DB_SESSION() 
    reports = session.query(Stats).order_by(Stats.last_updated.desc()) 
  
    results_list = [] 
 
    for report in reports: 
        results_list.append(report.to_dict()) 
 
    session.close() 
     
    logger.info("Return event") 
 
    return results_list[0], 200

def populate_stats(): 
    """ Periodically update stats """ 
    logger.info("Start Periodic Processing") 
    last_updated = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    current_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    prev_stats = {}
    try:
        session = DB_SESSION() 
        reports = session.query(Stats).order_by(Stats.last_updated.desc()) 
    
        results_list = [] 
    
        for report in reports: 
            results_list.append(report.to_dict()) 
    
        session.close()
        prev_stats = results_list[0]
        last_updated = prev_stats["last_updated"]

    except:
        prev_stats = {
            "num_ticket_report": 0,
            "num_sale_report": 0,
            "min_sale_report": 100,
            "max_sale_report": 0
        }
        current_timestamp = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

    report_stat = {}
    response = requests.get(app_config["eventstore"]["url"] + "/report/ticket?start_timestamp=" + last_updated + "&end_timestamp=" + current_timestamp)
    #response = requests.get(f'{app_config["eventstore"]["url"]}/report/ticket', params={"start_timestamp": last_updated})
    if response and response.status_code == 200 and len(response.json()) != 0:
        logging.info(f'Return {len(response.json())} numbers of events')
        ticket_result = []
        for report in response.json(): 
            ticket_result.append(report)
            logging.debug(f'Process ticket event with trace id: {report["trace_id"]}')

        report_stat["num_ticket_report"] = prev_stats["num_ticket_report"] + len(ticket_result)

    else:
        report_stat["num_ticket_report"] = prev_stats["num_ticket_report"]
        logging.error(f'Response fail with {response.status_code}')

    response = requests.get(app_config["eventstore"]["url"] + "/report/sale?start_timestamp=" + last_updated + "&end_timestamp=" + current_timestamp)

    if response and response.status_code == 200 and len(response.json()) != 0:
        logging.info(f'Return {len(response.json())} numbers of events')
        sale_result = []
        for report in response.json(): 
            sale_result.append(report)
            logging.debug(f'Process sale event with trace id: {report["trace_id"]}')
        logging.info(sale_result)
        report_stat["num_sale_report"] = prev_stats["num_sale_report"] + len(sale_result)
        prices = [r["price"] for r in sale_result]

        if prev_stats["min_sale_report"] < min(prices):
            report_stat["min_sale_report"] = prev_stats["min_sale_report"]
        else:
            report_stat["min_sale_report"] = min(prices)
        
        if prev_stats["max_sale_report"] > max(prices):
            report_stat["max_sale_report"] = prev_stats["max_sale_report"]
        else:
            report_stat["max_sale_report"] = max(prices)
            
    else:
        logging.error(f'Response fail with {response.status_code}')
        report_stat["num_sale_report"] = prev_stats["num_sale_report"]
        report_stat["min_sale_report"] = prev_stats["min_sale_report"]
        report_stat["max_sale_report"] = prev_stats["max_sale_report"]

    report_stat["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
    logging.debug(report_stat)
    session = DB_SESSION()

    stat = Stats(report_stat['num_ticket_report'],
                       report_stat['num_sale_report'],
                       report_stat['min_sale_report'],
                       report_stat['max_sale_report'],
                       report_stat['last_updated'])

    session.add(stat)

    session.commit()
    session.close()

    logging.debug(f'Updated stat: {report_stat}')
    logging.info(f'End Periodic Processing')

def init_scheduler(): 
    sched = BackgroundScheduler(daemon=True) 
    sched.add_job(populate_stats,    
                  'interval', 
                  seconds=app_config['scheduler']['period_sec']) 
    sched.start()

def get_health():
    return 200

app = connexion.FlaskApp(__name__, specification_dir='') 
app.add_api("openapi.yml",
base_path="/processing",
strict_validation=True,  
validate_responses=True) 
if "TARGET_ENV" not in os.environ or os.environ["TARGET_ENV"] != "test":
    CORS(app.app)
    app.app.config['CORS_HEADERS'] = 'Content-Type'

if __name__ == "__main__": 
    # run our standalone gevent server 
    init_scheduler() 
    app.run(port=8100, use_reloader=False)