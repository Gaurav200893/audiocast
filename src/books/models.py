from __future__ import unicode_literals
from datetime import timedelta
from django.contrib.auth.models import User,Group
from django.db import models
from django.core.urlresolvers import reverse
from decimal import Decimal
import time

def get_upload_file_name(instance, filename):
	return "uploaded_audio/%s_%s" % (str(time.time()).replace(".","_"), filename)



class Category(models.Model):
	''' Categories for books '''

	category_name = models.CharField(max_length=50)
	parent = models.ForeignKey('self', blank=True, null=True, related_name='child')

	def __unicode__(self):
		return self.category_name

	def __str__(self):
		return self.category_name

	class Meta:
		verbose_name = "category"
		verbose_name_plural = "categories"





class Book(models.Model):
	''' 
		Class of books
	'''

	BANNER_CHOICE = (
			('On', 'on'),
			('Off', 'off')
		)

	FEATURE_CHOICE=(
			('On', 'on'),
			('Off', 'off')
		)

	isbn = models.CharField(max_length=120)
	title = models.CharField(max_length=120)
	description = models.TextField()

	# from users
	author_id = models.ManyToManyField('Author')
	#models.OneToOneField(User,related_name='user_author')
	narrator_id = models.ManyToManyField('Narrator')
	#models.OneToOneField(User,related_name='user_narrator')

	length = models.DurationField(default=timedelta(minutes=20))

	# from program format
	program_format = models.ForeignKey('ProgramFormat', null=True)
	release_date = models.DateTimeField(auto_now=False, auto_now_add=False)

	publisher = models.ForeignKey('Publisher',null=False)
	image = models.FileField(null=True, blank=True)
	audio_link = models.FileField(upload_to=get_upload_file_name)

	category_id = models.ForeignKey('Category', null=True)

	is_banner = models.CharField(max_length=10, choices=BANNER_CHOICE)
	is_featured = models.CharField(max_length=10, choices=FEATURE_CHOICE)
	# language_categories = models.ManyToManyField('Language')
	# price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))

	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	# join the authors
	def author_join(self):
		authors = ''
		authors = ", ".join(str(author) for author in self.author_id.all())
		return authors

	# join the narrators
	def narrator_join(self):
		narrators = ''
		narrators = ", ".join(str(narrator) for narrator in self.narrator_id.all())
		return narrators

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

class Currency(models.Model):
	''' Set Currency Symbol '''

	currency_name = models.CharField(max_length=255)
	currency_symbol = models.CharField(max_length=10)

	def __unicode__(self):
		return self.currency_name+" - "+self.currency_symbol

	def __str__(self):
		return self.currency_name+" - "+self.currency_symbol


class Rating(models.Model):
	''' Books Rating '''

	book = models.ForeignKey(Book)
	user_id = models.OneToOneField(User)
	rating = models.IntegerField(default=0)


class Price(models.Model):
	''' Price for book '''

	book = models.ForeignKey('Book')
	language = models.ForeignKey('Language')
	currency = models.ForeignKey('Currency', related_name="price_currency")
	price_tag = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('0.00'))


	def __unicode__(self):
		return self.book.title +" - "+ str(self.price_tag)

	def __str__(self):
		return self.book.title +" - "+  str(self.price_tag)
	

class Author(models.Model):
	''' Author for the book '''

	author_name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.author_name

	def __str__(self):
		return self.author_name



class Narrator(models.Model):
	''' Narrator for the book '''
	
	narrator_name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.narrator_name

	def __str__(self):
		return self.narrator_name


# No need for using user profile now
class UserProfile(models.Model):
	''' Users in the system  '''

	user = models.OneToOneField(User)
	group = models.ForeignKey('Group',null=True)


class Group(models.Model):
	''' Groups for the user '''

	group_name = models.CharField(max_length=120)

	def __unicode__(self):
		return self.group_name

	def __str__(self):
		return self.group_name


class ProgramFormat(models.Model):
	''' Program format for audiobooks '''

	program_name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.program_name

	def __str__(self):
		return self.program_name


class Language(models.Model):
	''' Language for the books '''

	language_name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.language_name

	def __str__(self):
		return self.language_name

class Publisher(models.Model):
	''' Publisher for the book  '''

	publisher_name = models.CharField(max_length=255)

	def __unicode__(self):
		return self.publisher_name

	def __str__(self):
		return self.publisher_name




