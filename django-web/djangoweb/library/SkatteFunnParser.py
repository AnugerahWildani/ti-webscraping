import os
import requests
from bs4 import BeautifulSoup, Comment
from datetime import datetime
from lxml import html
from collections import defaultdict
import re

class SkatteFunnParser:

	def __init__(self,url, name, notes):

		self.url = url
		self.title = "SkatteFunn"
		self.header = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/76.0.3809.100 Chrome/76.0.3809.100 Safari/537.36'}
		self.username = name
		self.notes = notes

	def change_log_in(self,username, password):

		#logg inn
		login_url = self.url + 'j_security_check'
		login_data = {  
				'j_username': username,
				'j_password': password,
				'tegnsett': 'UTF-8'
			}
		with requests.Session() as session:
			login = session.post(login_url, data=login_data, headers=self.header)
			return login, session

	def print_settings(self):
		print(self.url, self.title, self.header)
	
	def header_str(self, text):
		head_text = text.replace('\n', '').replace('\t', '').lower().replace(' ', '_').replace('å','a').replace('ã¸', 'ø').replace('/','_').replace('ã¥', 'a').replace('ã', '')
		return head_text

	def body_str(self, text):
		body_text = text.replace('\n', '').replace('\t', '').replace('ã¸', 'ø').replace('Ã¥', 'å').replace('ã¥', 'å').replace('ã', 'å').replace('Ã¸', 'ø').replace('Ã', 'Ø')
		return body_text

	def get_data(self, url_, session):
		#parse website
		# content = session.get(url_)
		tree = html.parse(url_)
		content = html.tostring(tree)
		soup = BeautifulSoup(content, 'html.parser')

		try:
			web_data = {}
			web_data['url'] = url_
			if os.name == 'nt':
				web_data['url_name'] = url_.split('\\')[-1].split('_')[4].replace('.', '_')
			else:
				web_data['url_name'] = url_.split('/')[-1].split('_')[4].replace('.', '_')
			web_data['title'] = self.title
			web_data['project'] = self.notes
			web_data['username'] = self.username
			web_data['header'] = self.header
			web_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M')
			headers1 = []
			headers2 = []
			headers3 = []
			web_data['prosjektbrev'] = []
			web_data['prosjektrapporter'] = []
			web_data['historikk'] = []

			searchtext = re.compile(r'Prosjektbrev', re.IGNORECASE)
			foundtext = soup.find('span', text = searchtext)
			table1 = foundtext.findNext('table')
			rows = table1.find_all('tr')
			for idx, tr in enumerate(rows):
				if idx == 0:
					cols = tr.find_all('td')
					for td in cols:
						headers1.append(td.text.lower().replace(' ', '_'))
				else:
					data = []
					cols = tr.find_all('td')
					for td in cols:
						data.append(td.text.replace('\n', '').replace('\t', ''))
					newdict = dict(zip(headers1, data))
					web_data['prosjektbrev'].append(newdict) 

			searchtext = re.compile(r'Prosjektrapporter', re.IGNORECASE)
			foundtext = soup.find('span', text = searchtext)
			table1 = foundtext.findNext('table')
			rows = table1.find_all('tr')
			for idx, tr in enumerate(rows):
				if idx == 0:
					cols = tr.find_all('td')
					for td in cols:
						headers2.append(td.text.lower().replace(' ', '_'))
				else:
					data = []
					cols = tr.find_all('td')
					for td in cols:
						data.append(td.text.replace('\n', '').replace('\t', ''))
					newdict = dict(zip(headers2, data))
					web_data['prosjektrapporter'].append(newdict) 

			comments = soup.findAll(text=lambda text:isinstance(text, Comment))
			foundcomment = comments[3]
			table1 = foundcomment.findNext('table')
			rows = table1.find_all('tr')
			for idx, tr in enumerate(rows):
				if idx == 0:
					cols = tr.find_all('td')
					for i, td in enumerate(cols):
						if i > 0:
							headers3.append(td.text.lower().replace(' ', '_'))

				elif idx % 2 == 0:
					data = []
					cols = tr.find_all('span', class_='smallgrey')
					for span in cols:
						data.append(span.text.replace('\n', '').replace('\t', ''))
					newdict = dict(zip(headers3, data))
					web_data['historikk'].append(newdict) 
			
			return web_data
		except:
			web_data = {}
			web_data['url'] = url_
			if os.name == 'nt':
				web_data['url_name'] = url_.split('\\')[-1].split('_')[4].replace('.', '_')
			else:
				web_data['url_name'] = url_.split('/')[-1].split('_')[4].replace('.', '_')
			web_data['title'] = self.title
			web_data['project'] = self.notes
			web_data['username'] = self.username
			web_data['header'] = self.header
			web_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M')
			headers = []
			web_data['data_table'] = []

			table = soup.find('table', {'width': '100%', 'class':''})
			head_row = table.find('tr')
			theads = head_row.find_all('td', class_='worklist1')
			for thead in theads: 
				header = self.header_str(thead.text)
				headers.append(header)
			
			body_rows = head_row.find_next_siblings('tr')
			for idx, row in enumerate(body_rows):
				if idx % 2 == 0:	
					datas = row.find_all('td', class_='worklist2')
					values = []
					for data in datas:
						data = self.body_str(data.text)
						values.append(data)
					data_dict = dict(zip(headers, values))
					web_data['data_table'].append(data_dict)
				else:
					datas = row.find_all('td', class_='worklist1')
					values = []
					for data in datas:
						data = self.body_str(data.text)
						values.append(data)
					data_dict = dict(zip(headers, values))
					web_data['data_table'].append(data_dict)
			return web_data
	
	def get_data_main(self, url_, session):
		# content = session.get(url_)
		tree = html.parse(url_)
		content = html.tostring(tree)
		soup = BeautifulSoup(content, 'html.parser')
		
		web_data = {}
		web_data['url'] = url_
		web_data['url_name'] = 'main'
		web_data['title'] = self.title
		web_data['project'] = self.notes
		web_data['username'] = self.username
		web_data['header'] = self.header
		web_data['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M')
		web_data['info'] = []
		
		try:
			search1 = re.compile(r'under arbeid', re.IGNORECASE)
			found1 = soup.find('td', text = search1)
			get_text1 = [self.header_str(found1.text.split('(')[0])]
			get_number1 = [found1.text.split('(')[1].replace(')', '')]
			data_dict1 = dict(zip(get_text1, get_number1))
			web_data['info'].append(data_dict1)
			
			num1_int = int(''.join(get_number1))
			if int(num1_int) > 0:
				web_data['under_arbeid'] = []
				head_row = found1.find_next('tr')
				headers = []	
				td_heads = head_row.find_all('td')
				for tdh in td_heads:
					th = self.header_str(tdh.text)
					headers.append(th)
				body_rows = head_row.find_next_siblings('tr')
				for i, row in enumerate(body_rows[:-3]):
					if i % 2 == 0:
						bodies = []	
						tds = row.find_all('td', class_='worklist_second')
						for td in tds:
							data = self.body_str(td.text)
							bodies.append(data)
						newdict = dict(zip(headers, bodies))
						web_data['under_arbeid'].append(newdict)

					else:
						bodies = []	
						tds = row.find_all('td', class_='worklist_first')
						for td in tds:
							data = self.body_str(td.text)
							bodies.append(data)
						newdict = dict(zip(headers, bodies))
						web_data['under_arbeid'].append(newdict)

		except:
			print('Text not found')

		try:
			search2 = re.compile(r'pnede brev', re.IGNORECASE)
			found2 = soup.find('td', text = search2)
			get_text2 = [self.header_str(found2.text.split('(')[0])]
			get_number2 = [found2.text.split('(')[1].replace(')', '')]
			data_dict2 = dict(zip(get_text2, get_number2))
			web_data['info'].append(data_dict2)

			num2_int = int(''.join(get_number2))
			if int(num2_int) > 0:
				web_data['brev'] = []
				head_row = found2.find_next('tr')
				headers = []	
				td_heads = head_row.find_all('td')
				for tdh in td_heads:
					th = self.header_str(tdh.text)
					headers.append(th)
				body_rows = head_row.find_next_siblings('tr')
				for i, row in enumerate(body_rows[:-3]):
					if i % 2 == 0:
						bodies = []	
						tds = row.find_all('td', class_='worklist_second')
						for td in tds:
							data = self.body_str(td.text)
							bodies.append(data)
						newdict = dict(zip(headers, bodies))
						web_data['brev'].append(newdict)

					else:
						bodies = []	
						tds = row.find_all('td', class_='worklist_first')
						for td in tds:
							data = self.body_str(td.text)
							bodies.append(data)
						newdict = dict(zip(headers, bodies))
						web_data['brev'].append(newdict)							
					
				
		except:
			print('Text not found')

		try:
			search3 = re.compile(r'oppgaver', re.IGNORECASE)
			found3 = soup.find('td', text = search3)
			get_text3 = [self.header_str(found3.text.split('(')[0])]
			get_number3 = [found3.text.split('(')[1].replace(')', '')]
			data_dict3 = dict(zip(get_text3, get_number3))
			web_data['info'].append(data_dict3)

			num3_int = int(''.join(get_number3))
			if int(num3_int) > 0:
				web_data['oppgaver'] = []
				head_row = found3.find_next('tr')
				headers = []	
				td_heads = head_row.find_all('td')
				for tdh in td_heads:
					th = self.header_str(tdh.text)
					headers.append(th)
				body_rows = head_row.find_next_siblings('tr')
				for i, row in enumerate(body_rows[:-3]):
					if i % 2 == 0:
						bodies = []	
						tds = row.find_all('td', class_='worklist_second')
						for td in tds:
							data = self.body_str(td.text)
							bodies.append(data)
						newdict = dict(zip(headers, bodies))
						web_data['oppgaver'].append(newdict)

					else:
						bodies = []	
						tds = row.find_all('td', class_='worklist_first')
						for td in tds:
							data = self.body_str(td.text)
							bodies.append(data)
						newdict = dict(zip(headers, bodies))
						web_data['oppgaver'].append(newdict)

		except:
			print('Text not found')
		
		return web_data