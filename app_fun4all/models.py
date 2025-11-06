from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone

def valida_data_2025(value):
    if not (date(2025, 1, 1) <= value <= date(2025, 12, 31)):
        raise ValidationError("La data deve essere compresa nell'anno solare 2025.")
    
# Create your models here.

class Location(models.Model):
    nome = models.CharField(max_length=50)
    proprietario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    luogo = models.CharField(max_length=100)
    capienza = models.PositiveIntegerField()
    costo = models.PositiveIntegerField()
    data_appertura = models.DateField(validators=[valida_data_2025])
    data_chiusura = models.DateField(validators=[valida_data_2025])

    # Definizione dello stato della location
    Stato =[
        ('A', 'Attivo'),
        ('I', 'Inattivo'),
    ]
    stato = models.CharField(max_length=1, choices=Stato, default='A')
    class Meta:
        verbose_name_plural = 'Locations'
        ordering = ['nome']

    def clean(self):
        if self.data_chiusura < self.data_appertura:
            raise ValidationError("La data di chiusura deve essere successiva alla data di apertura.")
        
    def IsAvailable(self, data):
        return self.data_appertura <= data <= self.data_chiusura and self.stato == 'A'
    
    def __str__(self):
        return f"{self.nome} - {self.luogo} ({self.capienza} posti)"
  
    
class Evento(models.Model):
    nome = models.CharField(max_length=80)
    descrizione = models.CharField(max_length=300 ,help_text='Descrizione dell\'evento')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True)
    data_evento = models.DateField(unique=True, validators=[valida_data_2025])
    organizzatore = models.ForeignKey('auth.User',on_delete=models.SET_NULL, null= True)
    costo = models.PositiveIntegerField('Costo unitario (€)')

    Stato = [
        ('A', 'Attivo'),
        ('C', 'Cancellato dall\'organizzatore'),
        ('S', 'Sospeso per indisponibilità della location'),
        ('F', 'Scaduto e precedente attivo'),
        ('D', 'Scaduto e precededente cancellato'),
    ]

    stato = models.CharField(max_length=1, choices=Stato, default='A')

    class Meta:
        verbose_name_plural = 'Eventi'
        ordering = ['data_evento']

    def clean(self):
        if self.location and not self.location.Is(self.data_evento):
            raise ValidationError("La location non è disponibile o attiva in quella data.")

        eventi_stesso_giorno = Evento.objects.filter(
            location=self.location,
            data_evento=self.data_evento
        ).exclude(pk=self.pk)

        if eventi_stesso_giorno.exists():
            raise ValidationError("Esiste già un evento in questa location in questa data.")

    def __str__(self):
        return f"{self.nome} ({self.data_evento}) - {self.location.nome}"
    

class Prenotazione(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL,null=True)
    utente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    numero_biglietti = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    ID = models.AutoField(primary_key=True)

    Stato = [
        ('A', 'Attiva'),
        ('U', 'Cancellata dall\'utente'),
        ('C', 'Cancellata come conseguenza della cancellazione dell\'evento'),
        ('B', 'Scaduta e precedentemente cancellata dall\'utente'),
        ('S','In sospeso poiché l\'evento è in sospeso'),
        ('V', 'Scaduta e precedentemente cancellata da utente'),
        ('D', 'Scaduta e precedentemente cancellata causa evento cancellato'),
        ('J','Scaduta essendo in sopseso')
    ]
    stato = models.CharField(max_length=1, choices=Stato, default='A')

    class Meta:
        
        verbose_name_plural = 'Prenotazioni'
        ordering = ['-data']

    def clean(self):
        if not self.evento or not self.numero_biglietti:
            return

        # Somma prenotazioni esistenti attive o sospese
        prenotazioni = Prenotazione.objects.filter(
            evento=self.evento,
            stato__in=['A', 'S']
        ).exclude(pk=self.pk)

        totale = sum(p.numero_biglietti for p in prenotazioni)
        totale += self.numero_biglietti

        if totale > self.evento.location.capienza:
            raise ValidationError("Capacità massima della location superata.")
    
    def __str__(self):
        return f"Prenotazione {self.ID} - Evento: {self.evento.nome} - Utente: {self.utente.username} - Biglietti: {self.numero_biglietti}"

class DataFittizia(models.Model):
    data_fittizia = models.DateField(validators=[valida_data_2025])

    def __str__(self):
        return f"Data Fittizia: {self.data_corrente}"

    class Meta:
        verbose_name_plural = 'Data Fittizia'
        
    




