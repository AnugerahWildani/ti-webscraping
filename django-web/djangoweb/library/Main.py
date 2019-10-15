from pykeepass import PyKeePass
import os
import requests
from bs4 import BeautifulSoup
import time
import json
from datetime import datetime
import shutil

# import SkatteFunnParser as SFP
# import Urls as url_
import djangoweb.library.SkatteFunnParser as SFP
import djangoweb.library.Urls as url_

def save_to_folder(path, data, user, project, web_id):
	create_time = datetime.now().strftime('%Y-%m-%d-%H%M')
	if os.path.exists(path):
		write_json(path, user, data, create_time, project, web_id)
			
	else:
		os.mkdir(path)
		write_json(path, user, data, create_time, project, web_id)
   
def write_json(path, user, data, create_time, project, web_id):
	email = user.username.replace("@", "_at_").replace(".", "_dot_")
	project_dir = os.path.join(path, project)
	if os.path.exists(project_dir):
		save_per_url(project_dir, user, data, create_time, project, web_id)
	else:
		os.mkdir(project_dir)
		save_per_url(project_dir, user, data, create_time, project, web_id)

def save_per_url(project_dir, user, data, create_time, project, web_id):
	email = user.username.replace("@", "_at_").replace(".", "_dot_")
	url_dir = os.path.join(project_dir, web_id)
	if os.path.exists(url_dir):
		file_name = os.path.join(url_dir, email+'_'+project+'_'+web_id+'_'+user.title+'_'+create_time+'.json')
	else:
		os.mkdir(url_dir)
		file_name = os.path.join(url_dir, email+'_'+project+'_'+web_id+'_'+user.title+'_'+create_time+'.json')

	with open(file_name, 'w') as fn:
		json.dump(data, fn, indent=4, ensure_ascii=False)
	print("File successfully created", file_name)

	list_of_files = os.listdir(url_dir)
	full_path = [os.path.join(url_dir,"{0}".format(x)) for x in list_of_files]
	if len([name for name in list_of_files]) == 3:
		oldest_file = min(full_path, key=os.path.getctime)
		os.remove(oldest_file)

def Publish(keepassword):
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	archive_path = os.path.join(BASE_DIR, 'archive')

	with PyKeePass(os.path.join(archive_path, 'userdb.kdbx'), password=keepassword) as kp:
		entries = kp.find_entries(title='SkatteFunn')
		web_folder = os.path.join(archive_path, 'SkatteFunn')

		for entry in entries:

			if entry.title == 'SkatteFunn':

				website = SFP.SkatteFunnParser(entry.url, entry.username, entry.notes)
				website_login, session = website.change_log_in(entry.username,entry.password)
				website.print_settings()
				i = 0
				
				test_data_path = os.path.join(BASE_DIR, 'test-data')
				urls = []
				prosjekter = os.path.join(test_data_path, entry.notes, entry.notes + '_mittNettstedWeb_portlets_prosjekt_prosjekter.do_.html')
				detail = os.path.join(test_data_path, entry.notes, entry.notes + '_mittNettstedWeb_portlets_prosjekt_visDetaljerSkattefunn.doprojectId=305708_.html')
				begin = os.path.join(test_data_path, entry.notes, entry.notes + '_mittNettstedWeb_portlets_soknad_begin.do_.html')
				soknader = os.path.join(test_data_path, entry.notes, entry.notes + '_mittNettstedWeb_portlets_prosjekt_soknader.do_.html')
				detail2 = os.path.join(test_data_path, entry.notes, entry.notes + '_mittNettstedWeb_portlets_prosjekt_visDetaljerSkattefunn.doprojectId=304184_.html')
				detail3 = os.path.join(test_data_path, entry.notes, entry.notes + '_mittNettstedWeb_portlets_prosjekt_visDetaljerSkattefunn.doprojectId=269913_.html')
				if os.path.isfile(prosjekter):
					urls.append(prosjekter)
				if os.path.isfile(detail):
					urls.append(detail)
				if os.path.isfile(begin):
					urls.append(begin)
				if os.path.isfile(soknader):
					urls.append(soknader)
				if os.path.isfile(detail2):
					urls.append(detail2)
				if os.path.isfile(detail3):
					urls.append(detail3)
				
				urls_main = []
				main_web = os.path.join(test_data_path, entry.notes, entry.notes + '_nomittNettstedWeb_.html')
				if os.path.isfile(main_web):
					urls_main.append(main_web)

				for url in urls:
					output = website.get_data(url, session)
					project = entry.notes
					if os.name == 'nt':
						url_name = url.split('\\')[-1].split('_')[4].replace('.', '_')
					else:
						url_name = url.split('/')[-1].split('_')[4].replace('.', '_')
					save_to_folder(web_folder, output, entry, project, url_name)
					i += 1

				for url in urls_main:
					output = website.get_data_main(url, session)
					project = entry.notes
					url_name = 'main'
					save_to_folder(web_folder, output, entry, project, url_name)
					i += 1


# Publish()