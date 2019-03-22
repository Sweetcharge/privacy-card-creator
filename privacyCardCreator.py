import requests, time

cardListLength = 0

def login():
    print("Logging in...")
    link = "https://privacy.com/auth/local"

    ############# PUT YOUR INFO BELOW #############
    userInfo = {
        'email': '',
        'password': '',
        'extensionInstalled': 'false',
        'captchaResponse': None
    }

    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
		'content-type': 'application/json;charset=UTF-8',
        'connection': 'keep-alive',
        'cookie': 'sessionID=3a809cfb-1176-4b43-a134-7cd1da832888; experiments=CiQ2MmFiZjUwNS0zN2Y0LTQyOTgtOWVjZi0yZWQ0MDY3MmY3YjkSJhIRc2hvdWxkU2tpcENvbmZpcm0qEXNob3dDbGFzc2ljRnVubmVs; ETag="ps26i5unssI="'
    }

    postRequest = requests.post(url=link, headers=headers, json=userInfo)
    request_status = postRequest.status_code
    request_JSON = postRequest.json()
    if(request_status == 200):
        sessionToken = request_JSON["token"]
        print("Logged in!\n\n")
        mainMenu(sessionToken)
    else:
        print(request_JSON)

def mainMenu(token):
        print("Welcome, your current cards are:\n")
        showCurrentCards(token)
        print("\n1. Create a new card\n2. Delete a card\n3. Exit")
        userChoice = input("What would you like to do?: ")

        if(int(userChoice) == 1):
            createCard(token)
        elif(int(userChoice) == 2):
            deleteCard(token)
            mainMenu(token)
        elif(int(userChoice) == 3):
            print("Goodbye!")
        else:
            print("That's not a valid option")
            mainMenu(token)

def showCurrentCards(token):
    global cardListLength
    link = "https://privacy.com/api/v1/card/"

    newAuth = "Bearer "+token
    newCookie = 'sessionID=3a809cfb-1176-4b43-a134-7cd1da832888; experiments=CiQ2MmFiZjUwNS0zN2Y0LTQyOTgtOWVjZi0yZWQ0MDY3MmY3YjkSJhIRc2hvdWxkU2tpcENvbmZpcm0qEXNob3dDbGFzc2ljRnVubmVs; ETag="ps26i5unssI="; token='+token

    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
		'content-type': 'application/json;charset=UTF-8',
        'connection': 'keep-alive',
        'authorization': newAuth,
        'cookie': newCookie
    }

    getRequest = requests.get(url=link, headers=header)
    requestJSON = getRequest.json()
    cardList = requestJSON["cardList"]
    
    for cardIndex in range(len(cardList)):
        if(cardList[cardIndex]["state"] == "OPEN"):
            openCardName = cardList[cardIndex]["memo"]
            print(str(cardIndex+1)+") "+openCardName)

def createCard(token):
    cardName = input("Enter a card name: ")
    cardLimit = input("Set a card limit: ")
    print("Attempting to create some cards...")

    link = "https://privacy.com/api/v1/card"

    card_info = {
        'type': 'SINGLE_USE',
        'spendLimitDuration': 'FOREVER',
        'memo': cardName,
        'meta':{'hostname':""},
        'style': None,
        'spendLimit': cardLimit,
        'reloadable': 'false'
    }

    newAuth = "Bearer "+token
    newCookie = 'sessionID=3a809cfb-1176-4b43-a134-7cd1da832888; experiments=CiQ2MmFiZjUwNS0zN2Y0LTQyOTgtOWVjZi0yZWQ0MDY3MmY3YjkSJhIRc2hvdWxkU2tpcENvbmZpcm0qEXNob3dDbGFzc2ljRnVubmVs; ETag="ps26i5unssI="; token='+token

    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
		'content-type': 'application/json;charset=UTF-8',
        'connection': 'keep-alive',
        'authorization': newAuth,
        'cookie': newCookie
    }

    postRequest = requests.post(url=link, headers=header, json=card_info)
    request_status = postRequest.status_code
    request_JSON = postRequest.json()
    if(request_status == 200):
        cardName = request_JSON["card"]["memo"]
        cardStatus = request_JSON["accountState"]

        cardNum = request_JSON["card"]["pan"]
        cardCVV = request_JSON["card"]["cvv"]
        monthExp = request_JSON["card"]["expMonth"]
        yearExp = request_JSON["card"]["expYear"]

        cardSpendLimit = request_JSON["card"]["spendLimit"]
        cardType = request_JSON["card"]["type"]

        printCardInfo(cardName, cardStatus, cardNum, cardCVV, monthExp, yearExp, cardSpendLimit, cardType)
        createAnotherCard(token)
    else:
        print("ERROR: " + request_JSON["message"])
    
def printCardInfo(name, status, number, cvv, month, year, limit, cardType):
    print("\n"+name + " is " + status)
    print("Card #: "+ str(number))
    print("CVV: "+ str(cvv))
    print("Month: "+ str(month))
    print("Year: "+ str(year))
    print("Limit: "+str(limit))
    print("Card type: "+cardType)


def createAnotherCard(token):
    createAnoter = input("Create another card? ")
    if(createAnoter.lower() == "yes"):
        print("\nWelcome, your current cards are:\n")
        showCurrentCards(token)
        createCard(token)
    else:
        print("Goodbye!")
        mainMenu(token)

def deleteCard(token):
    showCurrentCards(token)
    cardToDelete = input("Which card would you like to delete? (i.e. 1): ")
    cardID = getCardID(token, int(cardToDelete)-1)
    removeCard(token, cardID)

def getCardID(token, target_cardIndex):
    link = "https://privacy.com/api/v1/card/"

    newAuth = "Bearer "+token
    newCookie = 'sessionID=3a809cfb-1176-4b43-a134-7cd1da832888; experiments=CiQ2MmFiZjUwNS0zN2Y0LTQyOTgtOWVjZi0yZWQ0MDY3MmY3YjkSJhIRc2hvdWxkU2tpcENvbmZpcm0qEXNob3dDbGFzc2ljRnVubmVs; ETag="ps26i5unssI="; token='+token

    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
		'content-type': 'application/json;charset=UTF-8',
        'connection': 'keep-alive',
        'authorization': newAuth,
        'cookie': newCookie
    }

    getRequest = requests.get(url=link, headers=header)
    requestJSON = getRequest.json()
    cardList = requestJSON["cardList"]

    for cardIndex in range(len(cardList)):
        if(cardList[cardIndex]["state"] == "OPEN" and target_cardIndex == cardIndex):
            targetCardID = cardList[cardIndex]["cardID"]
            return targetCardID
    
def removeCard(token, id):
    link = "https://privacy.com/api/v1/card/"+id+"/close"

    newAuth = "Bearer "+token
    newCookie = 'sessionID=3a809cfb-1176-4b43-a134-7cd1da832888; experiments=CiQ2MmFiZjUwNS0zN2Y0LTQyOTgtOWVjZi0yZWQ0MDY3MmY3YjkSJhIRc2hvdWxkU2tpcENvbmZpcm0qEXNob3dDbGFzc2ljRnVubmVs; ETag="ps26i5unssI="; token='+token

    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36',
		'content-type': 'application/json;charset=UTF-8',
        'connection': 'keep-alive',
        'authorization': newAuth,
        'cookie': newCookie
    }

    postRequest = requests.post(url=link, headers=header)
    request_status = postRequest.status_code
    request_JSON = postRequest.json()
    if(request_status == 200):
        print("Card successfully deleted!\n")
    else:
        print("ERROR: "+request_JSON)

# Start the program
login()    