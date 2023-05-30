from django import forms
from .models import Posts, Tag, Categorie
from ckeditor.widgets import CKEditorWidget


class TagsForm1(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'categories']

class CreateBlogForm(forms.ModelForm):
    categories = forms.ModelChoiceField(queryset=Categorie.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Posts
        exclude = ('created_at', 'user')
        widgets = {
            'author': forms.TextInput(attrs={'value': '', 'id':'author', 'type':'hidden'}),
            'mini_description': forms.Textarea(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail_image': forms.FileInput(),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'id': 'search-field'}),

        }

from django_select2.forms import Select2MultipleWidget

class PostsForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=Select2MultipleWidget
    )

    class Meta:
        model = Posts
        exclude = ('created_at', 'user')
        widgets = {
            'author': forms.TextInput(attrs={'value': '', 'id':'author', 'type':'hidden'}),
            'mini_description': forms.Textarea(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail_image': forms.FileInput(),
        }