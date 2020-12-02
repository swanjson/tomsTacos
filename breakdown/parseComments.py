import json
import re #used for regular expressions
import pandas as pd # to convert json to csv
import toolz


#### TODO
# Handle mentions and hashtags
# 159 rating is wrong

with open('tomeatingtacos.json', 'r') as f:
    listOfComments = json.load(f)


# print(listOfComments['GraphImages'][0]['edge_media_to_caption']['edges'][0]['node']['text'])
numberOfPosts = len(listOfComments['GraphImages'])

uniquesArray = []
comments = [None] * numberOfPosts
i = 0
# Goes through each post (621 atm) 
for entry in listOfComments['GraphImages']:  
    comments[i] = entry['edge_media_to_caption']['edges'][0]['node']['text']
    i=i+1


finishDiffs = ['finish ', 'finish.', 'finish#']
ratingDiffs = ['/10.', '/10 ']
parsedComments = [None] * numberOfPosts

i = 0
for text in comments:
    tacoType = text.partition('. ')[0]
    remainingText1 = text.partition('. ')[2]
    restaurant = remainingText1.partition('. ')[0]
    remainingText2 = remainingText1.partition('. ')[2]
    cityState = remainingText2.partition('. ')[0]
    remainingText3 = remainingText2.partition('. ')[2]

    if ratingDiffs[0] in remainingText3:
        rating = remainingText3.partition('. ')[0]
        remainingText4 = remainingText3.partition('. ')[2]
        rating = rating.strip()
    elif ratingDiffs[1] in remainingText3:
        rating = remainingText3.partition('/10 ')[0] + remainingText3.partition('/10')[1]
        remainingText4 = remainingText3.partition('/10 ')[2]
        rating = rating.strip()
    if finishDiffs[0] in remainingText4:
        secondsToFinish = remainingText4.partition('sh ')[0] + remainingText4.partition('sh ')[1]
        secondsToFinish = secondsToFinish.strip()
        leftovers = remainingText4.partition('sh ')[2]
    elif finishDiffs[1] in remainingText4:
        secondsToFinish = remainingText4.partition('sh. ')[0] + remainingText4.partition('sh. ')[1]
        secondsToFinish = secondsToFinish.replace('.','')
        secondsToFinish = secondsToFinish.strip()
        leftovers = remainingText4.partition('sh. ')[2]
    elif finishDiffs[2] in remainingText4:
        secondsToFinish = remainingText4.partition('sh#')[0] + remainingText4.partition('sh ')[1]
        secondsToFinish = secondsToFinish.strip()
        leftovers = remainingText4.partition('sh# ')[2]
    else:
        secondsToFinish = 'null'



    ########### TEST CASES ##############

    #Tests if any entry is blank or null, if so send to uniqueHandler
    if (tacoType == '' or restaurant == '' or cityState == '' or rating == ''):
        testCaseOutput(i,'rating, cityState, restaurant, or tacoType is blank',uniquesArray)

    #Tests if there are spaces in rating, if so sends to unique handler
    if ' ' in rating:
        testCaseOutput(i,'There is a space in the rating',uniquesArray)


    #Calculates the float of the ratings, if the rating is larger than 10 characters or there isn't a 10 in the rating, send to uniqueHandler
    if len(rating) < 10:
        if '10' in rating:
            ratingEval = eval(rating)
        else:
            ratingEval = None
            testCaseOutput(i,'There\'s no 10 in the rating',uniquesArray)
    else:
        ratingEval = None
        testCaseOutput(i,'length of rating is over 10',uniquesArray)

    if rating not in text:
        testCaseOutput(i,'rating is not correct',uniquesArray)

    # if 'seconds to finish' not in secondsToFinish:
    #     uniquesArray.append(i)


    ########### TEST CASES ##############
    z = 0
    def testCaseOutput(itemNumber,reasonString,uniquesArray):
        uniquesArray.append({
        "id": itemNumber,
        "failingReason": reasonString
        })
                    

    parsedComments[i] = {
        "id": i,
        "post#": numberOfPosts - i,
        "tacoType": tacoType,
        "restaurant": restaurant,
        "cityState": cityState,
        "rating": rating,
        "ratingEval": ratingEval,
        "secondsToFinish": secondsToFinish,
        "leftovers": leftovers
    }
    i=i+1 #INCREMENT



#Below sorts the array to only have unique objects
toolz.unique(uniquesArray)
# print(uniquesArray)

#creates array with unique objects that are messed up
arrayToRemove = [item['id'] for item in uniquesArray]
arrayToRemove = list(dict.fromkeys(arrayToRemove))
# print(arrayToRemove)


# removes all the things in question ^^ (arrayToRemove)
parsedComments = [item for item in parsedComments if item['id'] not in arrayToRemove]



# LIST OF UNIQUES THAT NEED TO BE ORGANIZED
# 428 - Behind the scenes
# 575 - Highlight clip
# 567 - Highlight clip
# 589 - restaurant/cityState different characters
# 607 - No '/10' in the rating
# 619 - restaurant/cityState different characters
# 620 - restaurant/cityState different characters

with open('commentsFull.json', 'w', encoding='utf8') as json_file:
    json.dump(comments, json_file, indent=4, ensure_ascii=False)

with open('errors.json', 'w', encoding='utf8') as json_file:
    json.dump(uniquesArray, json_file, indent=4, ensure_ascii=False)

with open('breakdown.json', 'w', encoding='utf8') as json_file:
    json.dump(parsedComments, json_file, indent=4, ensure_ascii=False)


# prints single object from parsedComments
# print(json.dumps(parsedComments[572], indent=4))
# print(json.dumps(parsedComments[159], indent=4))


#converts created json into csv via pandas
df = pd.read_json('breakdown.json')
df.to_csv('rankedCSV.csv')

