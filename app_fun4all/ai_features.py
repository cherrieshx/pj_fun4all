# app_fun4all/ai_features.py
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pathlib import Path

load_dotenv(Path(__file__).resolve().parent / '.env')
load_dotenv()

def genera_descrizione_evento(nome_evento: str) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return "Errore: chiave API non trovata nel file .env"

    client = genai.Client(api_key=api_key)
    
    config = types.GenerateContentConfig(
        system_instruction = (
            "Sei il copywriter ufficiale della piattaforma 'Fun4All'.\n\n"
            
            "ORDINE FONDAMENTALE DI RICERCA:\n"
            "Prima di scrivere, fai SEMPRE una ricerca web con Google Search sul nome dell'evento. "
            "Individua a quale categoria appartiene e CITA I FATTI REALI scoperti dalla ricerca:\n\n"
            
            "- SE CONCERTO / MUSICA: cita il cantante o la band reale, le loro caratteristiche, cita eventualmentegli album o le hit più famose.\n"
            "- SE COMICITÀ / STAND-UP: cita il nome del comico, lo show reale e i temi specifici della sua satira.\n"
            "- SE CIBO / STREET FOOD / SAGRA: cita i piatti tipici reali (es. porchetta, tartufo, arrosticini), le birre artigianali o i prodotti locali della tradizione.\n"
            "- SE FIERA DEL FUMETTO / COMICS: cita il nome della fiera, gli ospiti noti (disegnatori, doppiatori), l'area cosplay o i tornei gaming.\n"
            "- SE TEATRO / MUSICAL: cita il titolo dell'opera teatrale, la compagnia, il regista e un accenno concreto alla trama.\n"
            "- SE SPORT / GARA / OUTDOOR: cita la disciplina esatta, il tipo di sfida (es. 5km, torneo a gironi, arrampicata).\n"
            "- SE MOSTRA / ARTE: cita l'artista in esposizione, il tema della galleria o le opere di spicco.\n\n"
            
            "DIVIETO ASSOLUTO DI FRASI FATTE (ANTI-CLICHÉ):\n"
            "NON usare MAI espressioni vuote come: 'divertimento assicurato', 'energia travolgente', "
            "'un evento unico', 'emozioni indimenticabili', 'non fartelo raccontare'. "
            "Sii giornalistico, preciso e concreto.\n\n"
            
            "LIMITI TECNICI:\n"
            "1. EMOJI: inserisci rigorosamente massimo 1 o 2 emoji in tutto il testo.\n"
            "2. LUNGHEZZA: non superare mai i 280 caratteri."
        ),
        max_output_tokens=100, 
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=f"Nome evento: {nome_evento}",
            config=config
        )
        testo = response.text.strip()
        
        # Protezione extra per il database (max_length=300)
        if len(testo) > 300:
            testo = testo[:297] + "..."
            
        return testo
    except Exception as e:
        return f"Errore durante la generazione: {str(e)}"