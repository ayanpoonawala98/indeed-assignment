from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import pandas as pd


requirement = 10000
isscrpingpossible = True

website_heading = "https://www.indeed.co.in/"
url = "https://www.indeed.co.in/jobs?q=computer+engineer+fresher&l=India"

header = "Company, Designation, Address, Salary, Ratings \n"
file = open('indeedjob.csv','w')
file.write(header)
file.close()
a=1
data = pd.read_csv('indeedjob.csv')
while((data.shape[0] < requirement) and isscrpingpossible):
	print(url)
	req = requests.get(url)
	soup = BeautifulSoup(req.text,'lxml')
	divs = soup.findAll('div',{'class': 'jobsearch-SerpJobCard'})
	for div in divs:
		try:
			Companyname = div.findAll('span',{'class':'company'})[0].text.lstrip().rstrip().replace(',', ' -')

		except:
			Companyname = 'NAN'
		Designation = div.findAll('a',{'class':'jobtitle'})[0].text.lstrip().rstrip().replace(',', ' -')
		Address = div.findAll('span',{'class':'location'})[0].text.lstrip().rstrip().replace(',', ' -')
		try:
			Ratings= div.findAll('span',{'class':'ratingsContent'})[0].text.lstrip().rstrip().replace(',', ' -')
			Salary = div.findAll('span',{'class':'salaryText'})[0].text.lstrip().rstrip().replace(',', ' -')
		except Exception:
			Ratings ='NAN'
			Salary = 'Not Mention'
		joins_rows = Companyname + ', ' + Designation +', '+Address+', '+Salary + ', ' +Ratings +'\n'
		file = open('indeedjob.csv','a')
		file.write(joins_rows)
		file.close()
	data = pd.read_csv('indeedjob.csv')
	nexts = soup.find('div',{'class':'pagination'})
	print(url)
	nexts = nexts.findAll('a')[-1].attrs['href']


	print(nexts)
	try:
		url= urljoin(website_heading,nexts)
		
	except:
		isscrpingpossible = False
	print(a)
	a+=1
if(data.shape[0] < 10000):
	print("Sorry No more data Available, only " + str(data.shape[0]) + " data are available")
else:
	print(str(data.shape[0]) + " Data Scrapped Successfully")