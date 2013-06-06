from django.template.loader import get_template
from django.core.mail.message import EmailMessage, BadHeaderError
from smtplib import SMTPException
from django.template.context import Context
from django.conf import settings
from urlparse import urljoin
from django.core.urlresolvers import reverse



def get_bezeichnung_auswahl(auswahl, wert):
    for (w, n) in auswahl:
        if wert == w:
            return n
    
    return None



def get_status_bild(status):
    if status == 1:
        return "idea-red-22px.png"
    elif status == 2:
        return "idea-yellow-22px.png"
    elif status == 3:
        return "idea-green-22px.png"
    elif status == 4:
        return "idea-black-22px.png"
    else:
        return None



def sende_vorschlag_email(emailadresse, vorschlag_betreff, vorschlag_beschreibung, vorschlag_id):
    emails_fehler = False
    try:
        email_text = get_template("emails/opendata_vorschlag/sende_vorschlag.txt")
        daten = Context({
                         "betreff": vorschlag_betreff,
                         "beschreibung": vorschlag_beschreibung,
                         "url": urljoin(getattr(settings, "BASE_URL"),reverse("details_vorschlag", args=(vorschlag_id,)))
                         })
        email_nachricht = email_text.render(daten)
        betreff = "OpenData.HRO: Neue Datensatzanfrage"
        email = EmailMessage(betreff, email_nachricht, "opendata.hro@rostock.de", [emailadresse], ["opendata.hro@rostock.de"])
        email.send()
    except SMTPException:
        emails_fehler = True
    except BadHeaderError:
        emails_fehler = True
    
    return not emails_fehler
