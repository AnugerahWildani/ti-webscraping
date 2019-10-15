from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import os
import json
from djcelery.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from django.contrib import messages
from pykeepass import PyKeePass
from .forms import UpdateScheduleForm
from django.shortcuts import get_object_or_404
from croniter import croniter
from datetime import datetime
from django.http import HttpResponseRedirect
from cryptography.fernet import Fernet
from djangoweb.library.GenerateKey import key
from djangoweb.library.CompareData import compare_data

@login_required
def dashboard(request):	
	BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
	lib = os.path.dirname(BASE_DIR)
	all_data = []
	try:
		folder_path = os.path.join(lib, 'django-web', 'djangoweb', 'archive', 'SkatteFunn')
	except:
		print('Folder not  found')
	else:
		list_dir = os.listdir(folder_path)
		for folder in list_dir:
			table_datas = []
			if request.user.is_superuser:
				folder_json = os.path.join(folder_path, folder)
				list_url_folder = os.listdir(folder_json) 
				per_web = []
				for folder_url in list_url_folder:
					folder_url_file = os.path.join(folder_json, folder_url)
					list_url_folder_file = os.listdir(folder_url_file)
					full_path = [os.path.join(folder_url_file,"{0}".format(x)) for x in list_url_folder_file]
					for name in list_url_folder_file:
						newest_file = max(full_path, key=os.path.getctime)
						file_json = os.path.join(folder_url_file, name)
						if newest_file == file_json:
							jsonData = open(newest_file)
							data = json.load(jsonData)
							result = compare_data(folder_url_file)
							data['change'] = result
							per_web.append(data)

			else:
				folder_json = os.path.join(folder_path, folder)
				list_url_folder = os.listdir(folder_json) 
				per_web = []
				for folder_url in list_url_folder:
					folder_url_file = os.path.join(folder_json, folder_url)
					list_url_folder_file = os.listdir(folder_url_file)
					full_path = [os.path.join(folder_url_file,"{0}".format(x)) for x in list_url_folder_file]
					for name in list_url_folder_file:
						newest_file = max(full_path, key=os.path.getctime)
						file_json = os.path.join(folder_url_file, name)
						if newest_file == file_json:
							jsonData = open(newest_file)
							data = json.load(jsonData)
							result = compare_data(folder_url_file)
							data['change'] = result
							if data['username'] == request.user.username:						
								per_web.append(data)

			for table in per_web:
				table_content = {}
				table_content['username'] = table.get('username')
				table_content['timestamp'] = table.get('timestamp')
				table_content['project_name'] = folder
				table_content['title'] = table.get('title')
				table_content['change'] = table.get('change')
				uname = table.get('url_name')
				if uname == 'soknader_do':
					table_soknader = table.get('data_table')
					table_content['url'] = table.get('url')
					table_content['table_soknader'] = table_soknader
				elif uname == 'main':
					table_info = table.get('info')
					table_content['table_info'] = table_info
					table_content['under_arbeid'] = table.get('under_arbeid')
					table_content['brev'] = table.get('brev')
				elif uname == 'begin_do':
					table_begin = table.get('data_table')
					table_content['url'] = table.get('url')
					table_content['table_begin'] = table_begin
				elif uname == 'prosjekter_do':
					table_prosjekter = table.get('data_table')			
					table_content['url'] = table.get('url')
					table_content['table_prosjekter'] = table_prosjekter
				else:
					table_brev = table.get('prosjektbrev')
					table_rapporter = table.get('prosjektrapporter')
					table_historikk = table.get('historikk')
					table_content['url'] = table.get('url')
					table_content['table_brev'] = table_brev
					table_content['table_rapporter'] = table_rapporter
					table_content['table_historikk'] = table_historikk
				table_datas.append(table_content)
			all_data.append(table_datas)
	
	return render(request,'dashboard.html', {
		'table_datas': all_data
	})	

@login_required
def update_schedule(request, task_id):
	# schedule = CrontabSchedule.objects.get(id=task_id)
	schedule = get_object_or_404(CrontabSchedule, id=task_id)
	data = {
		'minute': schedule.minute,
		'hour': schedule.hour,
		'day_of_week': schedule.day_of_week,
		'day_of_month': schedule.day_of_month,
		'month_of_year': schedule.month_of_year
		}
	if request.method == 'POST' and 'update_schedule' in request.POST:

		form = UpdateScheduleForm(request.POST or None, initial=data, instance=schedule)

		if form.is_valid():
			form.save()

			messages.success(request, 'Scheduler has been updated') 
			return redirect('skattefunn')

		else:
			return render(request, "update_schedule.html", {'data':data, 'form':form, 'page_title': 'Update Schedule Data'})
	
	return render(request, 'update_schedule.html', {'data':data, 'page_title': 'Update Scheduler'})

@login_required
def delete_schedule(request, task_id):
	schedule = get_object_or_404(CrontabSchedule, id=task_id)
	schedule.delete()
	messages.success(request, 'Scheduler has been deleted') 
	return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	return render(request, 'delete_schedule.html')

class loginViews(TemplateView):
	template_name = 'login.html'
		
def loginView(request):
	context = {
		'page_title': 'Login',
	}
	if request.method == "POST":
		
		username_login = request.POST['username']
		password_login = request.POST['password']

		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		archive_path = os.path.join(BASE_DIR, 'djangoweb', 'archive')
		try:
			load_database = PyKeePass(os.path.join(archive_path, 'userdb.kdbx'), password=password_login)
			user_valid = authenticate(request, username=username_login, password= password_login)

		except:
			user_valid = authenticate(request, username=username_login, password= password_login)
			# messages.error(request, 'Username and password do not match')
			user = None
			user_admin = None
		else:
			with load_database as kp:
				user = kp.find_entries(username= username_login, password= password_login, title='SkatteFunn', first= True)
				user_admin = kp.find_entries(username= username_login, password= password_login, title= 'Admin', first= True)
				print(user)
		# user_valid = authenticate(request, username=username_login, password= password_login)
		print(user_valid)
		if user is not None or user_admin is not None or user_valid is not None:
			if user_valid is not None:
				login(request, user_valid)
				return redirect('dashboard')
			else:
				info = password_login.encode()
				f = Fernet(key)
				encrypted = f.encrypt(info)
				decoded_password = encrypted.decode()
				new_user = User.objects.create_user(username_login, password=password_login, first_name=decoded_password)
				if user is not None:
					new_user.is_staff = True
				elif user_admin is not None:
					new_user.is_staff = True
					new_user.is_superuser = True 
				new_user.save()
				login(request, new_user)
				return redirect('dashboard')
		else:
			messages.error(request, 'Username and password do not match')
			return redirect('login')

	return render(request, 'login.html',context)
	
@login_required
def logoutView(request):
	context = {
		'page_title':'Logout',
	}

	if request.method == "POST":
		if request.POST["logout"] == "Submit":
			logout(request)

		return redirect('login')
	return render(request, 'logout.html',context)

@login_required
def skattefunn(request):
	encoded = request.user.first_name.encode()
	f = Fernet(key)
	decrypted = f.decrypt(encoded)
	decoded = decrypted.decode()

	if request.method == 'POST' and 'run_script' in request.POST:
		from djangoweb.library.Main import Publish
		Publish(decoded)
		messages.success(request, 'Data has been updated') 
		return redirect('skattefunn')

	if request.method == 'POST' and 'update_schedule' in request.POST:
		form = UpdateScheduleForm(request.POST)

		if form.is_valid():
			post = form.save(commit=False)
			post.save()
			create_periodic = PeriodicTask.objects.create(crontab=post, interval=None, name=datetime.now(),task='webscrap.tasks.runscript')
			messages.success(request, 'Scheduler has been updated') 
			return redirect('skattefunn')
	else:
		form = UpdateScheduleForm()
	
	task_list = CrontabSchedule.objects.all()
	data_schedule = []
	for task in task_list:
		cron_data = str(task.minute)+' '+str(task.hour)+' '+str(task.day_of_week)+' '+str(task.day_of_month)+' '+str(task.month_of_year)
		base = datetime.now()
		iterate = croniter(cron_data, base) 
		next_schedule = iterate.get_next(datetime)
		data_schedule.append(next_schedule)

	home = os.getcwd()
	archive_path = os.path.join(home, 'djangoweb', 'archive')
	if request.method == 'POST' and 'import_user' in request.POST:
		with PyKeePass(os.path.join(archive_path, 'userdb.kdbx'), password=decoded) as kp:
			entries = kp.find_entries(title='SkatteFunn')
			for entry in entries:
				if User.objects.filter(username=entry.username).exists():
					print('already exist')
				else:
					new_user = User.objects.create_user(entry.username, password=entry.password)
					new_user.is_staff = True
					new_user.save()
				
			messages.success(request, 'Users have been imported')
			return redirect('skattefunn')
	user_list = User.objects.all()


	return render(request, 'skattefunn.html', {
		'task_list': task_list,		
		'user_list': user_list,
		'data_schedule': data_schedule,
		'form': form,
	})
