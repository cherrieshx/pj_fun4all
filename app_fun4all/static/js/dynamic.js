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

async function generaConAI() {
    const Nome = document.getElementById("id_nome");
    const Descrizione = document.getElementById("id_descrizione");

    if (!Nome || !Nome.value.trim()) {
        alert("Per favore, inserisci prima il nome dell'evento!");
        if (Nome) Nome.focus();
        return;
    }
    const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
    const csrfToken = csrfInput ? csrfInput.value : "";

    Descrizione.value = "Generazione in corso con l'AI...";
    try {
        const response = await fetch("/api/genera-descrizione/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({ nome: Nome.value.trim() })
        });
        const data = await response.json();
        if (data.descrizione) {
            Descrizione.value = data.descrizione;
        } else {
            alert("Errore: " + (data.error || "Impossibile generare la descrizione"));
            Descrizione.value = "";
        }
    } 
    catch (error) {
        alert("Errore di connessione con il server: " + error);
            Descrizione.value = "";
    }
}

     