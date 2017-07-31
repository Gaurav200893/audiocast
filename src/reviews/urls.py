from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.show_reviews, name="review_index"),
	url(r'^add/(?P<book_id>[0-9]+)/$', views.list_reviews, name="review_book"),
]