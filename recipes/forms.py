from django import forms
from recipes.models import Author, User


class Add_Author(forms.Form):
    name = forms.CharField(max_length=60)
    bio = forms.CharField(widget=forms.Textarea)


class Add_Recipe(forms.Form):
    title = forms.CharField(max_length=60)
    description = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)
    time_required = forms.IntegerField()
    author = forms.ModelChoiceField(queryset=Author.objects.all())


class SignupForm(forms.Form):
    name = forms.CharField(max_length=60)
    username = forms.CharField(max_length=50)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())


class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput())


class EditRecipe(forms.Form):
    """Travis Added"""
    title = forms.CharField(max_length=60)
    description = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)
    time_required = forms.IntegerField()
