from django.shortcuts import render
from .models import Evento, Location, Prenotazione, DataFittizia
from .forms import ManageDataFittiziaForm,ManageLocationForm, ChangeEventoLocationForm, ManageEventoForm, ManagePrenotazioneForm,ManagePrenotazioneForm,SignupForm
from django.views import generic
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import timedelta



def resetlogin(request, next):
    request.session['num_visits'] = 0 # azzera il contatore visite
    request.session.modified = True # forza il salvataggio della sessione
    return HttpResponseRedirect(reverse('login') + "?next=" + next)# reindirizza alla pagina di login

class HomeListView(generic.ListView):

    model = Evento
    template_name = 'index.html'
    context_object_name = 'eventi_attivi'
    paginate_by = 3
    
    # n_eventi = Evento.objects.all().count()
    # n_locations = Location.objects.all().count()
    # n_prenotazioni = Prenotazione.objects.all().count()
    
    def get_queryset(self):
        return Evento.objects.filter(
                 stato ='A',
                ).order_by("data_evento","nome","location")

         
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['data_corrente']= DataFittizia.objects.first()
        return ctx
    

class LocationListView(generic.ListView):

    login_url = '/accounts/login/'
    model = Location
    paginate_by = 3

    def get_queryset(self):
        all_locations = Location.objects.all()
        return all_locations.order_by('nome') 

class EventoListView(generic.ListView):
    login_url = '/accounts/login/'
    model = Evento
    paginate_by = 3

    def get_queryset(self):
        all_eventi = Evento.objects.all()
        return all_eventi.order_by('data_evento','nome','location')

    
class PrenotazioneListView(generic.ListView):
    login_url = '/accounts/login/'
    model = Prenotazione
    paginate_by = 3

class LocationDetailView(LoginRequiredMixin,PermissionRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    model = Location
    permission_required = 'app_fun4all.can_manage_location'
    paginate_by = 3

    def get_queryset(self):
        all_locations = Location.objects.all()
        return all_locations.order_by('nome')

class EventoDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    model = Evento

class PrenotazioneDetailView(LoginRequiredMixin, generic.DetailView):
    login_url = '/accounts/login/'
    model = Prenotazione

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

@login_required
@permission_required('app_fun4all.can_manage_location', raise_exception=True)
def manage_location(request, pk =None): # pk è opzionale, se non c'è si crea una nuova location

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

@login_required
@permission_required('app_fun4all.can_manage_evento', raise_exception=True)
def change_evento_location(request, pk):

    evento = get_object_or_404(Evento, pk=pk)

    if request.method == 'POST':
        form = ChangeEventoLocationForm(request.POST, instance=evento)
        if form.is_valid():
            print("Form is valid")
            evento = form.save(commit=False)
            evento.clean() #Chiamo metodi di model per validazioni aggiuntive
            evento.save() # Ora salviamo l'oggetto nel DB
            return HttpResponseRedirect(reverse('eventi'))
        else:
            print("FORM NON VALIDO")
            print(form.errors)
    else:  # GET request: crea il form con i dati dell'oggetto esistente      
        form = ChangeEventoLocationForm(request.POST, instance=evento)

    return render(request, 'app_fun4all/cambia_evento_location.html', {'form': form, 'evento': evento})

@login_required
@permission_required('app_fun4all.can_manage_evento', raise_exception=True)
def manage_evento(request, pk=None): # pk è opzionale, se non c'è si crea un nuovo evento
    if pk:   # Recupera dati dal DB usando il pk, se non esiste lancia 404
        evento = get_object_or_404(Evento, pk=pk)
    else: # Nuovo evento
        evento = None

    if request.method == 'POST':
        
        form = ManageEventoForm(request.POST, instance=evento)
        if form.is_valid():
            evt = form.save(commit=False) # Non salviamo ancora l'oggetto nel DB
            if evento is None:
                evt.organizzatore = request.user  # Imposta l'organizzatore
            evt.clean() #Chiamo metodi di model per validazioni aggiuntive
            evt.save() # Ora salviamo l'oggetto nel DB
            return HttpResponseRedirect(reverse('eventi'))
    else:  # GET request: crea il form con i dati dell'oggetto esistente      
        form = ManageEventoForm(instance=evento)

    return render(request, 'app_fun4all/manage_evento.html', {'form': form, 'evento': evento})

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

@login_required
@permission_required('app_fun4all.can_manage_prenotazione', raise_exception=True)
def manage_prenotazione(request, pk=None):
    if pk:   # Recupera dati dal DB usando il pk, se non esiste lancia 404
        prenotazione = get_object_or_404(Prenotazione, pk=pk)
        importo_totale = prenotazione.numero_biglietti * prenotazione.evento.costo
    else: # Nuova prenotazione
        prenotazione = None

    if request.method == 'POST':
        if 'delete' in request.POST and prenotazione is not None:
            prenotazione.stato = 'C'
            prenotazione.clean()
            prenotazione.save()
            return HttpResponseRedirect(reverse('prenotazioni'))
        else:
            form = ManagePrenotazioneForm(request.POST, instance=prenotazione)
            if form.is_valid():
                prn = form.save(commit=False)# Non salviamo ancora l'oggetto nel DB
                if prenotazione is None:
                    prn.utente = request.user  # Imposta l'utente 
                prn.clean() #Chiamo metodi di model per validazioni aggiuntive
                prn.save() # Ora salviamo l'oggetto nel DB
                return HttpResponseRedirect(reverse('prenotazioni'))
    else:  # GET request: crea il form con i dati dell'oggetto esistente      
        
        form = ManagePrenotazioneForm(instance=prenotazione)
    
    return render(request, 'app_fun4all/manage_prenotazione.html', {'form': form, 'prenotazione': prenotazione})

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
    
