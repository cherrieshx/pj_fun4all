function cancella_evento(evento_id) {
    if (!confirm("Sei sicuro di voler cancellare questo evento?")) return;

    const csrfToken = document.getElementById("csrf-token").value;

    const xhttp = new XMLHttpRequest();
    xhttp.onload = function() {
        const obj = JSON.parse(this.responseText);
        if (obj.success) {
            // Rimuove l'elemento dalla lista
            const liElem = document.getElementById("evento-" + evento_id);
            if (liElem) liElem.remove();
            alert(obj.message);
        } else {
            alert(obj.message);
        }
    };

    xhttp.open("POST", "/app_fun4all/cancella_evento_ajax/" + evento_id);
    xhttp.setRequestHeader("X-CSRFToken", csrfToken);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send();
}

function cancella_prenotazione(prenotazione_id) {
    if (!confirm("Sei sicuro di voler cancellare questa prenotazione?")) return;
if (!confirm("Sei sicuro di voler cancellare questo evento?")) return;

    const csrfToken = document.getElementById("csrf-token").value;
}

     