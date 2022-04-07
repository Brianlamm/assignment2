from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class Ticket(Base):
    """ Ticket """

    __tablename__ = "ticket"

    id = Column(Integer, primary_key=True)
    ticket_id = Column(String(250), nullable=False)
    date = Column(String(100), nullable=False)
    team1 = Column(String(100), nullable=False)
    team2 = Column(String(100), nullable=False)
    seat_number = Column(Integer, nullable=False)
    trace_id = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, ticket_id, date, team1, team2, seat_number, trace_id):
        """ Initializes a blood pressure reading """
        self.ticket_id = ticket_id
        self.date = date
        self.team1 = team1
        self.team2 = team2
        self.seat_number = seat_number
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['ticket_id'] = self.ticket_id
        dict['date'] = self.date
        dict['team1'] = self.team1
        dict['team2'] = self.team2
        dict['seat_number'] = self.seat_number
        dict['trace_id'] = self.trace_id
        dict['date_created'] = self.date_created

        return dict