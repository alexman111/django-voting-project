"""fair URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from voting import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('candidate/<int:pk>', views.CandidatePage.as_view(), name='candidate_page'),
    path('edit-page', views.CandidateCreateView.as_view(), name='edit_page'),
    path('update-page/<int:pk>', views.CandidateUpdateView.as_view(), name='update_page'),
    path('delete-page/<int:pk>', views.CandidateDeleteView.as_view(), name='delete_page'),
    path('login', views.UserLoginView.as_view(), name='login_page'),
    path('logout', views.UserLogoutView.as_view(), name='logout_page'),
    path('register', views.usersignup   , name='register_page'),
    path('vote_for_candidate', views.vote_for_candidate, name='vote_for_candidate'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
