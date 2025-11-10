from django.contrib import admin
from django.shortcuts import render

# Register your models here.asdasd
from .models import Location, Evento, Prenotazione, DataFittizia
from django.shortcuts import render
admin.site.register(Location)
admin.site.register(Evento)
admin.site.register(Prenotazione)
admin.site.register(DataFittizia)

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

# @admin.register(DataFittizia)ssssssssssaaaaaaaaaaaaa
# class DataFittiziaAdmin(admin.ModelAdmin):
#     list_display = ('data_corrente',)
