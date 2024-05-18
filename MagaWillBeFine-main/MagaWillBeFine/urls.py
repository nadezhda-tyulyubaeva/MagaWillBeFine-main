from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from Diplom import views
from Diplom.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', user_profile, name='profile'),
    path('', views.index, name='home'),
    path('', include('django.contrib.auth.urls')),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', views.LoginUser, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('base', views.base),
    path('events1/', EventView.as_view(), name='posts'),
    path('news/', NewView.as_view(), name='news'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('invitation/<int:pk>/', InvitationView.as_view(), name='invitation'),
    path('create_event/', create_event, name='create_event'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
