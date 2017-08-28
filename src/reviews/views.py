from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import Http404
from books.models import Book, Category
from .models import Review, Like, User
from .forms import ReviewForm
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# import this for aggregation or group by
from django.db.models import Count
import json
from django.conf import settings

# if printing query is necessary then import below
from django.db import connection
print connection.queries




def get_reviews(request):
	"""
		Get Reviews using ajax
	"""
	context = {}
	category_id = request.POST.get("category_id")

	# get categories
	category_ids = Category.objects.filter(parent=category_id)
	if not category_ids:
		category_ids = Category.objects.filter(pk=category_id)

	# get all the book reviews (remove likes__user_id to group by likes count or have desired result)
	if int(category_id) == 0:
		
		book_review_all = Review.objects.all().prefetch_related('likes').select_related("book",'user_id').annotate(rcount=Count('likes'))\
		.values(
			'id',
			'review_text',
			'audio_review',
			'book__id',
			'book__title',
			'rcount',
			'user_id__username',
			'user_id__first_name',
			'user_id__last_name',
			'user_id__id'
			
			).order_by("-id")
	else:
		
		book_review_all = Review.objects.prefetch_related('likes').select_related("book",'user_id').annotate(rcount=Count('likes'))\
		.values(
			'id',
			'review_text',
			'audio_review',
			'book__id',
			'book__title',
			'rcount',
			'user_id__username',
			'user_id__first_name',
			'user_id__last_name',
			'user_id__id'
			
			).filter(book__category_id__in=category_ids).order_by("-id")
	

	# get data according to pagination
	paginator = Paginator(book_review_all, 5)
	page = request.POST.get("paginator")

	is_new_page = 1
	try:
		book_review = paginator.page(page)
	except PageNotAnInteger:
		book_review = paginator.page(1)
	except EmptyPage:
		is_new_page = 0
		book_review = paginator.page(paginator.num_pages)

	# prepare the dictonary for the data
	review_dict = {}
	i=0
	for review in book_review:
		
		i+=1
		review_id = review.pop('id')
		review_dict[review_id] = review
		# check if this review is liked by current user
		review_dict[review_id]['likes__user_id'] = Like.objects.filter(book_review=Review.objects.get(id=review_id),user=request.user.id).count()

	media_path = settings.MEDIA_URL
	
	context['reviews'] = review_dict 
	context['page'] = page 
	context['is_new_data'] = is_new_page
	context['media_path'] = media_path
	return HttpResponse(JsonResponse(context))


def show_reviews(request,category_id=None):
	"""
		Display All Reviews (Just load the page)
	"""

	context = {}

	if category_id is None:
		category_id = 0

	# get selected category
	if category_id == 0:
		selected_category = 0
	else:
		selected_category = Category.objects.filter(id=category_id)[0].id

	context['categories'] = Category.objects.filter(parent=None)
	context['selected_category'] = selected_category
	context['category_id'] = category_id

	return render(request, "reviews/index.html", context)

def list_reviews(request,book_id=None):
	'''
		Add/Save Review
	'''

	context = {}
	form = ReviewForm(request.POST or None, request.FILES or None)
	# print(User.objects.get(id=request.user.id))

	if request.user.is_authenticated():

		if form.is_valid():
			instance = form.save(commit=False)
			instance.book = Book.objects.get(pk=book_id)
			instance.user_id = request.user
			instance.save()
			return redirect('/reviews/')
	else:
		return redirect('/login/')

	context['form'] = form
	
	try:
		book = Book.objects.get(pk=book_id)
		context['book'] = book
	except Book.DoesNotExist:
		raise Http404("Book review not available")

	print(context)

	return render(request, "reviews/add_review.html", context)

def add_likes(request):

	context = {}
	
	param = int(request.POST.get('param'))
	review_id = request.POST.get('review_id')
	review_obj = Review.objects.get(pk=review_id)

	is_logged = 0
	is_success = 0
	if param:
		
		if request.user.is_authenticated():
			like = Like()
			like.book_review = review_obj
			like.user = request.user
			like.save()
			is_success = 1
			is_logged = 1
		else:
			is_success = 0
			is_logged = 0
	else:
		
		if request.user.is_authenticated():
			try:
				instance = Like.objects.get(book_review = review_obj, user = request.user)
				instance.delete()
				is_success = 1
				is_logged = 1
			except Like.MultipleObjectsReturned:
				is_success = 0
				is_logged = 0
		else:
			is_success = 0
			is_logged = 0

	like_count_total = Like.objects.filter(book_review = review_obj).count()
	like_count_user = 0;
	if request.user.is_authenticated():
		like_count_user = Like.objects.filter(book_review = review_obj, user = request.user).count()

	context['success'] = is_success
	context['logged'] = is_logged
	context['like_count'] = like_count_total
	context['like_count_user'] = like_count_user
	return HttpResponse(JsonResponse(context));
	

