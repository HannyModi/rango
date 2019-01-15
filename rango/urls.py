from django.conf.urls import url 
from django.conf import settings
from django.conf.urls.static import static
from rango import views
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about/$',views.about, name='about'),
    url(r'^add_category/$',views.add_category, name='add_category'),
    url(r'^(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page, name='add_page'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.show_category,name='show_category'),    
   
] 