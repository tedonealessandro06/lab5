# Buongiorno Professore,
# purtroppo sto affrontando alcune serie difficoltà familiari ed economiche che, al momento,
# mi impediscono di frequentare le lezioni con regolarità e di rispettare le scadenze previste.
# svolgerò comunque tutti gli esercizi.
# La ringrazio di cuore se terrà in considerazione, anche solo in parte, il lavoro svolto

import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"        #1
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK   #2

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD) #3
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField(label="Tipo")
    input_marca = ft.TextField(label="Marca")
    input_anno = ft.TextField(label="Anno di acquisto")
    #contatore parte 1
    contatore = ft.TextField(
        label="Quantità",
        value="1",
        width=100,
        read_only=True,
        text_align=ft.TextAlign.CENTER
    )

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def aggiungi_strumento(e):
        try:
            tipo = input_tipo.value.strip()
            marca = input_marca.value.strip()
            anno = int(input_anno.value)
            valore = float(contatore.value)

            if not tipo or not marca:
                alert.show_alert("Inserisci tipo e marca dello strumento.")
                return

            if anno <= 0 or valore < 0:
                alert.show_alert("Anno e valore devono essere validi.")
                return

            deposito.aggiungi_strumento(tipo, marca, anno, valore)
            #svuoto campi
            input_tipo.value = ""
            input_marca.value = ""
            input_anno.value = ""
            #riporta contatore a 0
            contatore.value = "0"
            #aggiorno
            aggiorna_lista_strumenti()
            page.update()



        except ValueError:
          alert.show_alert("Inserisci un anno numerico valido.")

    # contatore parte 2
    def aumenta_contatore(e):
        contatore.value = str(int(contatore.value) + 1)
        contatore.update()

    def diminuisci_contatore(e):
        contatore.value = str(max(1, int(contatore.value) - 1))
        contatore.update()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)
    pulsante_aggiungi_strumento=ft.Button("Aggiungi strumento", on_click=aggiungi_strumento)
    #contatore parte 3
    pulsante_meno = ft.IconButton(icon=ft.Icons.REMOVE,on_click=diminuisci_contatore)
    pulsante_piu = ft.IconButton(icon=ft.Icons.ADD,on_click=aumenta_contatore)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Text("Aggiungi nuovo strumento", size=20),
        ft.Row(spacing=10,
               controls=[input_tipo, input_marca, input_anno],
               alignment=ft.MainAxisAlignment.CENTER),

        #Sezione 4
        ft.Row(spacing=20,
               controls=[pulsante_meno, contatore,
                         pulsante_piu, pulsante_aggiungi_strumento],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 5
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

ft.run(main)
