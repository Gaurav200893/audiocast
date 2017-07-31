from django import forms
from .models import Review
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class ReviewForm(forms.ModelForm):
	"""
		Review Model Form

	"""
	class Meta:
		model = Review
		labels = {
			'review_text': 'Tell us what you learned from this book',
			'audio_review': 'Upload your audio review (optional)'
		}
		fields = ['review_text', 'audio_review']
	

