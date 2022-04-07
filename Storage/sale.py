from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class Sale(Base):
    """ Sale """

    __tablename__ = "sale"

    id = Column(Integer, primary_key=True)
    sale_id = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    trace_id = Column(Integer, nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, sale_id, price, quantity, trace_id):
        """ Initializes a heart rate reading """
        self.sale_id = sale_id
        self.price = price
        self.quantity = quantity
        self.trace_id = trace_id
        self.date_created = datetime.datetime.now() # Sets the date/time record is created

    def to_dict(self):
        """ Dictionary Representation of a heart rate reading """
        dict = {}
        dict['id'] = self.id
        dict['sale_id'] = self.sale_id
        dict['price'] = self.price
        dict['quantity'] = self.quantity
        dict['trace_id'] = self.trace_id
        dict['date_created'] = self.date_created

        return dict