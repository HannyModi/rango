from django.urls import path,re_path
from django.conf import settings
from django.conf.urls.static import static
from rango import views
urlpatterns = [
    re_path('^$', views.index, name='index'),
    re_path('search/$',views.search, name='search'),
    re_path('goto/(?P<pid>\d+)/$', views.track_url, name='goto'),
    re_path('^about/$',views.about, name='about'),
    re_path('^add_category/$',views.add_category, name='add_category'),    
    re_path('^(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page, name='add_page'),
    re_path('^category/(?P<category_name_slug>[\w\-]+)/',views.show_category,name='show_category'),
    re_path('^(?P<slug>[\w\-]+)/edit_category/',views.update_category, name='update_category'), 
    re_path('^(?P<tid>[\w\-]+)/edit_page/$',views.update_page, name='update_page'),    
    re_path('^register/$',views.register,name='register'),
    re_path('^login/$', views.user_login, name='login'),
    re_path('^restricted/', views.restricted, name='restricted'),
    re_path('^logout/$', views.user_logout, name='logout'),
    re_path('^Add_Details/$',views.register_details,name='register_details'),
    re_path('^View_Profile/(?P<username>[\w\-]+)/$',views.view_profile,name='view_profile'),
    re_path('^List_Profile/$',views.list_user,name='list_user'),

] 
