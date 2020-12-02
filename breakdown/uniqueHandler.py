import json
import re #used for regular expressions
import pandas as pd # to convert json to csv
from parseComments import comments, uniquesArray, parsedComments


#### TODO
# Handle mentions and hashtags
# 159 rating is wrong


# LIST OF UNIQUES THAT NEED TO BE ORGANIZED
# 428 - Behind the scenes
# 575 - Highlight clip
# 567 - Highlight clip
# 589 - restaurant/cityState different characters
# 607 - No '/10' in the rating
# 619 - restaurant/cityState different characters
# 620 - restaurant/cityState different characters



i = 0
for text in comments:
	# TEST CASES
	# if (tacoType == '' or restaurant == '' or cityState == '' or rating == ''):
	#     print(i)
	    # These are the ones that have something come up blank
	    #148, 428, 485, 504, 567, 570, 575, 582, 587, 588, 589, 590, 591, 619, 620
	

	    # 3, 38, 63, 95, 99, 105, 121, 139, 150, 159, 170, 171, 172, 184, 198, 259, 266, 268, 286, 290, 333, 341, 358, 398, 405, 435, 482, 490, 514, 523, 528, 533, 536, 539, 551, 569, 572, 574, 580, 604, 606, 609, 610, 612, 613, 614, 615, 616, 617, 618
	    #fixed by stripping rating and seconds to finish

	# Good test would be to check seconds to finish for any ratings
	# 3,99,121,259,333,551,569,580,604,605,606,607,608,609,610,611,612,613,614,615,617,618,619,620
	i=i+1

# for item in uniquesArray:
# 	print(uniquesArray[item].'id')

print([item['id'] for item in uniquesArray])



# for item in uniquesArray:
# 	print(str(item.id) + '\n' + json.dumps(parsedComments[item.id], indent=4))

# print('606\n' + json.dumps(parsedComments[606], indent=4))
# print('620\n' + json.dumps(parsedComments[620], indent=4))

# print(comments[606])
# print(comments[620])


















