import requests
import re
import time
from lxml import html
import json
from bs4 import BeautifulSoup
data={}
sleep=0
itemsToFitch=25 # because 12*25 =300
data["records"]=[]
count=1
for i in range(itemsToFitch):
    url="https://www.kickstarter.com/discover/advanced?woe_id=0&sort=popularity&ref=discovery_overlay&seed=2624644&page="
    res=requests.get(url+str(i))
    soup = BeautifulSoup(res.text, 'lxml')

    x = soup.find_all(class_='js-react-proj-card grid-col-12 grid-col-6-sm grid-col-4-lg')
    html_content = x[0].prettify()
    html_content2 = x[1].prettify()
    for i in x:
        time.sleep(sleep) # this one used to wait between requests can be changed according to param Sleep
        line = i.prettify()
        r1 = re.findall('https://www\.kickstarter\.com/projects/.*/.*/rewards',line)
        inner=r1[0].split("https")[2][3:-8]

        project_page = requests.get('https://'+inner)

        structure = html.fromstring(project_page.content)


        pelaged = str(structure.xpath(
            '//*[@id="react-project-header"]/div/div/div[1]/div[2]/div[2]/div[1]/div[2]/span/span/text()')[0]).strip()

        title = str(
            structure.xpath('//*[@id="react-project-header"]/div/div/div[2]/div/div[2]/div/h2/text()')[0]).strip()


        description = str(structure.xpath('/html/text()')[0]).strip()

        days = str(structure.xpath(
            '//*[@id="react-project-header"]/div/div/div[1]/div[2]/div[2]/div[3]/div/div/span[1]/text()')[0]).strip()

        backer = str(
            structure.xpath('//*[@id="react-project-header"]/div/div/div[1]/div[2]/div[2]/div[2]/div/span/text()')[
                0]).strip()

        goal = str(structure.xpath(
            '//*[@id="react-project-header"]/div/div/div[1]/div[2]/div[2]/div[1]/span/span[2]/span/text()')[0]).strip()

        allOrNothing = str(
            structure.xpath('//*[@id="react-project-header"]/div/div/div[1]/div[2]/div[4]/p/span[1]/a/text()')[
                0]).strip()

        data["records"].append(
            {
                'id': str(count),
                'URL': 'https://'+inner,
                'Title': title,
                'DollarsPleaged': pelaged,
                'DollarsGoal': goal,
                'NumBackers': backer,
                'DaysToGo': days,
                'All Or Nothing': allOrNothing,


            }
        )

        print('pages scraped: '+str(count))
        count+=1


with open('data.txt','w') as outfile:
    json.dump(data,outfile)