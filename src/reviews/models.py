from __future__ import unicode_literals
from datetime import timedelta
from django.db import models
from django.core.urlresolvers import reverse
from decimal import Decimal
import time
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User,Group


def get_upload_file_name(instance, filename):
	return "uploaded_audio_review/%s_%s" % (str(time.time()).replace(".","_"), filename)


class Review(models.Model):
	''' Reviw for the book '''

	book = models.ForeignKey('books.Book')
	review_text = RichTextField() #models.TextField()
	user_id = models.ForeignKey(User)
	audio_review = models.FileField(blank=True, null=True, upload_to=get_upload_file_name)

	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	def __str__(self):
		return str(self.book)

	def __unicode__(self):
		return str(self.book)


class Like(models.Model):
	book_review = models.ForeignKey(Review, related_name="likes")
	user = models.ForeignKey(User)

	def __str__(self):
		return str(self.book_review) + " : " + str(self.user) + " : "+ str(self.book_review.id)

	def __unicode__(self):
		return str(self.book_review) + " : " + str(self.user) + " : "+ str(self.book_review.id)


