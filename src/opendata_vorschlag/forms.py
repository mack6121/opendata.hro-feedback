from django import forms
from opendata_vorschlag.models import Vorschlag
from captcha.fields import ReCaptchaField 
from django.utils.translation import ugettext_lazy as _



class VorschlagForm(forms.ModelForm):
    captcha = ReCaptchaField(label=_("CAPTCHA"))
    class Meta:
        model = Vorschlag
        exclude = ("freigegeben",)