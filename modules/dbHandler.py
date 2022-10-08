
from pymongo import MongoClient

import keys

CLUSTER = keys.getURI()
client = MongoClient(CLUSTER)

db = client.AutotaskRPA

ticketsDB = db.tickets
partsDB = db.parts
usersDB = db.users
stockDB = db.stock

#Tickets collection

#Gets Part list from Part database based on ticket's device
def getPartsList(ticketNum):
    ticket = ticketsDB.find_one({'Ticket Number':ticketNum},{'Title':1, '_id':0})
    deviceType = ticket['Title']
    print(deviceType)
    parts = partsDB.find_one({'models':deviceType},{'_id':0,'models':0})

    models = parts.get("MB")

    mobo = models.get(deviceType) 
    parts["Motherboard"] = parts.pop("MB")
    parts.update({"Motherboard": mobo})
    return parts


#Returns ticket dictionary(usually for ticket creation)
def getTicketInfo(ticketNum):
    ticketInfo = ticketsDB.find_one({'Ticket Number':ticketNum},{'_id':0})

    #Adds parts to ticketInfo
    partsList=getPartsList(ticketNum)
    ticketInfo["partsList"]=partsList

    return(ticketInfo)

#Users Collection

def getAllUsers():
    userResults = usersDB.find()
    users =[]
    for user in userResults:
        print("Found user: " + user['name'])
        users.append(user['name'])
    return users

def getUsersPin(selectedUser):
    pinResults = usersDB.find_one({'name':selectedUser},{'id':0,'name':0})
    pin = pinResults['loginPin']
    return pin


def getPartStocks(parts):
    stockAmounts = {}
    print(parts)
    for part in parts:
        stockResults = stockDB.find_one({'Product':part})
        stockAmount = stockResults['Available']
        stockAmounts[part] =stockAmount
    print(str(stockAmounts))
    return stockAmounts

#Testing
#searchEntry = True
# while(searchEntry):  
#     searchEntry=input("Enter your ticket: ")
#     #print(getTicketInfo(searchEntry))
#     test1 = Ticket(getTicketInfo(searchEntry))
#     test1.printTicket()
