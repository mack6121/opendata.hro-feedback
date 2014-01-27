from django.http import Http404
from opendata_vorschlag.forms import VorschlagForm
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.utils.translation import activate
from opendata_vorschlag.models import Vorschlag, VorschlagStatus, \
    DEFAULT_VORSCHLAG_STATUS, VORSCHLAG_STATUS
from opendata_vorschlag.helpers import get_status_bild, \
    sende_vorschlag_email
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import redirect, render
from django.conf import settings
from urlparse import urljoin
import math



@csrf_protect
def sende_vorschlag(request):
    
    form_vorschlag = VorschlagForm(request.POST or None)
    
    if request.method == "POST":
        if form_vorschlag.is_valid():
            vorschlag = form_vorschlag.save(commit=False)
            vorschlag.freigegeben = False
            vorschlag.save()
            
            VorschlagStatus.objects.create(
                vorschlag=vorschlag,
                # Dieser String wird bewusst nicht zur Uebersetzung angeboten, da die Anfragen vor allem
                # in Deutscher Sprache sein werden und es ansonsten zu einer inkonsistenten Umsetzung
                # kommen kann
                details="Eine neue Datensatzanfrage wurde erstellt.",
                status=DEFAULT_VORSCHLAG_STATUS,
                mitgeteilt=True,
            )
            
            sende_vorschlag_email(vorschlag)
            
            sprache = request.LANGUAGE_CODE
            activate("en")
            url_en = reverse("sende_vorschlag")
            activate("de")
            url_de = reverse("sende_vorschlag")
            activate(sprache)
            
            template_daten = {
                    "sprache": sprache,
                    "url_liste_vorschlaege": reverse("liste_vorschlaege"),
                    "url_en": url_en,
                    "url_de": url_de,
            }
            return render(request, "opendata_vorschlag/sende_vorschlag_erfolgreich.html", template_daten)
    
    sprache = request.LANGUAGE_CODE
    activate("en")
    url_en = reverse("sende_vorschlag")
    activate("de")
    url_de = reverse("sende_vorschlag")
    activate(sprache)
    
    template_daten = {
            "form_vorschlag": form_vorschlag,
            "sprache": sprache,
            "url_en": url_en,
            "url_de": url_de,
    }
    return render(request, "opendata_vorschlag/sende_vorschlag.html", template_daten)



def liste_vorschlaege(request):
    
    seite = 1
    # Falls moeglich lies die anzuzeigende Seite aus dem GET-Parameter page
    # und berechnen den notwendigen Offset
    if request.GET.get("page", None):
        try:
            seite = int(request.GET["page"])
        except ValueError:
            seite = 1
        finally:
            seite = 1 if seite < 1 else seite
    
    offset = (seite - 1) * 10
    
    daten = []
    vorschlaege = Vorschlag.objects.filter(freigegeben=True).order_by("-erstellt_datum")
    
    seitenzahl = int(math.ceil(vorschlaege.count() / 10.0))
    
    # Wenn nicht genuegend Eintraege vorhanden sind, dann leite den Nutzer auf die letzte Seite
    if offset > 0 and vorschlaege.count() < offset + 10:
        return redirect(reverse("liste_vorschlaege") + "?page=%i" % (seitenzahl,))
    
    for v in vorschlaege[offset:offset + 10]:
        status = list(v.vorschlagstatus_set.all().order_by("-erstellt_datum")[:1])
        if status:
            s = status[0] 
            daten.append({"vorschlag": v, "status": dict(VORSCHLAG_STATUS).get(s.status, _("Unknown")), "statusbild": get_status_bild(s.status)})
        else:
            daten.append({"vorschlag": v, "status": _("Unknown")})
    
    sprache = request.LANGUAGE_CODE
    activate("en")
    url_en = reverse("liste_vorschlaege") + "?page=%d" % (seite,)
    activate("de")
    url_de = reverse("liste_vorschlaege") + "?page=%d" % (seite,)
    activate(sprache)
    
    template_daten = {
            "daten": daten,
            "url_sende_vorschlag": reverse("sende_vorschlag"),
            "sprache": sprache,
            "url_en": url_en,
            "url_de": url_de,
            "seite": seite,
            "seitenzahl": seitenzahl,
    }
    
    return render(request, "opendata_vorschlag/liste_vorschlaege.html", template_daten)



def details_vorschlag(request, vorschlag_id):
    
    try:
        vorschlag = Vorschlag.objects.get(pk=vorschlag_id, freigegeben=True)
    except Vorschlag.DoesNotExist:
        raise Http404
    
    status = VorschlagStatus.objects.filter(vorschlag=vorschlag).order_by("-erstellt_datum")
    
    status_daten = []
    for s in status:
        status_daten.append({"daten":s, "titel": dict(VORSCHLAG_STATUS).get(s.status, _("Unknown")), "bild": get_status_bild(s.status)})
    
    sprache = request.LANGUAGE_CODE
    activate("en")
    url_en = reverse("details_vorschlag", args=(vorschlag_id,))
    activate("de")
    url_de = reverse("details_vorschlag", args=(vorschlag_id,))
    activate(sprache)
    
    template_daten = {
            "vorschlag": vorschlag,
            "status_daten": status_daten,
            "url_sende_vorschlag": reverse("sende_vorschlag"),
            "sprache": sprache,
            "url_en": url_en,
            "url_de": url_de,
    }
    return render(request, "opendata_vorschlag/details_vorschlag.html", template_daten)



def basic_redirect(request):
    return redirect(urljoin(getattr(settings, "BASE_URL"), "/feedback/" + request.LANGUAGE_CODE + "/requested-datasets/"))



def forbidden_error(request):
    return redirect("http://geo.sv.rostock.de/403.html")

def not_found_error(request):
    return redirect("http://geo.sv.rostock.de/404.html")

def server_error(request):
    return redirect("http://geo.sv.rostock.de/500.html")
