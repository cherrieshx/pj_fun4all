from django.contrib import admin
from django.shortcuts import render

# Register your models here.
from .models import Location, Evento, Prenotazione, DataFittizia


def index(request):
    n_eventi = Evento.objects.all().count()
    n_locations = Location.objects.all().count()
    n_prenotazioni = Prenotazione.objects.all().count()

    contesto = {
        'num_eventi': n_eventi,
        'num_locations': n_locations,
        'num_prenotazioni': n_prenotazioni,
    }
    return render(request, 'index.html', context= contesto)

class EventoAdmin(admin.ModelAdmin):
    exclude = ('data_corrente',)

class PrenotazioneAdmin(admin.ModelAdmin):
    exclude = ('data_corrente',)

class DataFittiziaAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        if DataFittizia.objects.exists():
            return False
        return True

# @admin.register(DataFittizia)
# class DataFittiziaAdmin(admin.ModelAdmin):
#     list_display = ('data_corrente',)

admin.site.register(Location)
admin.site.register(Evento, EventoAdmin)
admin.site.register(Prenotazione, PrenotazioneAdmin)
admin.site.register(DataFittizia,DataFittiziaAdmin)
