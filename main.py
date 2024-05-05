from fastapi import FastAPI, Depends, HTTPException
from models import Products, Users, Pharmacists, CardDetails, Feedback
#from pymongo import MongoClient
#from typing import Dict, Any
#import json
#from uuid import UUID, uuid4
from models import MongoDBManager, ProductRepository, UserRepository
from datetime import datetime

app = FastAPI()

mongo_manager = MongoDBManager()
ProdCollection = mongo_manager.get_collection('ProductDetails')
UserCollection = mongo_manager.get_collection('UserDetails')
PharmacistCollection = mongo_manager.get_collection('PharmacistDetails')
CardCollection = mongo_manager.get_collection('CardDetails')
FeedbackCollection = mongo_manager.get_collection('Feedbacks')

today = datetime.now().strftime("%m-%y")

# Instantiate repositories
product_repository = ProductRepository(ProdCollection)
user_repository = UserRepository(UserCollection)

# default
@app.get("/")
async def root():
    return {"Hello" : "World"}


# get all data
@app.get("/products")
async def fetchAllProducts():
    data_cursor = product_repository.list_all()        #data_cursor = ProdCollection.find()
    
    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return data_list


# add product data - only admin has access to this
@app.post("/products/add")
async def addProducts(product: Products):
    try:
        product_repository.add(product.dict())          #ProdCollection.insert_one(product.dict())
        return {"id": product._id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# remove product data - only admin has access to this
@app.post("/products/remove")
async def removeProducts(product: Products):
    try:
        result = product_repository.remove(product.ProductName)     #result = ProdCollection.delete_one({ "ProductName": product.ProductName })
        if result.deleted_count == 1:
            return {"Deleted Successfully"}
        else:
            return {"No matching record found"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# update product data - only admin has access to this
@app.post("/products/update")
async def updateProducts(product: Products):
    
    filter_query = {"ProductName": {"$regex": product.ProductName, "$options": "i"}}

    if product.ProductPrice != "":
        try:
            update_data = {
                "$set": {
                    "ProductPrice": product.ProductPrice
                }
            }
            
            result = product_repository.update(filter_query, update_data)    #result = ProdCollection.update_one(filter_query, update_data)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        if result.modified_count == 1:
            return {"Updated Successfully"}
        else:
            return {"No matching record found"}
    
    elif product.ProductDescription != "":
        try:
            update_data = {
                "$set": {
                    "ProductDescription": product.ProductDescription
                }
            }
            
            result = product_repository.update(filter_query, update_data)    #result = ProdCollection.update_one(filter_query, update_data)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        if result.modified_count == 1:
            return {"Updated Successfully"}
        else:
            return {"No matching record found"}
    
    elif product.ProductRatings != "":
        try:
            update_data = {
                "$set": {
                    "ProductRatings": product.ProductRatings
                }
            }
            
            result = product_repository.update(filter_query, update_data)    #result = ProdCollection.update_one(filter_query, update_data)

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        if result.modified_count == 1:
            return {"Updated Successfully"}
        else:
            return {"No matching record found"}
        
    elif product.Category != "":
        try:
            update_data = {
                "$set": {
                    "Category": product.Category
                }
            }
            
            result = product_repository.update(filter_query, update_data)    #result = ProdCollection.update_one(filter_query, update_data)
        
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        if result.modified_count == 1:
            return {"Updated Successfully"}
        else:
            return {"No matching record found"}


# get specific product data
@app.get("/products/prod={product_name}")
async def fetchOneProduct(product_name: str):

    filter_query = { "ProductName": { "$regex": product_name, "$options": 'i' } }
    data_cursor = product_repository.get(filter_query)
    
    ProdCollection.find()

    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return list(data_list)


# get category based product
@app.get("/products/cate={category}")
async def fetchCatProducts(category: str):
    data_cursor = ProdCollection.find({
        "Category": {
            "$regex": category,
            "$options": 'i'
        }
    })

    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return list(data_list)


# user registration
@app.post("/users/add")
async def registerUser(user: Users):
    try:
        user_repository.add(user.dict())                # UserCollection.insert_one(user.dict())
        return {"id": user._id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# get user details
@app.get("/users/{userEmail}")
async def getUserDetails(userEmail: str):
    data_cursor = UserCollection.find({
        "Email": {
            "$regex": userEmail,
            "$options": 'i'
        }
    })
    
    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return data_list


# payment check
@app.post("/paymentCheck/")
async def checkPayment(cardDetails: CardDetails):
    
    data_cursor = CardCollection.find({ "CardNumber": cardDetails.CardNumber })
    
    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    repsonse = False

    try:
        if data_list[0]['Owner'] == cardDetails.Owner:
            if datetime.strptime(data_list[0]['CardExpiry'], '%m-%y') >= datetime.strptime(today, '%m-%y') and data_list[0]['CardExpiry'] == cardDetails.CardExpiry:
                if data_list[0]['CVV'] == cardDetails.CVV:
                    repsonse = True
    except Exception as e:
        print(e)

    return repsonse


# cart add
@app.get("/addCart/{product_id}")
async def addCart(product_id: str):
    
    data_cursor = ProdCollection.find({ "_id": product_id })

    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return data_list


# feedback
@app.post("/feedback/")
async def feedbackAdd(feedback: Feedback):
    try:
        FeedbackCollection.insert_one(feedback.dict())
        return True
    except Exception as e:
        return False


'''
# pharamacist registration
@app.post("/pharamacist/add")
async def registerPharamacist(pharamacist: Pharmacists):
    try:
        PharmacistCollection.insert_one(pharamacist.dict())
    except Exception as e:
        print(e)
    return {"id": pharamacist._id}


# get pharamacist details
@app.get("/pharamacist/{phmEmail}")
async def getUserDetails(phmEmail: str):
    
    data_cursor = PharmacistCollection.find({
        "PhmEmail": {
            "$regex": phmEmail,
            "$options": 'i'
        }
    })

    data_list = []
    for document in data_cursor:
        document["_id"] = str(document["_id"])
        data_list.append(document)

    return list(data_list)
'''