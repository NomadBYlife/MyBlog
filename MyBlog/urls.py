import debug_toolbar

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('social_django.urls', namespace='social')),
    path('', include('blog.urls')),
    path('__debug__/', include(debug_toolbar.urls)),

]
