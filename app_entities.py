from ORM import AbstractRecord

class Customer(AbstractRecord):
    customer_id: int
    name: str
    email: str
    password: str
    phone: str
    address: str

class Package(AbstractRecord):
    package_id: int
    customer_id: int
    source: str
    destination: str
    current_location: str
    status: str
    weight: float
    pick_up_date: str
    delivery_option: str
    expected_delivery_date: str
    cost: float
