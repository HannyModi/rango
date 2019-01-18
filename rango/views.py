from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm, update_pageForm, update_category as update_cat
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
# Create your views here.

def get_server_side_cookie(request,cookie,default_val=None):
    val=request.session.get(cookie)
    if not val:
        val=default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request,'visits', '1'))
    last_visit_cookie = get_server_side_cookie(request,'last_visit', str(datetime.now()))
    last_visited_time = datetime.strptime(
        last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')        
    if(datetime.now() - last_visited_time).seconds/3600 >= 1:
        visits = visits+1
        request.session['last_visit']= str(datetime.now())
    else:
        visits = visits
        request.session['last_visit']= last_visit_cookie
    request.session['visits']= visits
    


def index(request):
    content_dict = {}
    content_dict['dynamicmessage'] = "Good to see you."
    category_list = Category.objects.order_by('-like')[:5]
    content_dict['categories'] = category_list
    page_list = Page.objects.order_by('-views')[:5]
    content_dict['pages'] = page_list
    visitor_cookie_handler(request)
    content_dict['visits'] = request.session['visits']
    return render(request, 'rango_t/index.html', content_dict)


def about(request):
    content_dict = {"MyName": "Hanny."}
    visitor_cookie_handler(request)
    content_dict['visits']=request.session['visits']
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


@login_required
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


@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return show_category(request, category_name_slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango_t/add_page.html', context_dict)


def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango_t/register.html', {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print("Invalid login details: {0}, {1}".format(username, password))
            return HttpResponse("Invalid login credentials provided.")
    else:
        return render(request, 'rango_t/login.html', {})


@login_required
def restricted(request):
    return render(request, 'rango_t/restricted.html', {})


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


@login_required
def update_category(request, slug):
    category = Category.objects.get(slug=slug)
    form = update_cat(
        {'name': category.name, 'views': category.views, 'likes': category.like})
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.like = request.POST.get('likes')
        category.views = request.POST.get('views')
        category.save()
        form = update_cat(request.POST, category)
        return index(request)
    return render(request, 'rango_t/edit_category.html', {'form': form})


@login_required
def update_page(request, tid):
    page = Page.objects.get(id=tid)
    form = update_pageForm(
        {'title': page.title, 'url': page.url, 'views': page.views})
    if request.method == 'POST':
        page.title = request.POST.get('title')
        page.url = request.POST.get('url')
        page.views = request.POST.get('views')
        page.save()
        form = update_pageForm(request.POST, page)
        return index(request)
    return render(request, 'rango_t/edit_page.html', {'form': form})
