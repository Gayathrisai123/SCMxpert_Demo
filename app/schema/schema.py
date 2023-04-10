from pydantic import BaseModel


class User(BaseModel):    
  # schema for a User    
    Username: str
    Email: str
    Password: str

class Shipment(BaseModel):   
  #  A Pydantic schema for a Shipment   
    Shipment_invoicenumber: str
    Container_number: int
    Shipment_description: str
    route: str
    goods: str
    device: str
    expected_delivery_date: str
    po_number: int
    delivery_number: int
    ndc_number: int
    Batch_id: int
    serial_number_of_goods: int
  
    
