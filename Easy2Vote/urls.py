"""
URL configuration for Easy2Vote project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from mainapp.views import *



urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignupPage, name='signup'),
    path('parent/',parent,name='parent'),
    path('contact/',ContactPage,name='contact'),
    path('login/',LoginPage,name='login'),
    path('about/',AboutPage,name='about'),
    path('services/',ServicesPage,name='services'),
    path('',HomePage,name='home'),
    path('logout/',LogoutPage,name='logout'),
    path('vote_success/',vote_successPage,name='vote_success'),
    path('elections_list/', elections_list, name='elections_list'),
    path('vote/<int:election_id>/', vote, name='vote'),
    path('results/<int:election_id>/', results, name='results'),
    path('check_results/', check_results, name='check_results'),
    path('submit-query/', submit_query, name='submit_query'),

    path('secure/', secure, name='secure'),
    path('data/', data, name='data'),
    path('realresult/', realresult, name='realresult'),
    path('support/', support, name='support'),
    path('friendly/', friendly, name='friendly'),
    path('fraud/', fraud, name='fraud'),
]
