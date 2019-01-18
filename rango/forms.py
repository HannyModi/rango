from django import forms
from rango.models import Category, Page,User_Profile
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=128, help_text="Please enter Category name")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)

class PageForm(forms.ModelForm):
    title = forms.CharField(
        max_length=128, help_text="Please enter the title of the page.")
    url = forms.URLField(
        max_length=200, help_text="Please enter the URL of the page.")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    # def clean(self):
    #     cleaned_data=self.cleaned_data
    #     url=cleaned_data.get('url')
    #     if url and not url.startswith('http://') and not url.startswith('https://'):
    #         url='http://' + url
    #         cleaned_data['url']=url
    #     return cleaned_data

    class Meta:
        model = Page
        fields=('title','url',)
        # exclude = ('category',)

class UserForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model=User
        fields=('username','email','password')

class UserProfileForm(forms.ModelForm):
    #something field
    class Meta:
        model=User_Profile
        fields=('website','picture')
        #fields:"__all__"

class update_category(forms.ModelForm):

    name = forms.CharField(max_length=128, help_text="Please enter Category name",initial='name')
    views = forms.IntegerField(help_text="Views",initial='views')
    likes = forms.IntegerField(initial='likes',help_text='Like')
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name','views','likes',)

class update_pageForm(forms.ModelForm):
   # pid=forms.IntegerField(widget=forms.HiddenInput(),required=False)
    title=forms.CharField(max_length=128, help_text="Page Title:",initial='title')
    views=forms.IntegerField(help_text="Views:",initial='views') 
    url=forms.URLField(help_text="Enter Url:",initial='url')
    class Meta:
        model=Page
        fields=('title','url','views',)

