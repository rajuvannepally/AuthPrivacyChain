from django.shortcuts import render,redirect,get_object_or_404
from . models import *
from django.contrib import messages
import datetime
from django.db.models import Q
from django.db import connection
import random 
from django.db.models import Sum, Count
from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.core.mail import EmailMessage
import datetime
from django.conf import settings
import os
from cryptography.fernet import Fernet
import random  
import string  
def public_key(length):  
    sample_string = 'd0LW25jG8feETs4WWpeCUA4AU1oPj7lAcCtKB1Cmuso=' # define the specific string  
    # define the condition for random string  
    result = ''.join((random.choice(sample_string)) for x in range(length))  
    return result 
def private_key(length):  
    sample_string = 'd0LW25jG8feETs4WWpeCUA4AU1oPj7lAcCtKB1Cmuso=' # define the specific string  
    # define the condition for random string  
    result = ''.join((random.choice(sample_string)) for x in range(length))  
    return result 
def register(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		address = request.POST.get('address')
		mobile= request.POST.get('mobile')
		email = request.POST.get('email')
		password = request.POST.get('password')
		fname = request.POST.get('fname')
		lname = request.POST.get('lname')
		country = request.POST.get('country')
		city = request.POST.get('city')
		zip = request.POST.get('zip')
		crt = Cloud_User.objects.create(username=username,
		address=address,mobile=mobile,password=password,email=email,fname=fname,lname=lname,
		city=city,country=country,zip=zip)
		if crt:
			messages.success(request,'Registered Successfully')
	return render(request,'register.html',{})
def dashboard(request):
	user = Cloud_User.objects.all().aggregate(Count('id'))
	a = Cloud_User.objects.filter(status='Activated').aggregate(Count('id'))
	b = Cloud_User.objects.filter(status='Deactivated').aggregate(Count('id'))
	e = Upload_File.objects.filter(status='Pending').aggregate(Count('id'))
	f = Upload_File.objects.filter(status='SENT To CLOUD').aggregate(Count('id'))
	return render(request,'dashboard.html',{'user':user,'a':a,'b':b,'e':e,'f':f})
def user_login(request):
	if request.session.has_key('username'):
		return redirect("user_dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =  request.POST.get('password')
			post = Cloud_User.objects.filter(username=username,password=password,status='Activated')
			if post:
				username = request.POST.get('username')
				request.session['username'] = username
				a = request.session['username']
				sess = Cloud_User.objects.only('id').get(username=a).id
				request.session['user_id']=sess
				return redirect("user_dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'index.html',{})
def user_dashboard(request):
	if request.session.has_key('username'):
		return render(request,'user_dashboard.html',{})
	else:
		return render(request,'index.html',{})
def logout(request):
	try:
		del request.session['username']
		del request.session['user_id']
	except:
		pass
	return render(request, 'index.html', {})
def aditor_login(request):
	if request.session.has_key('admin'):
		return redirect("dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =  request.POST.get('password')
			post = Aditor_Detail.objects.filter(username=username,password=password)
			if post:
				username = request.POST.get('username')
				request.session['admin'] = username
				a = request.session['admin']
				sess = Aditor_Detail.objects.only('id').get(username=a).id
				request.session['admin_id']=sess
				return redirect("dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'aditor_login.html',{})
def aditor_logout(request):
	try:
		del request.session['admin']
		del request.session['admin_id']
	except:
		pass
	return render(request, 'aditor_login.html', {})
def upload_file(request):
	if request.session.has_key('username'):
		uid = request.session['user_id']
		user_id = Cloud_User.objects.get(id=int(uid))
		if request.method == 'POST':
			name = request.POST.get('name')
			notes = request.POST.get('notes')
			a = request.FILES['file']
			crt = Upload_File.objects.create(user_id=user_id,name=name,notes=notes,
			file=a,status='Pending')
			if crt:
				messages.success(request, 'File Uploaded Waiting for Aditor to send the File to Cloud.')
				cursor = connection.cursor()
				sql='''select  f.file,f.id from app_upload_file as f order by f.id DESC'''
				post = cursor.execute(sql)
				row = cursor.fetchone()
				a = str(row[0])
				b = str(row[1])
				directory = os.getcwd()
				file_name = directory+"/media/"
				img = file_name+a
				class Encryptor():
					
					def key_create(self):
						key = Fernet.generate_key()
						return key

					def key_write(self, key, key_name):
						with open(key_name, 'wb') as mykey:
							mykey.write(key)

					def key_load(self, key_name):
						with open(key_name, 'rb') as mykey:
							key = mykey.read()
						return key


					def file_encrypt(self, key, original_file, encrypted_file):
						
						f = Fernet(key)

						with open(original_file, 'rb') as file:
							original = file.read()

						encrypted = f.encrypt(original)

						with open (encrypted_file, 'wb') as file:
							file.write(encrypted)

					def file_decrypt(self, key, encrypted_file, decrypted_file):
						
						f = Fernet(key)

						with open(encrypted_file, 'rb') as file:
							encrypted = file.read()

						decrypted = f.decrypt(encrypted)

						with open(decrypted_file, 'wb') as file:
							file.write(decrypted)

				encryptor=Encryptor()

				mykey=encryptor.key_create()

				encryptor.key_write(mykey, file_name+a+'.key')

				loaded_key=encryptor.key_load(file_name+a+'.key')

				encryptor.file_encrypt(loaded_key, img, file_name+'enc_'+a)
				encryptor.file_decrypt(loaded_key, file_name+'enc_'+a, file_name+'dec_'+a)
		return render(request,'upload_file.html',{})
	else:
		return render(request,'index.html',{})
def cloud_login(request):
	if request.session.has_key('cloud'):
		return redirect("cloud_dashboard")
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =  request.POST.get('password')
			post = Cloud.objects.filter(username=username,password=password)
			if post:
				username = request.POST.get('username')
				request.session['cloud'] = username
				a = request.session['cloud']
				sess = Cloud.objects.only('id').get(username=a).id
				request.session['cloud_id']=sess
				return redirect("cloud_dashboard")
			else:
				messages.success(request, 'Invalid Username or Password')
	return render(request,'cloud.html',{})
def cloud_dashboard(request):
	if request.session.has_key('cloud'):
		return render(request,'cloud_dashboard.html',{})
	else:
		return render(request,'cloud.html',{})
def clogout(request):
	try:
		del request.session['cloud']
		del request.session['cloud_id']
	except:
		pass
	return render(request, 'cloud.html', {})
def files(request):
	if request.session.has_key('username'):
		uid = request.session['user_id']
		a = Upload_File.objects.filter(user_id=int(uid),status='Pending')
		return render(request,'files.html',{'b':a})
	else:
		return render(request,'index.html',{})
def user_detail(request):
	if request.session.has_key('admin'):
		uid = request.session['admin_id']
		a = Cloud_User.objects.filter(status='Activated')
		return render(request,'users.html',{'b':a})
	else:
		return render(request,'index.html',{})
def send_cloud(request):
	if request.session.has_key('admin'):
		uid = request.session['admin_id']
		a = Upload_File.objects.filter(status='Pending')
		return render(request,'send_cloud.html',{'b':a})
	else:
		return render(request,'index.html',{})
def upload(request,pk):
	if request.session.has_key('admin'):
		uid = request.session['admin_id']
		pkey = public_key(20)
		b = private_key(25)
		a = Upload_File.objects.filter(status='Pending',id=pk).update(status='SENT To CLOUD',
		public_key=pkey,private_key=b)
		recipient_list = [request.GET.get('email')]
		email_from = settings.EMAIL_HOST_USER
		b = EmailMessage('Public and Private Keys',
		'Public Key:  ' + pkey + '  Private Key:  ' + b ,email_from,recipient_list).send()
		
		return redirect('send_cloud')
	else:
		return render(request,'index.html',{})
def up_files(request):
	if request.session.has_key('admin'):
		uid = request.session['admin_id']
		a = Upload_File.objects.filter(status='SENT To CLOUD')
		return render(request,'upload.html',{'b':a})
	else:
		return render(request,'index.html',{})
def cloud_files(request):
	if request.session.has_key('username'):
		uid = request.session['user_id']
		a = Upload_File.objects.filter(status='SENT To CLOUD',user_id=int(uid))
		return render(request,'cloud_files.html',{'b':a})
	else:
		return render(request,'index.html',{})
def download_file(request,pk):
	if request.session.has_key('username'):
		uid = request.session['user_id']
		if request.method == 'POST':
			pkey = request.POST.get('pkey')
			prkey =  request.POST.get('prkey')
			detail = Upload_File.objects.filter(public_key=pkey,private_key=prkey,id=pk)
			if detail:
				return render(request,'download_file.html',{'b':detail})
			else:
				messages.success(request, 'You have entered wrong keys pls check the keys.')
		
		return render(request,'download_file.html',{})
	else:
		return render(request,'index.html',{})
from django.db.models import Count
from django.http import JsonResponse
def chart(request):
	
	return render(request,'chart.html',{})
def chart_ajax(request):
	cursor = connection.cursor()
	post = ''' SELECT Count(app_cloud_user.username) from app_cloud_user where 
	app_cloud_user.status='Activated' '''
	sub = cursor.execute(post)
	row = cursor.fetchall()
	post1 = ''' SELECT Count(app_upload_file.id) from app_upload_file where 
	app_upload_file.status='SENT To CLOUD' '''
	sub1 = cursor.execute(post1)
	row1 = cursor.fetchall()
	post2 = ''' SELECT Count(app_upload_file.id) from app_upload_file where 
	app_upload_file.status='Pending' '''
	sub2 = cursor.execute(post2)
	row2 = cursor.fetchall()
	post3 = ''' SELECT Count(app_cloud_user.username) from app_cloud_user where 
	app_cloud_user.status='Deactivated' '''
	sub3 = cursor.execute(post3)
	row3 = cursor.fetchall()
	data = {
	'row':row,
	'row1':row1,
	'row2':row2,
	'row3':row3,
	}
	return JsonResponse(data)