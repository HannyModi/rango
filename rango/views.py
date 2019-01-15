from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm
from django.db import IntegrityError

# Create your views here.


def index(request):
    content_dict = {}
    content_dict['dynamicmessage'] = "Good to see you."
    category_list = Category.objects.order_by('-like')[:5]
    content_dict['categories'] = category_list
    page_list = Page.objects.order_by('-views')[:5]
    content_dict['pages'] = page_list
    return render(request, 'rango_t/index.html', context=content_dict)


def about(request):
    content_dict = {"MyName": "Hanny."}
    return render(request, 'rango_t/about.html', context=content_dict)


def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None
    return render(request, 'rango_t/category.html', context_dict)


def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            try:
                form.save(commit=True)
                return index(request)
            except IntegrityError:
                form.add_error(
                    "name", "Category with this Name already exists.")
                print(form.errors)
        else:
            print(form.errors)
    return render(request, 'rango_t/add_category.html', {'form': form})


def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            try:
                if category:
                    page = form.save(commit=False)
                    page.category = category
                    page.views = 0
                    page.save()
                return show_category(request, category_name_slug)
            except IntegrityError:
                form.add_error(
                    "name", "Category with this Name already exists.")
                print(form.errors)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango_t/add_page.html', context_dict)
