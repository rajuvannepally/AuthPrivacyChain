from django.db import models
from django.utils import timezone
STATUS = (
    ('','Select'),
    ('Activated','Activate'),
    ('Deactivated', 'Deactivate'),)
class Cloud_User(models.Model):
	username = models.CharField(max_length=50,unique=True)
	fname = models.CharField(max_length=50)
	lname = models.CharField(max_length=50)
	address = models.CharField(max_length=50)
	mobile = models.CharField(max_length=20)
	password = models.CharField(max_length=50)
	email = models.EmailField(max_length=50)
	country = models.CharField(max_length=50)
	city = models.CharField(max_length=50)
	zip = models.CharField(max_length=50)
	status = models.CharField(max_length=200,choices=STATUS,null=True)
	def __str__(self):
		return self.username
class Aditor_Detail(models.Model):
	username = models.CharField(max_length=30)
	email = models.EmailField(max_length=30)
	mobile = models.CharField(max_length=30)
	country = models.CharField(max_length=30)
	address = models.CharField(max_length=200)
	city = models.CharField(max_length=30)
	password = models.CharField(max_length=200)
	def __str__(self):
		return self.username
class Upload_File(models.Model):
	user_id = models.ForeignKey(Cloud_User, on_delete=models.CASCADE,null=True)
	name = models.CharField('File Name',max_length=100)
	file = models.FileField('File',upload_to='',null=True)
	notes = models.TextField('Notes',max_length=2000)
	upoaded_date = models.DateField('Uploaded Date',default=timezone.now())
	public_key = models.CharField('Public Key',max_length=1000,null=True,blank=True)
	private_key = models.CharField('Private Key',max_length=1000,null=True,blank=True)
	status = models.CharField('Status',max_length=1000,null=True,blank=True)
	def __str__(self):
		return self.name
class Cloud(models.Model):
	username = models.CharField(max_length=30)
	email = models.EmailField(max_length=30)
	mobile = models.CharField(max_length=30)
	country = models.CharField(max_length=30)
	address = models.CharField(max_length=200)
	city = models.CharField(max_length=30)
	password = models.CharField(max_length=200)
	def __str__(self):
		return self.username