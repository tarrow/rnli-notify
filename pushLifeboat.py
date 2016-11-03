import requests,json,os,time

'''
Test launch station and push notification if matches supplied shortName
'''
def launchMatcher(shout, station):
    if shout['shortName']==station:
        pushNotification(shout['launchDate'])

'''
Make a pushbullet notification
'''
def pushNotification(time):
    payload = {
        'type':'note',
        'channel_tag':'foweylifeboatunofficial',
        'title':'Lifeboat Launch',
        'body':'Lifeboat Launched At '+time
        }
    headers = {'Access-Token':os.environ['PB_KEY']}
    r=requests.post("https://api.pushbullet.com/v2/pushes", data=payload, headers=headers)
    print(r.text)
'''
Return set of values of a list of json object
'''
def makeSet(listInput):
    listOutput=list()
    for entry in listInput:
        listOutput.append(json.dumps(entry, sort_keys=True))
    return set(listOutput)
while True:
    try:
        with open('oldShouts.json') as oldShoutsFile:
            oldShouts=makeSet(json.load(oldShoutsFile))
    except (OSError, ValueError):
        oldShouts = set()
        pass
    rawNewShouts = requests.get("http://services.rnli.org/api/launches?numberOfShouts=10").json()
    newShouts = makeSet(rawNewShouts)
    differentShouts=newShouts-oldShouts

    for shoutString in differentShouts:
        shout = json.loads(shoutString)
        launchMatcher(shout, "Fowey")

    with open('oldShouts.json', 'w') as oldShoutsFile:
        newShoutsList=[]
        for entry in newShouts:
            newShoutsList.append(json.loads(entry))
        json.dump(newShoutsList, oldShoutsFile)
    time.sleep(600)
