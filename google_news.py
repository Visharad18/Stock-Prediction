import requests
import bs4
import urllib
import webbrowser
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
import nltk
from matplotlib import pyplot as plt
from textblob import TextBlob
nltk.download('vader_lexicon')
sia=SIA()
url1='https://www.google.com/search?q='
company_name='maruti'
url2='&rlz=1C1CHZL_enIN820IN820&biw=1366&bih=625&sxsrf=ACYBGNR_Yffd_Zho481hN4gWm15kmPcsFA%3A1570634911397&source=lnt&tbs=cdr%3A1%2Ccd_min%3A'
min_date=input('Enter starting date (in mm-dd-yyyy): ').split('-')		# in m(m)-d(d)-yyyy
url3=min_date[0]+'%2F'+min_date[1]+'%2F'+min_date[2]
#print(url3)
url4='%2Ccd_max%3A'
max_date=input('Enter ending date (in mm-dd-yyyy): ').split('-')		# in m(m)-d(d)-yyyy
url5=max_date[0]+'%2F'+max_date[1]+'%2F'+max_date[2]
#print(url5)
url6='&tbm=nws'
url=url1+company_name+url2+url3+url4+url5+url6
print(url)
h={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}
res=requests.get(url,headers=h)
soup=bs4.BeautifulSoup(res.text,'lxml')
links=soup.select('.r a')
#print(links)
x=int(input('Enter the number of search results to be opened: '))
tabs=min(x,len(links))
score=0
scores=[]
scoresblob=[]
for i in range(tabs):
	webbrowser.open(links[i].get('href'))
	print(links[i].get('href'))
	r=requests.get(links[i].get('href'),headers=h)
	s=bs4.BeautifulSoup(r.text,'lxml')
	par=(s('p',limit=7))

	y=[re.sub(r'<.+?>',r'',str(a)) for a in par]
	par=''
	for i in y:
		par=par+i
	print(par)
	print(type(par))
	scores.append(sia.polarity_scores(par)['compound'])
	scoresblob.append(TextBlob(par).sentiment.polarity)
	score+=sia.polarity_scores(par)['compound']
score/=len(scores)
print(score)
ax=plt.axes()
ax.plot(range(tabs),scores)
ax.plot(range(tabs),scoresblob)
plt.show()

	

#pg=urllib.request.urlopen(url).read()
#soup=bs4.BeautifulSoup(pg)
#links=[]
#for link in soup.findAll('a',attrs={'href':re.compile("^http://")}):
	#links.append(link.get('href'))
#print(links)