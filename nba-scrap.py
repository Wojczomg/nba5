headers = {
'Host': 'd.flashscore.pl',
'User-Agent': 'core',
'Accept': '*/*',
'Accept-Language':'*',
'Accept-Encoding': 'gzip, deflate, br',
'Referer': 'https://d.flashscore.pl/x/feed/proxy-local',
'X-Referer': 'https://www.flashscore.pl/koszykowka/usa/nba-2017-2018/wyniki/',
'X-Fsign': 'SW9D1eZo',
'X-Requested-With': 'XMLHttpRequest',
'Connection': 'keep-alive'}

import requests
from bs4 import BeautifulSoup
import re
import numpy as np
import csv
RENDER_HTML_URL = "http://192.168.99.100:8050/render.html"

kody=[]

for s in ["","-2017-2018","-2016-2017","-2015-2016","-2014-2015"]:
	req = requests.get(RENDER_HTML_URL,
	             params={'url': 'https://www.flashscore.pl/koszykowka/usa/nba{}/wyniki/'.format(s),
	              'wait': 0.5})
	print(req.status_code)


	soup = BeautifulSoup(req.content, 'html.parser')
	kodziki = [i.get('id')[4:] for i in soup.find_all(id = re.compile("^(g_3_)"))]
	kody.extend(kodziki)
for y in [9,8,7,6,5]:
	for i in range(1,14):

		r = requests.get('https://d.flashscore.pl/x/feed/tr_3_200_IBmris38_16{}_{}_2_pl_1'.format(y,i),
			headers = headers)
		kodziki=[i[1:-1] for i in re.findall(r'÷[\w]{8}¬',r.text)]
		kody.extend(kodziki[36::3])

def parse_match(code):
	req1 = requests.get(RENDER_HTML_URL,
             params={'url': 'https://www.flashscore.pl/mecz/{}/#szczegoly-meczu'.format(code),
              'wait': 1})
	print("REQ1 STATUS --------",req1.status_code)
	soup = BeautifulSoup(req1.content, 'html.parser')
	date = soup.find(id="utime", class_="info-time").text
	print(date)
	team1 = soup.find_all("td",class_="summary-horizontal")[0].a.text
	print(team1)
	team2 = soup.find_all("td",class_="summary-horizontal")[1].a.text
	print(team2)
	team1_p = [soup.find("span",class_="p{}_home".format(i)).text for i in range(1,5)]
	team2_p = [soup.find("span",class_="p{}_away".format(i)).text for i in range(1,5)]
	print(team1_p)
	print(team2_p)
	odd1 = soup.find("span",class_="odds-wrap up").text
	odd2 = soup.find("span",class_="odds-wrap down").text
	print(odd1)
	print(odd2)

	req2 = requests.get(RENDER_HTML_URL,
             params={'url': 'https://www.flashscore.pl/mecz/{}/#statystyki-meczu;1'.format(code),
              'wait': 1})
	print("REQ2 STATUS --------",req2.status_code)
	soup2 = BeautifulSoup(req2.content, 'html.parser')
	stats_home = [i.get_text() for i in soup2.find_all("div", class_="statText statText--homeValue",limit=63)[21:]]
	print(len(stats_home))
	stats_away = [i.get_text() for i in soup2.find_all("div", class_="statText statText--awayValue",limit=63)[21:]]
	print(len(stats_away))

	req3 = requests.get(RENDER_HTML_URL,
             params={'url': 'https://www.flashscore.pl/mecz/{}/#zestawienie-kursow;powyzej-ponizej;koniec-meczu'.format(code),
              'wait': 1})
	print("REQ3 STATUS --------",req3.status_code)
	soup3 = BeautifulSoup(req3.content, 'html.parser')
	ou_list = [list(i.strings) for i in soup3.find("div",id="block-under-over-ft").find_all("tr",class_="odd")]
	oo = [abs(float(ou_list[i][1]) - float(ou_list[i][2])) for i in range(0,len(ou_list))]
	ouborder = float(ou_list[oo.index(min(oo))][0])
	print(ouborder)

	row = [hash(date+team1+team2),date,team1,team2,*team1_p,*team2_p,odd1,odd2,ouborder,*stats_home,*stats_away]

	with open('nba5.csv', 'a') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
	csvFile.close()


print('NUM OF MATCHES TO PARSE:',len(kody))
for i in kody:
	try:
		parse_match(i)
	except:
		pass
			





