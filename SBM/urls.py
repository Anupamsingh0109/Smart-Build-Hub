"""
URL configuration for SBM project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from mainapp import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
     path('',views.index,name='index'),
     path('service/',views.service,name='service'),
     path('project/',views.project,name='project'),
      path('about/',views.about,name='about'),
       path('contact/',views.contact,name='contact'),
          path('sign/',views.sign,name='sign'),
             path('signup/',views.signup,name='signup'),
       path('self/',views.self,name='self'),
        path('adminlogin/',views.adminlogin,name='adminlogin'),
        path('adminapp/',include('adminapp.adminappurls')),
        path('homeowner/',include('homeownerapp.hurls')),
        path('contractor/',include('contractorapp.curls')),
        
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)