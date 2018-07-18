import random

# setup Json for game
def setupJson() :
    global playerdata
    playerdata = {}
    playerdata['players'] = []

#setupJson()

# add player to json
def addplayertoJson(ID,Name,lastScore,lastRoll,nextPlay,didPlay,hasWon,numGoes) :
    playerdata['players'].append({    
    'ID': ID ,
    'Name': Name,
    'lastScore': lastScore,
    'lastRoll': lastRoll,
    'Score': "0",
    'nextPlay': nextPlay,
    'didPlay': didPlay,
    'hasWon': hasWon,
    'numGoes': numGoes

    })

# create player dictionary, setup number of players and initial 0 value
def createPlayerDict(numPlayers):
    i = 0
    for i in range(0,numPlayers) :

        if i == 0 :
            nextPlay = True
        else :
            nextPlay = False

        playerKey = "Player" + str(i+1)
        addplayertoJson(i+1,playerKey,0,0,nextPlay,False,False,0)

    print(playerdata)

#createPlayerDict(2)

def setup_players(intent):
    session_attributes = {}
    # pick up number of players from slot in intent
    #playerName = intent['slots']['playername']
    playerName = intent

    # append player to json
    addplayertoJson(len(playerdata['players']),playerName,0,0,False,False,False,0)

    speech_output = playerName + ' has been added to the game, you have ' + str(len(playerdata['players'])) + ' to add another just say, add player with their name' 
    
    # how many players do you have?
    card_title = "Race to One Hundred"
    reprompt_text = ""
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    #card_output = cleanssml(speech_output)

    print(playerdata)
    print(speech_output)
    print(str(len(playerdata['players'])))

#setup_players('Steve')
#setup_players('John')
#setup_players('John')
#setup_players('John')
#setup_players('John')


def setfirstplayer():
    # select random number between 1 and the maximum length of the json file
    selectedplayer = random.randint(1,len(playerdata['players']))

    # udpate player in json file
    playerdata['players'][selectedplayer]['nextPlay'] = True

#setfirstplayer()

def maxPoints():
    global numPoints
    numPoints = 0
    #numPoints = {'Points2Win':20]
    print(numPoints)

#maxPoints()

def looping():
    numLoops = input("Please enter the number of loops you need")

    for i in range(1,int(numLoops)) :
        print(str(i))

looping()