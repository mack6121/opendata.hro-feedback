from django.contrib import admin
from opendata_vorschlag.models import Vorschlag, VorschlagStatus
from reversion import VersionAdmin
from django.utils.translation import ugettext_lazy as _



def gib_vorschlaege_frei(modeladmin, request, queryset):
    for vorschlag in queryset:
        vorschlag.freigegeben = True
        vorschlag.save()
gib_vorschlaege_frei.short_description = _("Publish request")



def verberge_vorschlaege(modeladmin, request, queryset):
    for vorschlag in queryset:
        vorschlag.freigegeben = False
        vorschlag.save()
verberge_vorschlaege.short_description = _("Unpublish request")



class VorschlagStatusInline(admin.StackedInline):
    model = VorschlagStatus



class VorschlagAdmin(VersionAdmin):
    list_display = ("betreff", "email", "freigegeben", "erstellt_datum")
    search_fields = ["betreff", "email", "beschreibung"]
    list_filter = ("erstellt_datum", "freigegeben")
    actions = [gib_vorschlaege_frei, verberge_vorschlaege, ]
    inlines = [ VorschlagStatusInline, ]
    
    def get_actions(self, request):
        actions = super(VorschlagAdmin, self).get_actions(request)
        if not self.has_delete_permission(request):
            del actions["delete_selected"]
        return actions

admin.site.register(Vorschlag, VorschlagAdmin)
