from django.db import models
from django.core.exceptions import ValidationError
from datetime import date
from django.contrib.auth.models import User
from django.utils import timezone

def valida_data_2025(value):
    if not (date(2025, 1, 1) <= value <= date(2025, 12, 31)):
        raise ValidationError("La data deve essere compresa nell'anno solare 2025.")
    

class DataFittizia(models.Model):
    data_fittizia = models.DateField(validators=[valida_data_2025])
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    

    def __str__(self):
        return f"Data Fittizia: {self.data_fittizia}"
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1, defaults={'data_fittizia': '2026-01-22'})
        return obj
    
    def save(self, *args, **kwargs):
        print("Sono in data fittizia save")
        self.pk = 1  # Forza l'ID a 1 per garantire l'unicità
        if not self.pk and DataFittizia.objects.exists():
            raise ValidationError("Può esistere solo una data nel sistema!")
        
        
        for evento in self.eventi.all():
            evento.update_status()
            evento.save()  # salva gli eventuali cambiamenti dello stato
            for prenotazione in evento.prenotazioni.all():
                print(f"for evento.prenotazione in datafittizia {prenotazione.evento.nome}")
                prenotazione.update_status()
                prenotazione.save()  # salva gli eventuali cambiamenti dello stato
        super().save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'Data Fittizia'
        permissions = (('can_manage_datefittizia', 'Can manage Data Fittizia'),)
      
class Location(models.Model):
    nome = models.CharField(max_length=50)
    proprietario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='locations' )
    luogo = models.CharField(max_length=100)
    capienza = models.PositiveIntegerField()
    costo = models.PositiveIntegerField()
    data_apertura = models.DateField(validators=[valida_data_2025])
    data_chiusura = models.DateField(validators=[valida_data_2025])
    data_corrente = models.ForeignKey(DataFittizia, on_delete=models.PROTECT, null=True, blank=True, related_name='locations')

    # Definizione dello stato della location
    Stato =[
        ('A', 'Attivo'),
        ('I', 'Inattivo'),
    ]
    stato = models.CharField(max_length=1, choices=Stato, default='A') #choices genera get_stato_display() che restituisce la descrizione dello stato
    class Meta:
        verbose_name_plural = 'Locations'
        ordering = ['nome']
        permissions = (('can_manage_location', 'Can manage location'),)

    def clean(self):
        if self.data_apertura and self.data_chiusura:
            if self.data_chiusura < self.data_apertura:
                raise ValidationError("La data di chiusura deve essere successiva alla data di apertura.")
        
    def IsAvailable(self,evento):
        return (self.data_apertura <= evento.data_evento<= self.data_chiusura) and (self.stato == 'A')
    
    def __str__(self):
        return f"{self.nome} - {self.luogo} ({self.capienza} posti)"
    
    def save(self, *args, **kwargs):
        if not self.data_corrente:
           self.data_corrente = DataFittizia.objects.first()
        self.clean()
        super().save(*args, **kwargs) #esegue tutto quello che fa normalmente Django quando salva un modello nel database
        print("Sono in location save")
        for evento in self.eventi.all():
            print(f"AAAAAAAAAAAAAAAAA") 
            evento.update_status()
            evento.save()  # salva gli eventuali cambiamenti dello stato
       
        # aggiorna gli eventi collegati quando cambia la location
        
            
    
class Evento(models.Model):
    nome = models.CharField(max_length=80)
    descrizione = models.CharField(max_length=300 ,help_text='Descrizione dell\'evento')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null = True, related_name='eventi')
    data_evento = models.DateField(unique=True, validators=[valida_data_2025])
    organizzatore = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='eventi' )
    costo = models.PositiveIntegerField('Costo unitario (€)')
    data_corrente = models.ForeignKey(DataFittizia, on_delete=models.PROTECT, blank=True, null = True,related_name='eventi')

    Stato = [
        ('A', 'Attivo'),
        ('C', 'Cancellato dall\'organizzatore'),
        ('S', 'Sospeso per indisponibilità della location'),
        ('F', 'Scaduto e precedente attivo'),
        ('D', 'Scaduto e precededente cancellato'),
    ]

    stato = models.CharField(max_length=1, choices=Stato, default='A')
    class Meta:
        ordering = ['data_evento']
        verbose_name_plural = 'Eventi'
        permissions = (('can_manage_evento', 'Can manage evento'),)

    def clean(self):
        if self.location and self.location.stato == 'I':
            print("La location è inagibile a tempo indeterminato ed a prescindere dalla data di apertura e chiusura.")
            return
        eventi_stesso_giorno = Evento.objects.filter(
            location=self.location,
            data_evento=self.data_evento
        ).exclude(pk=self.pk)

        if eventi_stesso_giorno.exists():
            raise ValidationError("Esiste già un evento in questa location in questa data.")

    def __str__(self):
        return f"{self.nome} ({self.data_evento}) - {self.location.nome}"

    def update_status(self):
        if self.data_corrente.data_fittizia is None:
            print("Data corrente non definita")
            return
        if (self.location.stato == 'I' or (not self.location.IsAvailable(self))) and (self.stato == 'A'):
            self.stato = 'S'  # Sospeso per indisponibilità della location
        if self.data_corrente.data_fittizia > self.data_evento:
            if self.stato == 'A':
                self.stato = 'F'  # Scaduto e precedente attivo
            elif self.stato == 'C':
                self.stato = 'D'  # Scaduto e precededente cancellato
        elif self.data_corrente.data_fittizia < self.data_evento:
            if self.stato == 'F':
                self.stato = 'A'  # Riattiva l'evento se era scaduto e precedente attivo
            elif self.stato == 'D':
                self.stato = 'C'  # Riattiva l'evento se era scaduto e precedente cancellato
            
    
    def save(self, *args, **kwargs):
        if not self.data_corrente:
            self.data_corrente = DataFittizia.objects.first()
        self.clean()
        super().save(*args, **kwargs)
        for prenotazione in self.prenotazioni.all():
            print(f"for   DI EVENTO SELF.prenotazione in evento {prenotazione.evento.nome}")
            prenotazione.update_status()
            prenotazione.save()
            print(f"{prenotazione.stato}")  # salva gli eventuali cambiamenti dello stato
        # self.update_status(self.data_corrente)
        
    
    @property
    def biglietti_venduti(self):
        return sum(b.numero_biglietti for b in self.prenotazioni.filter(stato='A'))

    @property
    def bilancio_economico(self):
        return self.biglietti_venduti * self.costo - self.location.costo

    @property
    def se_10_giorni_prima(self):
        return (self.data_evento - self.data_corrente.data_fittizia).days >= 10



class Prenotazione(models.Model):
    evento = models.ForeignKey(Evento, on_delete=models.SET_NULL,null=True, related_name='prenotazioni')
    utente = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='prenotazioni')
    numero_biglietti = models.PositiveIntegerField()
    data = models.DateTimeField(auto_now_add=True)
    ID = models.AutoField(primary_key=True)
    data_corrente = models.ForeignKey(DataFittizia, on_delete=models.PROTECT,null = True, blank = True, related_name='prenotazioni')

    Stato = [
        ('A', 'Attiva'),
        ('U', 'Cancellata dall\'utente'),
        ('C', 'Cancellata come conseguenza della cancellazione dell\'evento'),
        ('B', 'Scaduta e precedentemente attiva'),
        ('S', 'In sospeso poiché l\'evento è in sospeso'),
        ('V', 'Scaduta e precedentemente cancellata da utente'),
        ('D', 'Scaduta e precedentemente cancellata causa evento cancellato'),
        ('J', 'Scaduta essendo in sospeso')
    ]
    stato = models.CharField(max_length=1, choices=Stato, default='A')
  
    class Meta:
        verbose_name_plural = 'Prenotazioni'
        ordering = ['-data']
        permissions = (('can_manage_prenotazione', 'Can manage prenotazione'),)

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

    def update_status(self):
        print(".........................")
        if not self.evento:
            return
        print(f"PRIMA Stato prenotazione: {self.stato}")
        if self.evento.stato == 'C' :
            self.stato = 'C'  # Cancellata come conseguenza della cancellazione dell'evento
        elif self.evento.stato == 'S' :
            self.stato = 'S'  # In sospeso poiché l'evento è in sospeso
        elif self.evento.stato == 'A' and self.stato in ['C','S']:
            self.stato = 'A'  # Riattiva la prenotazione se l'evento è attivo
        elif self.evento.stato == 'F':
            self.stato = 'B'  # Scaduta e precedentemente attiva
        elif self.evento.stato == 'D':
            self.stato = 'D'  # Scaduta e precedentemente cancellata causa evento cancellato
        if self.data_corrente.data_fittizia > self.evento.data_evento:
            if self.stato == 'A':
                self.stato = 'B'  # Scaduta e precedentemente attiva
                print("Scaduta prenotazione da A a B")
            elif self.stato == 'U':
                self.stato = 'V'  # Scaduta e precedentemente cancellata da utente
            elif self.stato == 'C':
                self.stato = 'D'  # Scaduta e precedentemente cancellata causa evento cancellato    
            elif self.stato == 'S':
                self.stato = 'J'  # Scaduta essendo in sospeso
        if self.data_corrente.data_fittizia < self.evento.data_evento:
            print("Data corrente minore della data evento")
            if self.stato == 'B':
                self.stato = 'A'  # Riattiva la prenotazione se l'evento è attivo e la data corrente è prima dell'evento
                print("Riattivata prenotazione da B ad A")
            elif self.stato =='V':
                self.stato = 'U'  # Riattiva la prenotazione se l'evento è attivo e la data corrente è prima dell'evento
            elif self.stato == 'D':
                self.stato = 'C'  # Riattiva la prenotazione se l'evento è attivo e la data corrente è prima dell'evento
            elif self.stato == 'J':
                self.stato = 'S'  # Riattiva la prenotazione se l'evento è attivo e la data corrente è prima dell'evento        
        print(f"DOPO Stato prenotazione: {self.stato}")
        print(".........................")
        
    def save(self, *args, **kwargs):
        if not self.data_corrente:
            self.data_corrente = DataFittizia.objects.first()
        self.clean()
        # self.update_status(self.data_corrente)
        super().save(*args, **kwargs)  
            
    @property
    def se_5_giorni_prima(self):
        return (self.evento.data_evento - self.data_corrente.data_fittizia).days >= 5

    




