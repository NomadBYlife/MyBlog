from django.conf.urls.static import static
from django.urls import path

from MyBlog import settings
from blog.views import *

urlpatterns = [
    path('', Blog_home.as_view(), name='home'),
    path('blogs/newblog', Blog_add.as_view(), name='add_blog'),
    path('blogs/', Blogs_all.as_view(), name='all_blogs'),
    path('blogs/<slug:slug>', Blog_show.as_view(), name='show_blog'),
    path('blogs/<slug:slug>/create', CommentShow.as_view(), name='add_comment'),
    path('blogers/', Bloger_all.as_view(), name='all_blogers'),
    path('blogers/<slug:slug>', BlogerView.as_view(), name='blogerview'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('register/', RegisterUser.as_view(), name='register'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
