from pymongo import MongoClient

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
    # print("no_of_transactions done")
    count_tan["Total_Transaction"]=total_amount
    return count_tan

def no_of_orders():
    count_tan={}
    merchant_count = {}
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
    # print("no_of_orders done",merchant_count)
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
    # print("status_of_SMART_BOX_PANELS done")
    return count_tan

def customer_count():
    count_tan={}
    for p in db.CUSTOMERS.find():
        if p["personType"] not in count_tan:
            count_tan[p["personType"]]=1
        else:
            count_tan[p["personType"]]=1+count_tan[p["personType"]]
    # print("customer_count done")
    return count_tan

def merchant_name(numb):
    count_tan={}
    quer=db.MERCHANTS.find_one({"merchantID":numb})
    # print("qer",quer)
    for p in quer:
        if p == "shopName":
            # print("\n===============================\n")
            # pprint(quer)
            return quer[p]

def findAvgDeliveryTime(startDate = 1571110200000, endDate = 1573788600000):
    from datetime import datetime
    date = {}
    while startDate < endDate:
        orderCountForDay = db.ORDERS.count_documents({"placedAt" : {"$gt" : str(startDate), "$lt" : str(startDate + 86400000)}, "status" : "COMPLETED"})
        # print(orderCountForDay)
        deliveryTime = 0
        for order in db.ORDERS.find({"placedAt" : {"$gt" : str(startDate), "$lt" : str(startDate + 86400000)}, "status" : "COMPLETED"}):
            deliveryTime += ((int(order["completedTime"]) - int(order["placedAt"])) / 60000)
        avgDeliveryTime = deliveryTime / orderCountForDay
        dateTime = datetime.fromtimestamp(startDate / 1000)
        date[dateTime.strftime("%A %d %B %Y")] = avgDeliveryTime
        startDate += 86400000
    # print("End.")
    return date

def findTopSellingMerchant(startDate = 1571110200000):
    from datetime import datetime
    endDate = startDate + 2419200000
    date = {}
    count = {}
    while startDate < endDate:
        for order in db.ORDERS.find({"placedAt" : {"$gt" : str(startDate), "$lt" : str(startDate + 2419200000)}, "status" : "COMPLETED"}):
            if order["merchantID"] not in count:
                count[order["merchantID"]] = 1
            else:
                count[order["merchantID"]] += 1
        maxKey = max(count, key = count.get)
        merchant = db.MERCHANTS.find_one({"merchantID" : maxKey}, {"shopName" : 1})
        print(merchant["shopName"])
        dateTime = datetime.fromtimestamp(startDate / 1000)
        # for merchants in merchant:
        date[dateTime.strftime("%B %Y")] = merchant["shopName"]
        # print(merchants["shopName"])
        startDate += 2419200000
    return date

def findAvgTimeFromSB(startDate = 1571110200000, endDate = 1573788600000):
    from datetime import datetime
    date = {}
    while startDate < endDate:
        numberOfPickUpFromSB = 0
        sbDeliveryTime = 0
        for order in db.ORDERS.find({"placedAt" : {"$gt" : str(startDate), "$lt" : str(startDate + 86400000)}, "status" : "COMPLETED"}):
            if order["holders"] is not None and len(order["holders"]) == 3:
                if order["holders"][2]["holder"] == "SMART_BOX":
                    if int(order["holders"][2]["orderDropOffTime"]) is not None and int(order["holders"][2]["orderPickUpTime"]) is not None and (int(order["holders"][2]["orderDropOffTime"]) - int(order["holders"][2]["orderPickUpTime"]) < 18000000):
                        sbDeliveryTime += ((int(order["holders"][2]["orderDropOffTime"]) - int(order["holders"][2]["orderPickUpTime"])) / 60000)
                        numberOfPickUpFromSB += 1
        dateTime = datetime.fromtimestamp(startDate / 1000)
        date[dateTime.strftime("%m/%d/%Y, %H:%M:%S")] = (sbDeliveryTime / numberOfPickUpFromSB)
        startDate += 86400000
    return date

def findReturning(startDate = 1571110200000, endDate = 1573788600000):
    from datetime import datetime
    date = {}
    while startDate < endDate:
        totalUserCount = db.ORDERS.count_documents({"placedAt" : { "$gt" : str(startDate - 86400000), "$lt" : str(startDate)}, "status" : "COMPLETED"})
        # print(totalUserCount)
        previousUsers = []
        for order in db.ORDERS.find({"placedAt" : { "$gt" : str(startDate - 86400000) , "$lt" : str(startDate)}, "status" : "COMPLETED"}):
            previousUsers.append(order["customerPhoneNumber"])
        currentUsers = []
        for order in db.ORDERS.find({"placedAt" : { "$gt" : str(startDate) , "$lt" : str(startDate + 86400000)}, "status" : "COMPLETED"}):
            currentUsers.append(order["customerPhoneNumber"])
        currentUsers = set(currentUsers)
        previousUsers = set(previousUsers)
        commonUsers = currentUsers.intersection(previousUsers)
        # print(len(commonUsers))
        dateTime = datetime.fromtimestamp(startDate / 1000)
        date[dateTime.strftime("%m/%d/%Y, %H:%M:%S")] = ((len(commonUsers) / totalUserCount) * 100)
        startDate += 86400000
    return date

def findDailyActiveUsers(startDate = 1571110200000, endDate = 1573788600000):
    import time
    from datetime import datetime
    today = round(time.time())
    totalUserCount = db.ORDERS.count_documents({"placedAt" : { "$gt" : str(startDate), "$lt" : str(today)}, "status" : "COMPLETED"})
    date = {}
    while startDate < endDate:
        uniqueUsers = []
        for order in db.ORDERS.find({"placedAt" : { "$gt" : str(startDate) , "$lt" : str(startDate + 86400000)}, "status" : "COMPLETED"}):
            uniqueUsers.append(order["customerPhoneNumber"])
        dateTime = datetime.fromtimestamp(startDate / 1000)
        date[dateTime.strftime("%m/%d/%Y, %H:%M:%S")] = (len(set(uniqueUsers))) 
        startDate += 86400000
    # print("Daily Acitve User : Done")
    return date

def findMonthlyActiveUsers(startDate = 1571110200000):
    import time
    from datetime import datetime
    today = round(time.time())
    totalUserCount = db.ORDERS.count_documents({"placedAt" : { "$gt" : str(startDate), "$lt" : str(today)}, "status" : "COMPLETED"})

    date = {}
    endDate = startDate + 2419200000

    while startDate < endDate:
        uniqueUsers = []
        for order in db.ORDERS.find({"placedAt" : { "$gt" : str(startDate) , "$lt" : str(startDate + 2419200000)}, "status" : "COMPLETED"}):
            uniqueUsers.append(order["customerPhoneNumber"])
        dateTime = datetime.fromtimestamp(startDate / 1000)
        date[dateTime.strftime("%m/%d/%Y, %H:%M:%S")] = (len(set(uniqueUsers))) 
        startDate += 2419200000
    # print("Mothly Acitve User : Done")
    return date

def findAvgRevenuePerUser(startDate = 1571110200000, endDate = 1573788600000):
    import time
    from datetime import datetime
    today = round(time.time())
    totalRevenue = 0
    date = {}
    endDate = startDate + 2419200000

    for order in db.ORDERS.find({"placedAt" : {"$gt" : str(startDate), "$lt" : str(today)}, "status" : "COMPLETED"}):
        if not order["serviceSpecificData"]:
            continue
        else:
            totalRevenue += order["serviceSpecificData"]["DELIVERY_CHARGE"]

    while startDate < endDate:
        uniqueUsers = []
        for order in db.ORDERS.find({"placedAt" : { "$gt" : str(startDate) , "$lt" : str(startDate + 2419200000)}, "status" : "COMPLETED"}):
            uniqueUsers.append(order["customerPhoneNumber"])
        dateTime = datetime.fromtimestamp((startDate) / 1000)
        date[dateTime.strftime("%m/%d/%Y, %H:%M:%S")] = (totalRevenue / len(set(uniqueUsers)))
        startDate += 2419200000
    return date

def consolidated_data():
    number_of_orders, merchant_count=no_of_orders()
    today_number_of_orders, today_merchant_count=today_no_of_orders()
    dailyActiveUsers = findDailyActiveUsers()
    monthlyActiveUsers = findMonthlyActiveUsers()
    avgTimeFromSB = findAvgTimeFromSB()
    avgRevenuePerUser = findAvgRevenuePerUser()
    topSellingMerchant = findTopSellingMerchant()
    print(merchant_count)
    print(findAvgDeliveryTime())
    Result={
        "No_of_Transactions":no_of_transactions(),
        "No_of_Orders":number_of_orders,
        "Smart_Box_Status":status_of_SMART_BOX_PANELS(),
        "Customer_Count":customer_count(),
        "Merchant_count":merchant_count,
        "No_of_Orders_Today":today_number_of_orders,
        "No_of_Transactions_Today":no_of_transactions_today(),
        "DailyActiveUsers": {},
        "MonthlyActiveUsers": {},
        "AvgTimeFromSB": {},
        "AvgRevenuePerUser": {},
        "TopSellingMerchant": {}
        # "AverageTimeforDelivery":average_time_for_delivery()
        # "Daily Active Users" : dailyActiveUsers
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
    dauc = []
    for dau in dailyActiveUsers:
        dauc.append({"name" : dau, "y" : dailyActiveUsers[dau]})
    mauc = []
    for mau in monthlyActiveUsers:
        mauc.append({"name": mau, "y": monthlyActiveUsers[mau]})
    avsb = []
    for asb in avgTimeFromSB:
        avsb.append({"name": asb, "y": avgTimeFromSB[asb]})
    arpu = []
    for arp in avgRevenuePerUser:
        arpu.append({"name": arp, "y": avgRevenuePerUser[arp]})
    tslm = []
    for tsm in topSellingMerchant:
        tslm.append({"name": tsm, "y": topSellingMerchant[tsm]})
    # print("tomcc\n",tomc)
    # print("\daucn",dauc)
    GraphData={
        "No_of_Orders":nomc,
        "Merchant_count":gdmc,
        "No_of_Orders_Today":tomc,
        "DailyActiveUsers" : dauc,
        "MonthlyActiveUsers": mauc,
        "AvgTimeFromSB": avsb,
        "AvgRevenuePerUser": arpu,
        "TopSellingMerchant": tslm
    }
    return Result,GraphData

def today_no_of_orders():
    # print("HI")
    count_tan={}
    merchant_count={}
    import time
    millis = int(round(time.time() * 1000))
    # print (millis)
    # print("timestamp =", millis-864000000)
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
    # print("no_of_orders done")
    return count_tan, merchant_count

def no_of_transactions_today():
    count_tan={}
    # print(db.TRANSACTIONS.find( { "status": "COMPLETED"} ).count())
    import time
    millis = int(round(time.time() * 1000))
    # print (millis)
    # print("timestamp =", millis-864000000)
    fil = {'placedAt':{"$gt":str(millis-86400000)}}
    total_amount=0
    for p in db.TRANSACTIONS.find(fil):
        if p["status"] not in count_tan:
            count_tan[p["status"]]=1
        else:
            count_tan[p["status"]]=1+count_tan[p["status"]]
        # print(p["authorizedAmount"])
        total_amount=total_amount+float(p["authorizedAmount"])
    # print("no_of_transactions done today")
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
    print(findTopSellingMerchant())