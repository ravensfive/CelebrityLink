# main python program
import json, re, random

# lambda function handler - including specific reference to our skill
def lambda_handler(event, context):
    # if skill ID does not match my ID then raise error
    if (event["session"]["application"]["applicationId"] !=
            "amzn1.ask.skill.32109323-a7d4-4018-b21e-13f46c4223b5"):
        raise ValueError("Invalid Application ID")

    # test if session is new
    if event["session"]["new"]: 
        on_session_started({"requestId": event["request"]["requestId"]}, event["session"])

    # test and set session status
    if event["request"]["type"] == "LaunchRequest":
        return on_launch(event["request"], event["session"])
    elif event["request"]["type"] == "IntentRequest":
        return on_intent(event["request"], event["session"])
    elif event["request"]["type"] == "SessionEndedRequest":
        return on_session_ended(event["request"], event["session"])

# define session start
def on_session_started(session_started_request, session):
    print ("Starting new session")

# define session launch
def on_launch(launch_request, session):
    return get_welcome_response()

# control intent call 
def on_intent(intent_request, session):
    intent = intent_request["intent"]
    intent_name = intent_request["intent"]["name"]

    if intent_name == "GetInstructions":
        return get_instructions()
    elif intent_name == "SetupGame":
        return setup_players(intent)
    elif intent_name == "PlayTurn" or intent_name == "StartGame":
        return play_turn(intent)
    elif intent_name == "ResetGame":
        return reset_game('delete')
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    elif intent_name == "AMAZON.FallbackIntent":
        return fall_back_reponse()
    else:
        raise ValueError("Invalid intent")

# define end session
def on_session_ended(session_ended_request, session):
    print("Ending session")

# handle end of session
def handle_session_end_request():
    card_title = "Thanks"
    speech_output = "See you soon"
    should_end_session = True
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response({}, build_speechlet_response(card_title, speech_output, card_output, None, should_end_session))

# define welcome intent
def get_welcome_response():
    session_attributes = {}
    # setup new json
    setupgameJson()
    setupplayerJson()
    
    # set default value for numPoints
    card_title = "Welcome"
    speech_output = "Welcome to Celebrity Link, to hear the instructions just say, I need the instructions, if you are ready to play then say setup game followed by the players names"
    # you must say the name of a famous celebrity, the next player must then say the name of celebrity that's surname begins with the last letter of the previous celebrities, if you mention a celebrity whose first name starts with the same letter as the surname, then the order reverses"
    reprompt_text = "Welcome to Celebrity Link, to hear the instructions just say, I need the instructions, if you are ready to play then say setup game followed by the players names"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

        # define welcome intent
def fall_back_reponse():
    session_attributes = {}    
    # set default value for numPoints
    card_title = "Welcome"
    speech_output = "Welcome to Celebrity Link, are you ready to start or do you need the instructions"
    # you must say the name of a famous celebrity, the next player must then say the name of celebrity that's surname begins with the last letter of the previous celebrities, if you mention a celebrity whose first name starts with the same letter as the surname, then the order reverses"
    reprompt_text = "Welcome to Celebrity Link, are you ready to start or do you need the instructions"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define welcome intent
def get_instructions():
    session_attributes = {}
    # set default value for numPoints
    card_title = "Welcome"
    speech_output = "You must say the name of a famous celebrity, the next player must then say the name of a celebrity that's first name begins with the first letter of the previous celebrities surname, if you say a celebrity whose first name starts with the same letter as their surname, the order reverses"
    reprompt_text = "Welcome to Celebrity Link, are you ready to start or do you need the instructions"
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define setup game
def setup_players(intent):
    # setup session attributes
    session_attributes = {}

    speech_output = ""

    # pick up number of players from slot in intent
    playerString = intent['slots']['players']['value'].split()

    for part in playerString:
        if part.lower() != 'and':
            # append player to json
            addplayertoJson(len(playerdata['players'])+1,part,0,0,False,False,False,0,0)
            speech_output = speech_output + " " + part.title()
    
    speech_output = "I've added " + speech_output + ", you can add more by saying add followed by the players name, or to start say start game"
    card_title = "Players Added"
    reprompt_text = ""
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))

# define play turn intent
def play_turn(intent):
    global directionType
    # set up session attributes
    session_attributes = {}

    # setup temporary variables
    speech_output = ""
    playerselected = False
    celebName = ""
    
    # test if a player has already been selected at random 
    #if 'ID' in playerdata['players']:
    for p in playerdata['players'] :
        if p['nextPlay'] == True:
                playerselected = True

    # if no players have been added then push back welcome message
    print(len(playerdata['players']))
    print(playerdata)

    if len(playerdata['players']) == 0:
        speech_output = "I cannot find any players loaded, say setup game followed by the players names"

    # if no start player has been selected yet then make the choice
    elif playerselected == False :
        # select random number between 1 and the maximum length of the json file
        selectedplayer = random.randint(1,len(playerdata['players'])) - 1
        
        # udpate player in json file
        playerdata['players'][selectedplayer]['nextPlay'] = True

        speech_output = playerdata['players'][selectedplayer]['Name'] + " will start, " + generatebreakstring(500,"ms") + playerdata['players'][selectedplayer]['Name'] + " say the name of our first celebrity"
        
    # else play the turn
    else:
        playingPlayerID = 0
        next_player = ""

        # loop through players in json    
        for p in playerdata['players']:    
            # test if they are next to play
            if p['nextPlay'] == True :  
                
                # extract celebrity from slot
                celebName = intent['slots']['celebrity']['value']
                speech_output =  celebName.title() + generatebreakstring(500,"ms") + ", "
                # set up for next player turn    
                # set playing player ID - will be used to set the next player later in function
                playingPlayerID = int(p['ID'])
                playingPlayerName = p['Name']
                # turn off next play to force next player turn
                p['nextPlay'] = False

                # if the json is empty then add the first celeb, else play the game
                if len(gamedata['names']) == 0 :
                    # add new celeb to json
                    loaded = addtogameJson(len(gamedata['names'])+1,celebName.title())
                    # set starting direction type
                    directionType = "asc"
                    # if the load to the game json failed then state error
                    if loaded == False :
                        p['hasLost'] = True

                else:
                     # load last celebrity criteria
                    lastCeleb = gamedata["names"][-1]['celebName']
                    oldlnamestart = gamedata["names"][-1]['lnamestart']
                    oldFinalLetter = gamedata["names"][-1]['finalletter']

                    # add new celeb to json
                    loaded = addtogameJson(len(gamedata['names'])+1,celebName.title())

                    if loaded == True:

                        # load new celebrity criteria
                        newCeleb = gamedata["names"][-1]['celebName']
                        newStartingLetter = gamedata["names"][-1]['fnamestart']
                        newLastLetter = gamedata["names"][-1]['lnamestart']
                        newFinalLetter = gamedata["names"][-1]['finalletter']

                        # test last ending letter with new starting letter
                        if oldlnamestart == newStartingLetter:
                            # add jingle    
                            # test if starting letter of new celeb is also the starting letter of the surname, if so reverse order
                            if newStartingLetter == newLastLetter :
                                # if current direction of players is asc then switch to descending
                                if directionType == "asc":
                                    directionType = "desc"
                                # else must be desc so switch to asc
                                elif directionType == "desc":
                                    directionType ="asc"

                                speech_output = speech_output + " , doubles, back to "
                        else: 
                            p['hasLost'] = True
                    else: 
                        p['hasLost'] = True
                

        # set next player - if the playing ID is equal to the number of players then, reset to player one
        if directionType == "asc":
            # if direction is asc and on max player then reset to first player
            if playingPlayerID == len(playerdata['players']):
                jsonIndex = 0
            # if direction is asc and not on max player then increment by one
            else : 
                jsonIndex = playingPlayerID
        else :
            # if direction is desc and on first player then set to max player
            if playingPlayerID == 1:
                jsonIndex = -1
            # if direction is desc and not on first player then decrease by one
            else:
                jsonIndex = playingPlayerID - 2

        # use json index to set next player
        playerdata['players'][jsonIndex]['nextPlay'] = True        
        # build next_player string to be added to the speech output
        next_player = playerdata['players'][jsonIndex]['Name']

        # set temporary variable
        playerLost = ""
        # loop through to see if anyone last lost game, edit final text on outcome
        for p in playerdata['players']:
            if p['hasLost'] == True:
                playerLost = p['Name']

        # if a player has lost, change the play back message and reset the game
        if playerLost != "" :
            speech_output = playerLost + " has lost, say start game to play again, or to start again with new players then say reset game"
            reset_game('reset')  
        else:
            speech_output = speech_output + next_player + "?"  
    # output
    card_title = "Celebrity"
    reprompt_text = ""
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session)) 

def reset_game(resettype):
    # set up session attributes
    session_attributes = {}

    if resettype == "reset":
        
        # reset json
        for p in playerdata['players']:
            p['nextPlay'] = False
            p['didPlay'] = False
            p['hasLost'] = False

        # re instantiate game data json
        gamedata['names'] = []
        # tell user
        speech_output =  "I've reset the game, just say start game to start"
    
    elif resettype == "delete":
        # re instantiate game data json
        playerdata['players'] = []
        # re instantiate game data json
        gamedata['names'] = []
        # tell user
        speech_output = "I've reset the game, just say setup game with players followed by the player names"

    # output
    card_title = "Reset Game"
    reprompt_text = ""
    should_end_session = False
    speech_output = "<speak>" + speech_output + "</speak>"
    card_output = cleanssml(speech_output)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, card_output, reprompt_text, should_end_session))       
                
    
# build message response
def build_speechlet_response(title, output, cardoutput, reprompt_text, should_end_session):
    return {"outputSpeech": {"type": "SSML", "ssml":  output},
            "card": {"type": "Simple","title": title,"content": cardoutput},
            "reprompt": {"outputSpeech": {"type": "PlainText","text": reprompt_text}},
            "shouldEndSession": should_end_session}

# build response
def build_response(session_attributes, speechlet_response):
    return {
    "version": "1.0",
    "sessionAttributes": session_attributes,
    "response": speechlet_response }

# function to generate the ssml needed for a break
def generatebreakstring(pause, timetype):
    # generate the SSML string for break with dynamic length
    breakstring = '<break time="' + str(pause) + timetype + '"/>'
    return breakstring

# function to automatically remove ssml markup, needed to generate the card output - which is what is shown on screen
def cleanssml(ssml):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', ssml)
    return cleantext

# setup Json for players
def setupplayerJson() :
    global playerdata
    playerdata = {}
    playerdata['players'] = []

# add player to json
def addplayertoJson(ID,Name,lastScore,lastRoll,nextPlay,didPlay,hasLost,numGoes,sessionWins) :
    playerdata['players'].append({    
    'ID': ID,
    'Name': Name,
    'nextPlay': nextPlay,
    'didPlay': didPlay,
    'hasLost': hasLost
    })

# setup Json for game
def setupgameJson() :
    global gamedata
    gamedata = {}
    gamedata['names'] = []

def addtogameJson(ID, celebName):
    # add code to strip out letters from celeb name
    try:
        startLetter = celebName[0].lower()
        lastLetter = celebName[celebName.index(" ")+1].lower()
        finalLetter = celebName[-1].lower()
        load = True
        # append
        gamedata['names'].append({
            'ID': ID,
            'celebName' : celebName,
            'fnamestart': startLetter,
            'lnamestart': lastLetter,
            'finalletter': finalLetter
        })
    except :
        load = False
    print(load)
    return load

    

# test for a winner
def testforwinner():
    # setup temporary variables
    winner = ""
    # loop through players in json
    for p in playerdata['players'] :   
        # if anyone has hasWon set to true then there is a winner return the name
        if p['hasWon'] == True :
                winner = p['Name'] 
    return winner          


        
