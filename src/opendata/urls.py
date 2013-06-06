from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
admin.autodiscover()

urlpatterns = patterns("",
    url(r"^admin/", include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
    
    url(r"^$", "opendata_vorschlag.views.basic_redirect"),
    )

urlpatterns += i18n_patterns("",
    url(r"^$", "opendata_vorschlag.views.basic_redirect"),
    
    url(r"^request-dataset/$", "opendata_vorschlag.views.sende_vorschlag", name="sende_vorschlag"),
    url(r"^requested-datasets/$", "opendata_vorschlag.views.liste_vorschlaege", name="liste_vorschlaege"),
    url(r"^requested-dataset/(?P<vorschlag_id>[0-9]+)/$", "opendata_vorschlag.views.details_vorschlag", name="details_vorschlag"),
)
handler403 = "opendata_vorschlag.views.forbidden_error"
handler404 = "opendata_vorschlag.views.not_found_error"
handler500 = "opendata_vorschlag.views.server_error"
