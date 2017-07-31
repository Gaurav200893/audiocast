from django.views import generic
from django.utils.decorators import method_decorator
from django.http import JsonResponse,HttpResponse
from django.core import serializers
# from .models import Book, Category, Price, 
from .models import Book, Category, Price, Currency, Language, Rating, User
import tweepy
# import this for aggregation or group by
from django.db.models import Count


def getTweets(country_name):
	''' Get the tweets '''

	ACCESS_TOKEN = "884317426711543810-TnQVyXM3d8y7kdiPXo32jtVKmXdXcwD"
	ACCESS_SECRET = "ztc0WfhtV4BDAUIVWWXgw2M7XXC5f0F7vC4e3mln3Olah" 
	CONSUMER_KEY = "SkqreObweTWiKVI1X0qjJ7a6B"
	CONSUMER_SECRET = "wIXEyi6mxitwlnyP9GJK3mzpIkr9QL6q5OLXXq4dBtS2iFIbP4"

	# get place
	auth2 = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	auth2.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
	api2 = tweepy.API(auth2)
	places = api2.geo_search(query=country_name, granularity="country")
	place_id = places[0].id

	auth = tweepy.AppAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
	api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

	remaining_query = api.rate_limit_status()['resources']['search']
	# print(remaining_query)

	searchQuery = 'place:'+place_id+'  #read OR #reading OR #bookread OR' \
              '#bookworm OR #books OR #readbook OR #readbooks OR #booklover OR #readinglover' \
              'OR "reading" OR "read book" OR "reading book" OR "book read" OR "book lover" OR "reading lover"'
    
    #Maximum number of tweets we want to collect 
	maxTweets = 10

	#The twitter Search API allows up to 100 tweets per query
	tweetsPerQry = 100

	if (not api):
   		country_tweets.append("Problem connecting to API")

   	country_tweets = []
	for tweet in tweepy.Cursor(api.search,q=searchQuery).items(maxTweets) :
		country_tweets.append(tweet.text)

	if not country_tweets:
		country_tweets.append("No data available yet.")


	return country_tweets


class IndexView(generic.ListView):
	''' Index page '''

	template_name = "book_index.html"
	context_object_name = "all_books"

 	# pass the book object (required)
	def get_queryset(self):
		return Book.objects.all()

	# pass other objects
	def get_context_data(self, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		context['all_categories'] = Category.objects.all()
		return context


class WorldReads(generic.ListView):
	''' Tweets on the world '''

	template_name = "world_tweets.html"

	def get_queryset(self):
		return Book.objects.all()

	def post(self, request, *args, **kwargs):
		context = {}
		country_name = request.POST['country_name']
		tweets = []
		try:
			tweets = getTweets(country_name)
		except Exception:
			tweets.append("Please try after sometime.")

		return HttpResponse(JsonResponse(tweets, safe=False))

class WorldReadsBook(generic.ListView):

	template_name = "world_tweets.html"
	context_object_name = "selected_books"

	def get_queryset(self):
		return Book.objects.all()

	def post(self, request, *args, **kwargs):
		context = {}
		country_name = request.POST['country_name']
		tweets = []
		try:
			tweets = getTweets(country_name)
		except Exception:
			tweets.append("Please try after sometime.")

		return HttpResponse(JsonResponse(tweets, safe=False))


class CategoryView(generic.ListView):
	''' Display Books By Category '''

	template_name = "category_detail.html"
	context_object_name= "books_by_category"

	def get_queryset(self):
		''' Get the details for the Categorical View of the books '''

		category_ids = None
		''' Get the children ids if the passed id is parent id '''
		category_children_ids = Category.objects.filter(parent=self.kwargs.get('category_id',"0")).values("id")
		
		
		# assign the category ids
		if not category_children_ids:
			category_ids = self.kwargs.get('category_id',"0")
		else:
			category_ids = category_children_ids
			
		if int(self.kwargs.get('category_id',"0")):
			return Book.objects.filter(category_id__in=category_ids)
		else:
			return Book.objects.all()

	def get_context_data(self, **kwargs):
		''' Get the data for the given Category '''

		context = super(CategoryView, self).get_context_data(**kwargs)
		context['all_categories'] = Category.objects.all()
		context['selected_category']= int(self.kwargs.get('category_id',"0"))
		
		# assign collapse for the category
		parent_id = Category.objects.filter(child=self.kwargs.get('category_id',"0")).values("id")


		# check if parent exits
		collapse_var = "collapse"
		match_parent = self.kwargs.get('category_id',"0")
		if parent_id:
			collapse_var ="in"
			match_parent = parent_id

		context['collapse_category'] = collapse_var
		context['matches_parent'] = match_parent
		return context



# class DetailView(generic.DetailView):
# 	''' Get the book detail '''

# 	model = Book
# 	template_name = "book_detail.html"

# 	# pp= Price.objects.all().values("currency") #Price.objects.all().values("currency")
# 	# print("//--------")
# 	# print(pp)
# 	# cc = Currency.objects.filter(id__in=pp)
# 	# print(cc)
# 	def get_context_data(self, **kwargs):
# 		context = super(DetailView, self).get_context_data(**kwargs)
# 		book_obj = Book.objects.get()
# 		book_price = Price.objects.filter(book=book_obj)
# 		print(book_price.price_currency)
# 		currency_list = Currency.objects.filter(id__in=book_price)
# 		context['price_tags'] = book_price
# 		return context


class JSONResponseMixin(object):
	def render_to_json_response(self, context, **response_kwargs):
		''' Returns a JSON response, transforming 'context' to make the payload. '''

		return JsonResponse(
			self.get_data(context),
			**response_kwargs
			)

	def  get_data(self, context):
		''' 
		Returns obj that is serialized by json.dump()
		'''

		return context


# @method_decorator(login_required, name='dispatch') #LOGIN_URL = '/login/'
class DetailView(JSONResponseMixin, generic.DetailView):
	''' Get the Details Page with the ajax price '''
	model = Book
	template_name = "book_detail.html"

	def get_context_data(self, **kwargs):

		context = super(DetailView, self).get_context_data(**kwargs)
		currency_list_ids = Price.objects.all().values('currency')
		language_list_ids = Price.objects.all().values('language')	


		

		# overall rating
		overall_rating = None

		is_rating_exists = Rating.objects.filter(book = self.kwargs.get('pk')).count()

		if is_rating_exists:
			overall_rating = Rating.objects.filter(book = self.kwargs.get('pk'))\
			.values("rating")\
			.annotate(rcount=Count('rating'))\
			.order_by('-rcount')\
			.order_by('-rating')[0]

		# users rating
		book_rating = None

		if self.request.user.is_authenticated():
			book_rating = Rating.objects.filter(book = self.kwargs.get('pk'),user_id=self.request.user).values("rating")
		
		if book_rating:
			rating = book_rating[0]['rating']
		else:
			rating = 0

		context['price_list'] = Price.objects.all().values('currency', 'language', 'price_tag')
		context['currency_list'] = Currency.objects.filter(id__in=currency_list_ids)
		context['language_list'] = Language.objects.filter(id__in=language_list_ids)
		context['book_rating'] = rating
		context['overall_rating'] = overall_rating
		return context


class LanguagePriceView( generic.DetailView):
	''' Get price on basis of language '''

	model = Book

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		book_id = self.object.id
		# book language and price
		book_language = request.POST['language']
		book_prices = Price.objects.filter(language=book_language,book=book_id)
		
		# currency and price tags
		currency_list = Currency.objects.filter(pk=book_prices.values("currency_id"))

		price_tags = Currency.objects.filter()
		context_dict = {}

		try:
			context_dict['is_sucess'] = 1
			context_dict['price_list'] = serializers.serialize('json',book_prices)
			context_dict['currency_list'] = serializers.serialize('json',currency_list)
		except:
			context_dict['is_sucess'] = 0

		return HttpResponse(JsonResponse(context_dict))


class RatingView(generic.TemplateView):
	''' Rating update accoding to user '''
	
	template_name = "book_detail.html"

	def post(self, request, *args, **kwargs):
		rating = request.POST.get('rating', None)
		book_id = request.POST.get('book_id', None)
		book_model = Book.objects.get(pk=book_id)
		context_dict = {}
		
		book_rating = None
		if request.user.is_authenticated():
			
			user_rating = Rating.objects.filter(book=book_model,user_id=request.user).only('id','rating')
			
			
			if user_rating:
				rating_model = Rating.objects.get(book=book_model, user_id=request.user)
				rating_model.rating = rating
				rating_model.save()
				user_rating = Rating.objects.filter(book=book_model,user_id=request.user).only('id','rating')
				book_rating = user_rating
			else:	
				
				rating_model = Rating(book=book_model, user_id=request.user, rating=rating)
				rating_model.save()
				user_rating = Rating.objects.filter(book=book_model,user_id=request.user).only('id','rating')
				book_rating = user_rating

			context_dict['success'] = 1
			context_dict['book_rating'] = serializers.serialize('json',book_rating)
		else:
			context_dict['success'] = 0

		return HttpResponse(JsonResponse(context_dict))


'''
	
	Twitter API
	-----------
	Consumer Key (API Key)	SkqreObweTWiKVI1X0qjJ7a6B
	Consumer Secret (API Secret)	wIXEyi6mxitwlnyP9GJK3mzpIkr9QL6q5OLXXq4dBtS2iFIbP4

	Access Token	884317426711543810-TnQVyXM3d8y7kdiPXo32jtVKmXdXcwD
	Access Token Secret	ztc0WfhtV4BDAUIVWWXgw2M7XXC5f0F7vC4e3mln3Olah


'''


