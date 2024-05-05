from pydantic import BaseModel
from typing import Optional, List
from uuid import UUID, uuid4
from enum import Enum
import pymongo
from pymongo import MongoClient
from datetime import datetime
from abc import ABC, abstractmethod

class MongoDBManager:                                           # Encapsulation
    DatabaseName = "Online-Pharmacy"
    def __init__(self):
        try:
            self.client = MongoClient('mongodb+srv://vishvkaneria:myD82721ZAaVpv6A@myproject.vgagynf.mongodb.net/?retryWrites=true&w=majority&appName=MyProject')
            self.db = self.client[self.DatabaseName] 
        except Exception as e:
            print(f"Failed to connect to MongoDB: {e}")

    def get_collection(self, collection_name):
        try:
            collection = self.db[collection_name]
            print(f"Retrieved collection: {collection_name}")
            return collection
        except Exception as e:
            print(f"Error retrieving collection {collection_name}: {e}")
            return None


class Repository(ABC):                                          # Polymorphism
    @abstractmethod
    def add(self, data):
        pass

    @abstractmethod
    def remove(self, name):
        pass

    @abstractmethod
    def update(self, filter_query, update_data):
        pass

    @abstractmethod
    def get(self, filter_query):
        pass

    @abstractmethod
    def list_all(self):
        pass


class ProductRepository(Repository):                            # Abstraction
    def __init__(self, collection):
        self.collection = collection

    def add(self, product_data):                                # add product
        self.collection.insert_one(product_data)

    def remove(self, product_name):                             # remove product
        return self.collection.delete_one({"ProductName": product_name})

    def update(self, filter_query, update_data):                # update product details
        return self.collection.update_one(filter_query, update_data)

    def get(self, filter_query):                                # get single product
        return self.collection.find_one(filter_query)

    def list_all(self):                                         # get all products
        return list(self.collection.find())


class UserRepository(Repository):
    def __init__(self, collection):
        self.collection = collection

    def add(self, user_data):
        self.collection.insert_one(user_data)

    def remove(self, email):
        return self.collection.delete_one({"Email": email})

    def update(self, filter_query, update_data):
        return self.collection.update_one(filter_query, update_data)

    def get(self, filter_query):
        return self.collection.find_one(filter_query)

    def list_all(self):
        return list(self.collection.find())


class Gender(str, Enum):
    male = "Male"
    female = "Female"
    default = ""


class Products(BaseModel):
    _id: Optional[str] = uuid4()
    ProductImage: Optional[str]
    ProductName: str
    ProductPrice: Optional[str]
    ProductDescription: Optional[str]
    ProductRatings: Optional[str]
    Category: str


class OrderProducts(BaseModel):
    Products: Products
    Quantity: int


class Orders(str, Enum):
    OrderId: Optional[str] = uuid4()
    OrderDate: str
    Total: float
    Products: List[OrderProducts]


class PersonDetails(BaseModel):
    _id: Optional[UUID] = uuid4()
    Email: str
    ContactNumber: Optional[str]
    FName: Optional[str]
    LName: Optional[str]
    Street: Optional[str]
    City: Optional[str]
    State: Optional[str]
    Pincode: Optional[str]
    Gender: Optional[str]
    Orders: Optional[List[Orders]]


class Users(PersonDetails):                                     # Inheritance
    DateofBirth: Optional[str]
    Gender: Gender
    Password: str


class CardDetails(BaseModel):
    CardType: str
    Owner: str
    CardNumber: str
    CardExpiry: str
    CVV: str


class Feedback(BaseModel):
    Name: str
    Email: str
    Message: str


class Pharmacists(PersonDetails):
    Store: str