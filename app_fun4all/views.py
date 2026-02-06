from django.shortcuts import render
from .models import Evento, Location, Prenotazione, DataFittizia
from .forms import ManageDataFittiziaForm,ManageLocationForm, ChangeEventoLocationForm, ManageEventoForm, ManagePrenotazioneForm,ManagePrenotazioneForm,SignupForm
from django.views import generic
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import  Group
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse


def data_corrente(request): #FBV che restituisce la data fittizia 
    return { 'data_corrente': DataFittizia.objects.first() }


def resetlogin(request, next): #FBV che 

    request.session['num_visits'] = 0 # azzera il contatore visite
    request.session.modified = True # forza il salvataggio della sessione
    return HttpResponseRedirect(reverse('login') + "?next=" + next)# reindirizza alla pagina di login


class HomeListView(generic.ListView): #CBV della Home che mostra gli eventi attivi alla data fittizia

    model = Evento
    template_name = 'index.html'
    context_object_name = 'eventi_attivi'
    paginate_by = 3
   
    def get_queryset(self):
        return Evento.objects.filter(
                 stato ='A',
                ).order_by("data_evento","nome","location")

        
class LocationListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView): #CBV della lista delle location con i loro dati

    login_url = '/accounts/login/'
    model = Location
    paginate_by = 3
    permission_required = 'app_fun4all.can_manage_location'
    raise_exception = True

    def get_queryset(self): 
        if self.request.user.is_superuser or self.request.user.is_staff:
            all_locations = Location.objects.all()
        else:
            all_locations = Location.objects.filter(proprietario=self.request.user)
        return all_locations.order_by('nome') 


class EventoListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView): #CBV della lista degli eventi con i loro dati

    login_url = '/accounts/login/'
    model = Evento
    paginate_by = 3
    permission_required = 'app_fun4all.can_manage_evento'
    raise_exception = True

    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            all_eventi = Evento.objects.all()
        else:
            all_eventi = Evento.objects.filter(organizzatore=self.request.user)
        return all_eventi.order_by('data_evento','nome','location')


class PrenotazioneListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView): #CBV della lista delle prenotazioni con i loro dati        

    login_url = '/accounts/login/'
    permission_required = 'app_fun4all.can_manage_prenotazione'
    raise_exception = True
    model = Prenotazione
    paginate_by = 3

    
    def get_queryset(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            all_prenotazioni = Prenotazione.objects.all()
        else:
            all_prenotazioni = Prenotazione.objects.filter(fruitore=self.request.user)
        return all_prenotazioni.order_by('evento__data_evento','evento__nome','data')
    

class LocationDetailView(LoginRequiredMixin,PermissionRequiredMixin, generic.DetailView): #CBV per i dettagli di una location

    login_url = '/accounts/login/'
    model = Location
    permission_required = 'app_fun4all.can_manage_location'
    raise_exception = True


#FBV per amministratore del sito che può modificare la data fittizia
@login_required
@staff_member_required
def manage_data_fittizia(request,pk=None): 

    data_fittizia = None
    if pk:
        data_fittizia = get_object_or_404(DataFittizia, pk=pk)

    if request.method == 'POST':
        form = ManageDataFittiziaForm(request.POST, instance=data_fittizia)
        if form.is_valid():
            data_fittizia = form.save(commit=False)
            data_fittizia.pk = 1 # Forziamo l'uso di un singolo oggetto con pk=1
            data_fittizia.clean()
            data_fittizia.save()
            return HttpResponseRedirect(reverse('home'))
    else:
        try:
            data_fittizia = DataFittizia.objects.get(pk=1)
            form = ManageDataFittiziaForm(instance=data_fittizia)
        except DataFittizia.DoesNotExist:
            form = ManageDataFittiziaForm()

    return render(request, 'app_fun4all/manage_data_fittizia.html', {'form': form, 'data_fittizia': data_fittizia})


#FBV per proprietari di location
@login_required
@permission_required('app_fun4all.can_manage_location', raise_exception=True) 
def manage_location(request, pk =None): # pk se non c'è si crea una nuova location

    if pk:   # Recupera dati dal DB usando il pk, se non esiste lancia 404
        location = get_object_or_404(Location, pk=pk)
    else: # Nuova location
        location = None

    if request.method == 'POST':
        form = ManageLocationForm(request.POST, instance=location)
        if form.is_valid():
            loc = form.save(commit=False)# Non salviamo ancora l'oggetto nel DB
            if location is None:
                loc.proprietario = request.user  # Imposta il proprietario 
            loc.clean() #Chiamo metodi di model per validazioni aggiuntive
            loc.save() # Ora salviamo l'oggetto nel DB
            return HttpResponseRedirect(reverse('locations'))
    else:  # GET request: crea il form con i dati dell'oggetto esistente     
        form = ManageLocationForm(instance=location)
    
    return render(request, 'app_fun4all/manage_location.html', {'form': form, 'location': location})


#FBV per cambiare location da organizzatori di eventi
@login_required
@permission_required('app_fun4all.can_manage_evento', raise_exception=True)
def change_evento_location(request, pk):

    evento = get_object_or_404(Evento, pk=pk)

    if request.method == 'POST':
        form = ChangeEventoLocationForm(request.POST, instance=evento)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.clean() #Chiamo metodi di model per validazioni aggiuntive
            evento.save() 
            return HttpResponseRedirect(reverse('eventi'))
        else:
            print(form.errors)
    else:  # GET request     
        form = ChangeEventoLocationForm(request.POST, instance=evento)

    return render(request, 'app_fun4all/cambia_evento_location.html', {'form': form, 'evento': evento})

@login_required
@permission_required('app_fun4all.can_manage_evento', raise_exception=True)
def manage_evento(request, pk=None): 
    if pk:   # Recupera dati dal DB usando il pk, se non esiste lancia 404
        evento = get_object_or_404(Evento, pk=pk)
    else: # Nuovo evento
        evento = None

    if request.method == 'POST':
        form = ManageEventoForm(request.POST, instance=evento)
        if form.is_valid():
            evt = form.save(commit=False) 
            if evento is None:
                evt.organizzatore = request.user  # Imposta l'organizzatore
            evt.clean() 
            evt.save() 
            return HttpResponseRedirect(reverse('eventi'))
    else:  # GET request   
        form = ManageEventoForm(instance=evento)
    return render(request, 'app_fun4all/manage_evento.html', {'form': form, 'evento': evento})


#FBV per la cancellazione di un evento da parte di un proprietario, mostra in una pagina valore economi perduto
@login_required
@permission_required('app_fun4all.can_manage_evento', raise_exception=True)
def cancella_evento(request, pk):

    evento = get_object_or_404(Evento, pk=pk)

    valore_perduto = evento.biglietti_venduti * evento.costo
    if request.method == 'POST' and 'delete' in request.POST:
        for prenotazione in Prenotazione.objects.filter(evento=evento, stato='A'):
            prenotazione.stato = 'C'
            prenotazione.save()
        evento.stato = 'C'
        evento.save()
        return HttpResponseRedirect(reverse('eventi'))
    return render(request, 'app_fun4all/cancella_evento.html', {'evento': evento, 'valore_perduto': valore_perduto})


#FBV per i fruitori di prenotazioni
@login_required
@permission_required('app_fun4all.can_manage_prenotazione', raise_exception=True)
def manage_prenotazione(request, pk=None):
    if pk:   
        prenotazione = get_object_or_404(Prenotazione, pk=pk)
    else: # Nuova prenotazione
        prenotazione = None

    if request.method == 'POST':
        form = ManagePrenotazioneForm(request.POST, instance=prenotazione)
        print(form.errors)
        if form.is_valid():
            prn = form.save(commit=False)
            if prenotazione is None:
                prn.fruitore = request.user  # Imposta il fruitore
            prn.clean() 
            prn.save() 
            return HttpResponseRedirect(reverse('prenotazioni'))
    else:  # GET request      
        form = ManagePrenotazioneForm(instance=prenotazione)
    
    return render(request, 'app_fun4all/manage_prenotazione.html', {'form': form, 'prenotazione': prenotazione})


#FBV per la cancellazione di una prenotazione da parte di un fruitore
@login_required
@permission_required('app_fun4all.can_manage_prenotazione', raise_exception=True)
def cancella_prenotazione(request, pk):

    prenotazione = get_object_or_404(Prenotazione, pk=pk)
    if request.method == 'POST' and 'delete' in request.POST:
        prenotazione.stato = 'U'
        prenotazione.save()
    return HttpResponseRedirect(reverse('prenotazioni')) #Ritorna alla lista delle prenotazioni
   

#FBV per registrazione
def user_signup(request, next):
    if request.method != 'POST':
        form = SignupForm()
        return render(request, 'app_fun4all/signup.html', {'form': form})
    else:
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            auth_user = authenticate(username=form.cleaned_data['username'],
                                     password=form.cleaned_data['password1'])
            if auth_user is not None:
                login(request, auth_user)
                gruppo_utenti = Group.objects.get(name='Utenti')
                auth_user.groups.add(gruppo_utenti)
                return HttpResponseRedirect(next)
        return render(request, 'app_fun4all/signup.html', {'form': form})
    
