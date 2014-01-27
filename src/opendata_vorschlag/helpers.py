from django.template.loader import get_template
from django.core.mail.message import EmailMessage, BadHeaderError
from smtplib import SMTPException
from django.template.context import Context
from django.conf import settings
from urlparse import urljoin
from django.core.urlresolvers import reverse
from opendata_vorschlag.models import VORSCHLAG_STATUS_NEU,\
    VORSCHLAG_STATUS_AKZEPTIERT, VORSCHLAG_STATUS_REALISIERT,\
    VORSCHLAG_STATUS_NICHT_REALISIERBAR



def get_status_bild(status):
    if status == VORSCHLAG_STATUS_NEU:
        return "idea-red-22px.png"
    elif status == VORSCHLAG_STATUS_AKZEPTIERT:
        return "idea-yellow-22px.png"
    elif status == VORSCHLAG_STATUS_REALISIERT:
        return "idea-green-22px.png"
    elif status == VORSCHLAG_STATUS_NICHT_REALISIERBAR:
        return "idea-black-22px.png"
    else:
        return None



def sende_vorschlag_email(vorschlag):
    try:
        email_text = get_template("emails/opendata_vorschlag/sende_vorschlag.txt")
        daten = Context({
                         "betreff": vorschlag.betreff,
                         "beschreibung": vorschlag.beschreibung,
                         "url": urljoin(getattr(settings, "BASE_URL"), reverse("details_vorschlag", args=(vorschlag.id,)))
                         })
        email_nachricht = email_text.render(daten)
        betreff = "OpenData.HRO: Neue Datensatzanfrage"
        email = EmailMessage(betreff, email_nachricht, "opendata.hro@rostock.de", [vorschlag.email], ["opendata.hro@rostock.de"])
        email.send()
    except SMTPException:
        return False
    except BadHeaderError:
        return False
    
    return True
