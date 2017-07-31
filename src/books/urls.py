from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
  	url(r'^$', views.IndexView.as_view(), name="index"),
  	url(r'^world-reads/$', views.WorldReads.as_view(), name="world-read"),
  	url(r'^world-reads-book/(?P<pk>[0-9]+)/$', views.WorldReadsBook.as_view(), name="world-read"),
  	
	url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name="detail"),
	url(r'^category_link/(?P<category_id>[0-9]+)/$', views.CategoryView.as_view(), name="category_link"),
	url(r'^category_link/$', views.CategoryView.as_view(), name="category_link"),
	url(r'^ajax/(?P<pk>[0-9]+)/$', views.LanguagePriceView.as_view(), name="language_price"),
	url(r'^ajax/rating/$', views.RatingView.as_view(), name="rating"),
	
]