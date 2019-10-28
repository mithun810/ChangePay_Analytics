from pymongo import MongoClient
from pprint import pprint
import pymongo
import json
client = MongoClient("localhost:27017")
db=client.CHANGEPAY

def no_of_transactions():
    count_tan={}
# print(db.TRANSACTIONS.find( { "status": "COMPLETED"} ).count())
    from datetime import datetime
    fil = {'placedAt':datetime.now()}
    total_amount=0
    for p in db.TRANSACTIONS.find():
        if p["status"] not in count_tan:
            count_tan[p["status"]]=1
        else:
            count_tan[p["status"]]=1+count_tan[p["status"]]
        # print(p["authorizedAmount"])
        total_amount=total_amount+p["authorizedAmount"]
    print("no_of_transactions done")
    count_tan["Total_Transaction"]=total_amount
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
            # mer_name=merchant_name(p["merchantID"])
            if p["merchantID"] not in merchant_count:
                # print("Merchantser::",merchant_name(p["merchantID"]))
                merchant_count[p["merchantID"]]=1
            else:
                merchant_count[p["merchantID"]]=1+merchant_count[p["merchantID"]]
            # print(p)
    print("no_of_orders done",merchant_count)
    merc={}
    for mc in merchant_count:
        merc[merchant_name(mc)]=merchant_count[mc]
    return count_tan, merc

def status_of_SMART_BOX_PANELS():
    count_tan={}
    for p in db.SMART_BOX_PANELS.find():
        if p["panelName"] not in count_tan:
            count_tan[p["panelName"]]={"panelIP":p["panelIP"],"panelLocation":p["panelLocation"]}
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
    # print("qer",quer)
    for p in quer:
        if p == "shopName":
            print("\n===============================\n")
            # pprint(quer)
            return quer[p]

def consolidated_data():
    number_of_orders, merchant_count=no_of_orders()
    today_number_of_orders, today_merchant_count=today_no_of_orders()
    Result={
        "No_of_Transactions":no_of_transactions(),
        "No_of_Orders":number_of_orders,
        "Smart_Box_Status":status_of_SMART_BOX_PANELS(),
        "Customer_Count":customer_count(),
        "Merchant_count":merchant_count,
        "No_of_Orders_Today":today_number_of_orders,
        "No_of_Transactions_Today":no_of_transactions_today(),
        # "AverageTimeforDelivery":average_time_for_delivery()
    }
    gdmc=[]
    for mc in merchant_count:
        gdmc.append({"name":mc,"y":merchant_count[mc]})
    nomc=[]
    for no in number_of_orders:
        nomc.append({"name":no,"y":number_of_orders[no]})
    tomc=[]
    for tno in today_number_of_orders:
        tomc.append({"name":tno,"y":today_number_of_orders[tno]})
    GraphData={
        "No_of_Orders":nomc,
        "Merchant_count":gdmc,
        "No_of_Orders_Today":tomc,
    }
    return Result,GraphData

def today_no_of_orders():
    print("HI")
    count_tan={}
    merchant_count={}
    import time
    millis = int(round(time.time() * 1000))
    print (millis)
    print("timestamp =", millis-864000000)
    fil = {'placedAt':{"$gt":str(millis-86400000)}}
    for p in db.ORDERS.find(fil):
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

def no_of_transactions_today():
    count_tan={}
    # print(db.TRANSACTIONS.find( { "status": "COMPLETED"} ).count())
    import time
    millis = int(round(time.time() * 1000))
    print (millis)
    print("timestamp =", millis-864000000)
    fil = {'placedAt':{"$gt":str(millis-86400000)}}
    total_amount=0
    for p in db.TRANSACTIONS.find(fil):
        if p["status"] not in count_tan:
            count_tan[p["status"]]=1
        else:
            count_tan[p["status"]]=1+count_tan[p["status"]]
        # print(p["authorizedAmount"])
        total_amount=total_amount+float(p["authorizedAmount"])
    print("no_of_transactions done today")
    count_tan["Total_Transaction"]=total_amount
    return count_tan

def average_time_for_delivery():
    merchant_count={}
    i=0
    total_avg_time=0
    # for p in db.ORDERS.find():
    #     if p["status"]:
    #         if p["status"] == "COMPLETED":
    #             total_avg_time=total_avg_time+int(p["completedTime"]-p["placedAt"])
    #             i=i+1
            # print(p)
    return total_avg_time

if __name__ == '__main__':
    print(today_no_of_orders())