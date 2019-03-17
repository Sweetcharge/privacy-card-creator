import requests

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
    if(request_status == 200):
        request_JSON = postRequest.json()
        sessionToken = request_JSON["token"]
        print("Logged in!")

        cardName = input("Enter a card name: ")
        cardLimit = input("Set a card limit: ")

        createCard(sessionToken, cardName, cardLimit)

def createCard(token, name, limit):
    print("Attempting to create some cards...")

    link = "https://privacy.com/api/v1/card"

    card_info = {
        'type': 'SINGLE_USE',
        'spendLimitDuration': 'FOREVER',
        'memo': name,
        'meta':{'hostname':""},
        'style': None,
        'spendLimit': limit,
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
    if(request_status == 200):
        request_JSON = postRequest.json()

        cardName = request_JSON["card"]["memo"]
        cardStatus = request_JSON["accountState"]
        cardID = request_JSON["card"]["cardID"]

        cardNum = request_JSON["card"]["pan"]
        cardCVV = request_JSON["card"]["cvv"]
        monthExp = request_JSON["card"]["expMonth"]
        yearExp = request_JSON["card"]["expYear"]

        cardSpendLimit = request_JSON["card"]["spendLimit"]
        cardType = request_JSON["card"]["type"]

        printCardInfo(cardName, cardStatus, cardID, cardNum, cardCVV, monthExp, yearExp, cardSpendLimit, cardType)
        createAnotherCard(token)
    else:
        request_JSON = postRequest.json()
        print("ERROR: " + request_JSON["message"])

def printCardInfo(name, status, id, number, cvv, month, year, limit, cardType):
    print("\n"+name + " is " + status)
    print("Card ID: "+str(id))
    print("Card #: "+ str(number))
    print("CVV: "+ str(cvv))
    print("Month: "+ str(month))
    print("Year: "+ str(year))
    print("Limit: "+str(limit))
    print("Card type: "+cardType)

def createAnotherCard(sessionToken):
    createAnoter = input("Create another card? ")
    if(createAnoter == "Yes"):
        cardName = input("Enter a card name: ")
        cardLimit = input("Set a card limit: ")

        createCard(sessionToken, cardName, cardLimit)


login()    