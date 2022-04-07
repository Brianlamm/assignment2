from sqlalchemy import Column, Integer, String, DateTime 
from base import Base 
class Stats(Base): 
    """ Processing Statistics """ 
 
    __tablename__ = "stats" 
 
    id = Column(Integer, primary_key=True) 
    num_ticket_report = Column(Integer, nullable=False) 
    num_sale_report = Column(Integer, nullable=False) 
    min_sale_report = Column(Integer, nullable=True) 
    max_sale_report = Column(Integer, nullable=True) 
    last_updated = Column(String, nullable=False) 
 
    def __init__(self, num_ticket_report, num_sale_report, min_sale_report, max_sale_report, last_updated): 
        """ Initializes a processing statistics objet """ 
        self.num_ticket_report = num_ticket_report 
        self.num_sale_report = num_sale_report 
        self.min_sale_report = min_sale_report 
        self.max_sale_report = max_sale_report 
        self.last_updated = last_updated 
 
    def to_dict(self): 
        """ Dictionary Representation of a statistics """ 
        dict = {} 
        dict['num_ticket_report'] = self.num_ticket_report 
        dict['num_sale_report'] = self.num_sale_report 
        dict['min_sale_report'] = self.min_sale_report 
        dict['max_sale_report'] = self.max_sale_report 
        dict['last_updated'] = self.last_updated
 
        return dict