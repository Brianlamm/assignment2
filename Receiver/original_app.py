import connexion 
from connexion import NoContent 
import datetime
import json
import os.path

EVENT_FILE='events.json'
MAX_EVENTS=10
def report_ticket_info(body): 
    """ Receives a ticket info event """ 
    # Implement Here 
    current_datetime = datetime.datetime.now()
    current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    information = f'Your ticket number is {body["ticket_id"]} and you seat number is {body["seat_number"]}, the game is on {body["date"]}, between {body["team1"]} and {body["team2"]}'
    if os.path.isfile(EVENT_FILE):
        with open(EVENT_FILE, "r") as file:
            events = json.loads(file.read())
    else:
        events = []

    if len(events) < MAX_EVENTS:
        events.append({'received_timestamp' : current_datetime_str, 'request_data' : information})
    else:
        while len(events) >= MAX_EVENTS:
            events.pop(0)
        events.append({'received_timestamp' : current_datetime_str, 'request_data' : information})

    json_string = json.dumps(events, indent=4)

    with open(EVENT_FILE, "w") as file:
        file.write(json_string)
    
    return NoContent, 201 
 
 
def report_sale_info(body): 
    """ Receives a sale info event """ 
    # Implement Here 
    events = []
    current_datetime = datetime.datetime.now()
    current_datetime_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")  
    information = "The price for the ticket is {}, and there are only {} tickets left".format(body["price"], body["quantity"])
    
    if os.path.isfile(EVENT_FILE):
        with open(EVENT_FILE, "r") as file:
            events = json.loads(file.read())
    else:
        events = []

    if len(events) < MAX_EVENTS:
        events.append({'received_timestamp' : current_datetime_str, 'request_data' : information})
    else:
        while len(events) >= MAX_EVENTS:
            events.pop(0)
        events.append({'received_timestamp' : current_datetime_str, 'request_data' : information})

    json_string = json.dumps(events, indent=4)

    with open(EVENT_FILE, "w") as file:
        file.write(json_string)
    return NoContent, 201

app = connexion.FlaskApp(__name__, specification_dir='') 
app.add_api("openapi.yml",
strict_validation=True,  
validate_responses=True) 
 
if __name__ == "__main__": 
    app.run(port=8080)