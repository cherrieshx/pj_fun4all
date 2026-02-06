import datetime
from django import forms
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import DataFittizia,Location, Evento, Prenotazione



class ManageDataFittiziaForm(forms.ModelForm):
    class Meta:
        model = DataFittizia
        fields = ['data_fittizia']


class ManageLocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['nome', 'luogo', 'capienza','costo', 'data_apertura', 'data_chiusura', 
                  'stato']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'fino a 80 caratteri',
            }),
            'luogo': forms.TextInput(attrs={
                'placeholder': 'fino a 100 caratteri',
            }),
        }
        
class ManageEventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['nome','descrizione','location','data_evento','costo','stato']
        widgets = {
            'nome': forms.TextInput(attrs={
                'placeholder': 'fino a 80 caratteri',
            }),
            'descrizione': forms.Textarea(attrs={
                'class': 'descrizione',
                'placeholder': 'fino a 300 caratteri',     
            }),
        }

    def __init__(self, *args, **kwargs): #Selezionabile solo le locations non inattive alla data fittizia
        super().__init__(*args, **kwargs)
        self.fields['stato'].disabled = True  # disabilita la modifica
        dt = self.instance.data_evento
        loc = Location.objects.filter(stato='A')
        
        if dt:
            loc = loc.exclude(
                eventi__data_evento=dt,
                eventi__pk=self.instance.pk 
            )
        else:
            loc = loc.exclude(eventi__data_evento=dt)

        self.fields['location'].queryset = loc
  
class ChangeEventoLocationForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = ['location']

    def __init__(self, *args, **kwargs): #Selezionabile le locations attive disponibili alla data fittizia 
        super().__init__(*args, **kwargs)
        dt = self.instance.data_evento
        loc = Location.objects.filter(stato='A')
        
        if dt:
            loc = loc.exclude(
                eventi__data_evento=dt,
                eventi__pk=self.instance.pk 
            )
        else:
            loc = loc.exclude(eventi__data_evento=dt)

        self.fields['location'].queryset = loc


class ManagePrenotazioneForm(forms.ModelForm):
    class Meta:
        model = Prenotazione
        fields = ['evento', 'numero_biglietti']

    def __init__(self, *args, **kwargs): #Selezionabile solo gli aventi attivi alla data fittiza
        super().__init__(*args, **kwargs)
        dt =  DataFittizia.objects.get(pk=1).data_fittizia
        self.fields['evento'].queryset = Evento.objects.filter(stato='A', data_evento__gte=dt)

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email',
                  'username', 'password1', 'password2']
