from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.http import Http404
from books.models import Book, Category
from .models import Review
from .forms import ReviewForm


def show_reviews(request):
	"""
		Display All Reviews
	"""

	context = {}
	
	book_review = Review.objects.all().order_by("-id")[:5]
	context['reviews'] = book_review

	return render(request, "reviews/index.html", context)

def list_reviews(request,book_id=None):
	'''
		Add/Save Review
	'''

	context = {}
	
	form = ReviewForm(request.POST or None)

	if form.is_valid():
		instance = form.save(commit=False)
		instance.book = Book.objects.get(pk=book_id)
		instance.user_id = request.user
		instance.save()
		return redirect('/reviews/')

	context['form'] = form
	
	try:
		book = Book.objects.get(pk=book_id)
		context['book'] = book
	except Book.DoesNotExist:
		raise Http404("Book review not available")

	print(context)

	return render(request, "reviews/add_review.html", context)

