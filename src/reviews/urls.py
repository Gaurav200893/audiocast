from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
	url(r'^$', views.show_reviews, name="review_index"),
	url(r'^(?P<category_id>[0-9]+)/$', views.show_reviews, name="review_book"),
	url(r'^ajax/getreview/$', views.get_reviews, name="review_ajax"),
	url(r'^add/(?P<book_id>[0-9]+)/$', views.list_reviews, name="review_book"),
	url(r'^add/like/$', views.add_likes, name="add_review_like"),
]