from pymongo import MongoClient
from pprint import pprint
import pymongo
import json
client = MongoClient("localhost:27017")
db=client.CHANGEPAY

def no_of_transactions():
    count_tan={}
    # print(db.TRANSACTIONS.find( { "status": "COMPLETED"} ).count())
    for p in db.TRANSACTIONS.find():
        if p["status"] not in count_tan:
            count_tan[p["status"]]=1
        else:
            count_tan[p["status"]]=1+count_tan[p["status"]]
    print("no_of_transactions done")
    return count_tan

def no_of_orders():
    count_tan={}
    merchant_count={}
    for p in db.ORDERS.find():
        if p["status"]:
            if p["status"] not in count_tan:
                count_tan[p["status"]]=1
            else:
                count_tan[p["status"]]=1+count_tan[p["status"]]
            if p["merchantID"] not in merchant_count:
                # print("Merchantser::",merchant_name(p["merchantID"]))
                merchant_count[p["merchantID"]]=1
            else:
                merchant_count[p["merchantID"]]=1+merchant_count[p["merchantID"]]
            # print(p)
    print("no_of_orders done")
    return count_tan, merchant_count

def status_of_SMART_BOX_PANELS():
    count_tan={}
    for p in db.SMART_BOX_PANELS.find():
        if p["panelName"] not in count_tan:
            count_tan[p["panelName"]]={"panelIP":p["panelIP"],"panelLocation":p["panelLocation"],"active":p["active"]}
        else:
            count_tan["Unmarked"]={p["panelName"]:{"panelIP":p["panelIP"]}}
    print("status_of_SMART_BOX_PANELS done")
    return count_tan

def customer_count():
    count_tan={}
    for p in db.CUSTOMERS.find():
        if p["personType"] not in count_tan:
            count_tan[p["personType"]]=1
        else:
            count_tan[p["personType"]]=1+count_tan[p["personType"]]
    print("customer_count done")
    return count_tan

def merchant_name(numb):
    count_tan={}
    quer=db.MERCHANTS.find_one({"merchantID":numb})
    for p in quer:
        if p == "name":
            return quer[p]

def consolidated_data():
    number_of_orders, merchant_count=no_of_orders()
    Result={
        "No_of_Transactions":no_of_transactions(),
        "No_of_Orders":number_of_orders,
        "Smart_Box_Status":status_of_SMART_BOX_PANELS(),
        "Customer_Count":customer_count(),
        "Merchant_count":merchant_count
    }
    return Result

if __name__ == '__main__':
    print(merchant_count())