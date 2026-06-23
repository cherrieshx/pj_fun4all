# Fun4All

## Descrizione

**Fun4All** è un progetto universitario sviluppato con Django per il corso di **Progettazione e Sviluppo di Applicazioni Web**.

L'applicazione consente la gestione di eventi di intrattenimento pubblico, come concerti, fiere del fumetto, festival e manifestazioni, mettendo in comunicazione diverse tipologie di utenti:

* Amministratori del sistema
* Proprietari delle location
* Organizzatori di eventi
* Fruitori degli eventi

Il sistema utilizza una **data fittizia** per simulare il trascorrere del tempo e consentire la gestione delle funzionalità legate alle date degli eventi.

---

## Funzionalità

### Utenti non autenticati

Gli utenti non autenticati possono:

* Visualizzare la home page.
* Consultare gli eventi attivi.
* Registrarsi al sistema.
* Effettuare il login.

---

### Amministratori del sistema

Gli amministratori possono:

* Modificare la data fittizia del sistema.
* Accedere al pannello di amministrazione Django.
* Gestire utenti e gruppi.
* Creare nuovi account.
* Assegnare ruoli e permessi agli utenti.

---

### Proprietari delle location

I proprietari possono:

* Creare nuove location tramite apposito form.
* Specificare il periodo di apertura della location.
* Impostare lo stato della location (attiva/inattiva).
* Visualizzare e modificare le proprie location.

---

### Organizzatori di eventi

Gli organizzatori possono:

* Creare nuovi eventi.
* Selezionare esclusivamente location disponibili e attive nella data dell'evento.
* Visualizzare i propri eventi.
* Cancellare un evento fino a 10 giorni prima della data fittizia del sistema.

In caso di cancellazione di un evento con prenotazioni già effettuate, il sistema mostra:

* Numero totale delle prenotazioni annullate.
* Valore economico complessivo delle prenotazioni perse.

---

### Fruitori degli eventi

I fruitori possono:

* Visualizzare gli eventi attivi.
* Prenotare uno o più biglietti per un evento.

Il sistema verifica automaticamente che:

* I dati inseriti siano validi.
* Il numero totale dei biglietti prenotati non superi la capienza della location associata all'evento.

---

## Gestione della coerenza dei dati

L'applicazione implementa controlli automatici per mantenere la coerenza del sistema.

Le modifiche relative a:

* Data fittizia del sistema
* Location
* Eventi
* Prenotazioni

possono generare aggiornamenti automatici di altri dati correlati per garantire la correttezza delle informazioni memorizzate.

---


## Requisiti Software

Per eseguire il progetto è necessario avere installato:

* Python 3.12 o superiore
* pip
* Git

Verifica dell'installazione:

```bash
python --version
pip --version
git --version
```

---

## Installazione

Clonare il repository:

```bash
git clone https://github.com/USERNAME/Fun4All.git
```

Entrare nella cartella del progetto:

```bash
cd Fun4All
```

Creare un ambiente virtuale:

```bash
python -m venv venv
```

Attivare l'ambiente virtuale:

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Installare le dipendenze:

```bash
pip install -r requirements.txt
```

---

## Configurazione del Database

Applicare le migrazioni:

```bash
python manage.py makemigrations
python manage.py migrate
```

Creare un superutente:

```bash
python manage.py createsuperuser
```

Seguire le istruzioni visualizzate nel terminale.

---

## Avvio dell'Applicazione

Avviare il server Django:

```bash
python manage.py runserver
```

L'applicazione sarà disponibile all'indirizzo:

```text
http://127.0.0.1:8000/
```

Pannello di amministrazione:

```text
http://127.0.0.1:8000/admin/
```



## Credenziali di Test

Per testare nella cartella vi è un file admin.txt ove ci sono le credenziali per vari tipi di utenti.


