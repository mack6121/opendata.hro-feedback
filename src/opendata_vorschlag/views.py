from django.template import loader
from django.template.context import RequestContext
from django.http import HttpResponse, Http404
from opendata_vorschlag.forms import VorschlagForm
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.utils.translation import activate
from opendata_vorschlag.models import Vorschlag, VorschlagStatus,\
    DEFAULT_VORSCHLAG_STATUS, VORSCHLAG_STATUS
from opendata_vorschlag.helpers import get_bezeichnung_auswahl, get_status_bild,\
    sende_vorschlag_email
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect
from django.conf import settings
from urlparse import urljoin



@csrf_protect
def sende_vorschlag(request):
    
    form_vorschlag = VorschlagForm(request.POST or None)
    
    if request.method == "POST":
        if form_vorschlag.is_valid():
            vorschlag = Vorschlag.objects.create(
                email = form_vorschlag.cleaned_data["email"],
                betreff = form_vorschlag.cleaned_data["betreff"],
                beschreibung = form_vorschlag.cleaned_data["beschreibung"],
                freigegeben = False,
            )
            
            VorschlagStatus.objects.create(
                vorschlag = vorschlag,
                # Dieser String wird bewusst nicht zur Uebersetzung angeboten, da die Anfragen vor allem
                # in Deutscher Sprache sein werden und es ansonsten zu einer inkonsistenten Umsetzung
                # kommen kann
                details = "Eine neue Datensatzanfrage wurde erstellt.",
                status = DEFAULT_VORSCHLAG_STATUS,
                mitgeteilt = True,
            )
            
            sende_vorschlag_email(vorschlag.email, vorschlag.betreff, vorschlag.beschreibung, vorschlag.id)
            
            t = loader.get_template("opendata_vorschlag/sende_vorschlag_erfolgreich.html")
            
            sprache = request.LANGUAGE_CODE
            activate("en")
            url_en = reverse("sende_vorschlag")
            activate("de")
            url_de = reverse("sende_vorschlag")
            activate(sprache)
            
            c = RequestContext(request, {
                    "sprache": sprache,
                    "url_liste_vorschlaege": reverse("liste_vorschlaege"),
                    "url_en": url_en,
                    "url_de": url_de,
            })
            return HttpResponse(t.render(c))
    
    t = loader.get_template("opendata_vorschlag/sende_vorschlag.html")
    
    sprache = request.LANGUAGE_CODE
    activate("en")
    url_en = reverse("sende_vorschlag")
    activate("de")
    url_de = reverse("sende_vorschlag")
    activate(sprache)
    
    c = RequestContext(request, {
            "form_vorschlag": form_vorschlag,
            "sprache": sprache,
            "url_en": url_en,
            "url_de": url_de, 
    })
    return HttpResponse(t.render(c))



def liste_vorschlaege(request):
    
    offset = 0
    page = 1
    
    if request.GET.has_key("page"):
        tmp = request.GET["page"]
        if tmp and int(tmp) >= 1:
            page = int(request.GET["page"])
            offset = (page-1)*10
    
    vorschlaege = Vorschlag.objects.filter(freigegeben=True).order_by("-erstellt_datum")
    daten = []
    for v in vorschlaege[offset:offset+10]:
        status = list(v.vorschlagstatus_set.all()[:1])
        if status:
            s = status[0]
            daten.append({"vorschlag": v, "status": get_bezeichnung_auswahl(VORSCHLAG_STATUS,s.status), "statusbild": get_status_bild(s.status)})
        else:
            daten.append({"vorschlag": v, "status": _("Unknown")})
    
    num_pages = len(vorschlaege) / 10 + (1 if len(vorschlaege) % 10 else 0)
    
    pagination = ""
    if num_pages > 1:
        pagination = "<div class='pagination'><ul>"
        if page > 1:
            pagination += "<li><a href=\"?page=%d\">&laquo; zur&uuml;ck</a></li><li><a href=\"?page=1\">1</a>" % (page-1,)
        
        if page-3 > 1:
            pagination += "<li class=\"disabled\"><a href=\"#\">...</a></li>"
        
        for i in [2,1]:
            if page-i > 1:
                pagination += "<li><a href=\"?page=%d\">%d</a></li>" % (page-i, page-i,)
        
        pagination += "<li class=\"active\"><a href=\"?page=%d\">%d</a></li>" % (page, page,)
        
        for i in [1,2]:
            if page+i < num_pages:
                pagination += "<li><a href=\"?page=%d\">%d</a></li>" % (page+i, page+i,)
        
        if page+3 < num_pages:
            pagination += "<li class=\"disabled\"><a href=\"#\">...</a></li>"
        
        if page < num_pages:
            pagination += "<li><a href=\"?page=%d\">%d</a><li><a href=\"?page=%d\">vor &raquo;</a></li>" % (num_pages, num_pages, page+1,)
        
        pagination += "</ul></div>"
    
    
    t = loader.get_template("opendata_vorschlag/liste_vorschlaege.html")
    
    sprache = request.LANGUAGE_CODE
    activate("en")
    url_en = reverse("liste_vorschlaege") + "?page=%d" % (page,)
    activate("de")
    url_de = reverse("liste_vorschlaege") + "?page=%d" % (page,)
    activate(sprache)
    
    c = RequestContext(request, {
            "daten": daten,
            "url_sende_vorschlag": reverse("sende_vorschlag"),
            "sprache": sprache,
            "url_en": url_en,
            "url_de": url_de,
            "pagination": pagination,
    })
    return HttpResponse(t.render(c))



def details_vorschlag(request, vorschlag_id):
    
    try:
        vorschlag = Vorschlag.objects.get(pk=vorschlag_id, freigegeben=True)
    except Vorschlag.DoesNotExist:
        raise Http404
    
    status = VorschlagStatus.objects.filter(vorschlag=vorschlag).order_by("-erstellt_datum")
    
    status_daten = []
    for s in status:
        status_daten.append({"daten":s, "titel": get_bezeichnung_auswahl(VORSCHLAG_STATUS, s.status),"bild": get_status_bild(s.status)})
    
    t = loader.get_template("opendata_vorschlag/details_vorschlag.html")
    
    sprache = request.LANGUAGE_CODE
    activate("en")
    url_en = reverse("details_vorschlag", args=(vorschlag_id,))
    activate("de")
    url_de = reverse("details_vorschlag", args=(vorschlag_id,))
    activate(sprache)
    
    c = RequestContext(request, {
            "vorschlag": vorschlag,
            "status_daten": status_daten,
            "url_sende_vorschlag": reverse("sende_vorschlag"),
            "sprache": sprache,
            "url_en": url_en,
            "url_de": url_de,
    })
    return HttpResponse(t.render(c))



def basic_redirect(request):
    return redirect(urljoin(getattr(settings, "BASE_URL"), "/feedback/"+request.LANGUAGE_CODE+"/requested-datasets/"))



def forbidden_error(request):
    return redirect("http://geo.sv.rostock.de/403.html")

def not_found_error(request):
    return redirect("http://geo.sv.rostock.de/404.html")

def server_error(request):
    return redirect("http://geo.sv.rostock.de/500.html")
