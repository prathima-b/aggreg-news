from django import forms
from .models import Article
class Post_article(forms.ModelForm):
	class Meta:
		model=Article
		fields=('title','image_url','blog_url')