from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', 'newsletter.views.home', name='home'),
    url(r'^signup/(\d+)/$', 'newsletter.views.signup', name='signup'),
	url(r'^contact/$', 'newsletter.views.contact', name='contact'),
	url(r'^about/$', 'test_project.views.about', name='about'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('registration.backends.default.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
