from django.db import models
from django.utils.translation import ugettext_lazy as _



# Bei Aenderungen das sende_statusaenderungen Skript entsprechend anpassen
VORSCHLAG_STATUS = (
    (1, _("New")),
    (2, _("Accepted")),
    (3, _("Realized")),
    (4, _("Not realizable"))
)
DEFAULT_VORSCHLAG_STATUS = 1



class Vorschlag(models.Model):
    class Meta:
        verbose_name = _("Dataset request")
        verbose_name_plural = _("Dataset requests")
        ordering = ["-erstellt_datum"]
    
    email = models.EmailField(max_length=128,verbose_name=_("Email address"), help_text=_("Please note that this information will not be published but used for further queries."))
    betreff = models.CharField(max_length=64, verbose_name=_("Subject"), help_text=_("Which dataset would you like to be published as open data?"))
    beschreibung = models.TextField(max_length=4096,verbose_name=_("Description"), help_text=_("Please provide some details concerning your request, e.g. which information the dataset should provide."))
    freigegeben = models.BooleanField(default=False, verbose_name=_("Public"), help_text=_("Should this request be published?"))
    erstellt_datum = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return _("%(subject)s (E-mail address of the author: %(email)s)") % {"subject": self.betreff, "email": self.email,}



class VorschlagStatus(models.Model):
    class Meta:
        verbose_name = _("Dataset request status")
        verbose_name_plural = _("Dataset request status'")
        ordering = ["vorschlag", "-erstellt_datum"]
    
    vorschlag = models.ForeignKey(Vorschlag)
    details = models.TextField()
    status = models.PositiveSmallIntegerField(choices=VORSCHLAG_STATUS)
    mitgeteilt = models.BooleanField(default=False, editable=False)
    erstellt_datum = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return _("%(request)s: %(status)d") % {"request": self.vorschlag, "status": self.status,}
