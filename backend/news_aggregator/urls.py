from .import views
from django.urls import path
urlpatterns=[
    path('',views.homepage,name='homepage'),
    path('new_entry/',views.post_article,name='post_article'),
    path('search/',views.search,name='search')
]
