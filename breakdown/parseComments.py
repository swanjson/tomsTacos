import json
import re #used for regular expressions
import pandas as pd # to convert json to csv


#### TODO
#### REMOVE NEW LINES
# Handle mentions too

with open('tomeatingtacos.json', 'r') as f:
    listOfComments = json.load(f)


# print(listOfComments['GraphImages'][0]['edge_media_to_caption']['edges'][0]['node']['text'])



comments = [None] * 621
i = 0
# Goes through each post (621 atm) 
for entry in listOfComments['GraphImages']:  
    comments[i] = entry['edge_media_to_caption']['edges'][0]['node']['text']
    i=i+1


finishDiffs = ['finish ', 'finish.', 'finish#']
ratingDiffs = ['/10.', '/10 ']
parsedComments = [None] * 621

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


    # TEST CASES
    # if (tacoType == '' or restaurant == '' or cityState == '' or rating == ''):
    #     print(i)
        # These are the ones that have something come up blank
        #148, 428, 485, 504, 567, 570, 575, 582, 587, 588, 589, 590, 591, 619, 620
    if ' ' in rating:
        print(i)

        # 3, 38, 63, 95, 99, 105, 121, 139, 150, 159, 170, 171, 172, 184, 198, 259, 266, 268, 286, 290, 333, 341, 358, 398, 405, 435, 482, 490, 514, 523, 528, 533, 536, 539, 551, 569, 572, 574, 580, 604, 606, 609, 610, 612, 613, 614, 615, 616, 617, 618
        #fixed by stripping rating and seconds to finish
    if len(rating) < 10:
        if '10' in rating:
            ratingEval = eval(rating)
        else:
            ratingEval = None
    else:
        ratingEval = None

    # Good test would be to check seconds to finish for any ratings
    # 3,99,121,259,333,551,569,580,604,605,606,607,608,609,610,611,612,613,614,615,617,618,619,620

    parsedComments[i] = {
        "id": i,
        "post#": 621 - i,
        "tacoType": tacoType,
        "restaurant": restaurant,
        "cityState": cityState,
        "rating": rating,
        "ratingEval": ratingEval,
        "secondsToFinish": secondsToFinish,
        "leftovers": leftovers
    }
    i=i+1 #INCREMENT

# print(json.dumps(parsedComments, indent=4, sort_keys=True))
# print(json.dumps(listOfComments, indent=4, sort_keys=True))


# LIST OF UNIQUES THAT NEED TO BE ORGANIZED
# 428 - Behind the scenes
# 575 - Highlight clip
# 567 - Highlight clip
# 589 - restaurant/cityState different characters
# 607 - No '/10' in the rating
# 619 - restaurant/cityState different characters
# 620 - restaurant/cityState different characters


# print('428\n' + json.dumps(parsedComments[428], indent=4)) #behind the scenes?
# print('567\n' + json.dumps(parsedComments[567], indent=4)) #highlight clip
# print('575\n' + json.dumps(parsedComments[575], indent=4)) #highlight clip
# print('589\n' + json.dumps(parsedComments[589], indent=4)) #restaurant/cityState different characters
# print('619\n' + json.dumps(parsedComments[619], indent=4)) #restaurant/cityState different characters
# print('620\n' + json.dumps(parsedComments[620], indent=4)) #restaurant/cityState different characters


with open('breakdown.json', 'w', encoding='utf8') as json_file:
    json.dump(parsedComments, json_file, indent=4, ensure_ascii=False)



# 3, 38, 63, 95, 99, 105, 121, 139, 150, 159, 170, 171, 172, 184, 198, 259, 266, 268, 286, 290, 333, 341, 358, 398, 405, 435, 482, 490, 514, 523, 528, 533, 536, 539, 551, 569, 572, 574, 580, 604, 606, 609, 610, 612, 613, 614, 615, 616, 617, 618

print('3\n' + json.dumps(parsedComments[3], indent=4)) # still flagged period in location line
print('63\n' + json.dumps(parsedComments[63], indent=4)) # still flagged switched rating and seconds to finish
print('99\n' + json.dumps(parsedComments[99], indent=4)) # still flagged Extra Period in citystate
print('121\n' + json.dumps(parsedComments[121], indent=4)) # still flagged 500th Taco video Extra title line
print('259\n' + json.dumps(parsedComments[259], indent=4)) # still flagged Period in Taco Name
print('333\n' + json.dumps(parsedComments[333], indent=4)) # still flagged period in location line
print('482\n' + json.dumps(parsedComments[482], indent=4)) # still flagged extra location line
print('551\n' + json.dumps(parsedComments[551], indent=4)) # still flagged extra location line
print('572\n' + json.dumps(parsedComments[572], indent=4)) # still flagged 2 tacos with 2 ratings and seconds to finish
print('574\n' + json.dumps(parsedComments[574], indent=4)) # still flagged 2 tacos
print('569\n' + json.dumps(parsedComments[574], indent=4)) # still flagged 2 tacos w 2 ratings (wasn't auto found)
print('606\n' + json.dumps(parsedComments[606], indent=4)) # still flagged extra city state line


df = pd.read_json('breakdown.json')
df.to_csv('rankedCSV.csv')




# 3
# 63
# 99
# 121
# 171
# 172
# 259
# 266
# 268
# 333
# 482
# 551
# 572
# 574
# 575
# 606
# 607






# 3
# 38
# 63
# 95
# 99
# 105
# 121
# 139
# 150
# 159
# 170
# 171
# 172
# 184
# 198
# 259
# 266
# 268
# 286
# 290
# 333
# 341
# 358
# 398
# 405
# 435
# 482
# 490
# 514
# 523
# 528
# 533
# 536
# 539
# 551
# 569
# 572
# 574
# 580
# 604
# 606
# 609
# 610
# 612
# 613
# 614
# 615
# 616
# 617
# 618