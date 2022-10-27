from dataclasses import field
from .models import Review
from django import forms

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('title','movie_title','content','grade','image',)