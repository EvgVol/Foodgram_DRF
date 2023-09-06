from django.contrib import admin
from django.urls import include, path
from django.views.defaults import (bad_request,
                                   permission_denied,
                                   page_not_found,
                                   server_error)


handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls',)),
]
