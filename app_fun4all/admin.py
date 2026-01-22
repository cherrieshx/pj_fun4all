from django.contrib import admin
from django.shortcuts import render

# Register your models here.asdasd
from .models import Location, Evento, Prenotazione, DataFittizia

class EventoAdmin(admin.ModelAdmin):
    exclude = ('data_corrente',)

class PrenotazioneAdmin(admin.ModelAdmin):
    exclude = ('data_corrente',)

class LocationAdmin(admin.ModelAdmin):
    exclude = ('data_corrente',)

class DataFittiziaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False  # Disabilita l'aggiunta di nuove istanze

    def changelist_view(self, request, extra_context=None):
        obj = DataFittizia.load()  # prende sempre il record unico
        return self.change_view(request, str(obj.pk))

admin.site.register(DataFittizia, DataFittiziaAdmin)
# @admin.register(DataFittizia)
# class DataFittiziaAdmin(admin.ModelAdmin):
#     list_display = ('data_corrente',)

admin.site.register(Location,LocationAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Prenotazione, PrenotazioneAdmin)


# @admin.register(DataFittizia)
# class DataFittiziaAdmin(admin.ModelAdmin):
#     list_display = ('data_corrente',)


