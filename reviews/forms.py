from dataclasses import field
from .models import Review, Comment
from django import forms

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title','movie_title','content','grade','image',)

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)