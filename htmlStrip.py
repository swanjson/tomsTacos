from bs4 import BeautifulSoup
import requests


#source = requests.get('https://www.instagram.com/tomeatingtacos').text


with open('instagramPageFull.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

i = 0

for div in soup.find_all('div', class_='_4rbun'):
    for comment in div.find_all('img', alt=True):
        i += 1
        print(i)
        print(comment['alt'])


#division = soup.find('div', class_='_4rbun')
#comment = division.find('img', alt=True)
#print(comment)




#for div in soup.find_all('div', 'thumbnail'):
#   for img in div.find_all('img', alt=True):
#       print(img['alt'])
#
