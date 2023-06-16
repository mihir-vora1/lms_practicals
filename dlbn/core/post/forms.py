from django import forms
from .models import Posts, Categorie

class CreateBlogForm(forms.ModelForm):
    categories = forms.ModelChoiceField(queryset=Categorie.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    article_tags = forms.CharField(
        max_length=500,
        required=False,
        widget=forms.TextInput(
            attrs={'class': 'form-control tag-editor-hidden-src', 'id': 'hero-demo', 'onclick': 'convertToTagEditor()'})
    )

    class Meta:
        model = Posts
        exclude = ('created_at', 'user', 'tags')
        widgets = {
            'author': forms.TextInput(attrs={'value': '', 'id': 'author', 'type': 'hidden'}),
            'mini_description': forms.Textarea(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
            'thumbnail_image': forms.FileInput(),
        }
