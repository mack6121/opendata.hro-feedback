from django import forms
from opendata_vorschlag.models import Vorschlag
from captcha.fields import ReCaptchaField 
from django.utils.translation import ugettext_lazy as _



class VorschlagForm(forms.ModelForm):
    captcha = ReCaptchaField(label=_("CAPTCHA"))
    
    class Meta:
        model = Vorschlag
        exclude = ("freigegeben",)
    
    
    
    def clean_email(self):
        return self.cleaned_data.get("email", "").strip()
    
    def clean_betreff(self):
        return self.cleaned_data.get("betreff", "").strip()
    
    def clean_beschreibung(self):
        return self.cleaned_data.get("beschreibung", "").strip()
