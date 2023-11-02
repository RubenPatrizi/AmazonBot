LAN = 0
LAN_dict = {
    "Italian": 0,
    "English": 1
}
COUNTRIES = ['it','co.uk','de','fr','es']

ft = ['File trovato','File found']
File_trovato = {'green':ft[LAN],'#565B5E':''}
Select_lan = ['Seleziona lingua\n(richiede il riavvio)','Select language\n(restart needed)']
Errore = ['Errore','Error']
Successo = ['Successo!','Success!']
Modifica = ['Aggiungi o rimuovi','Add or remove']
Aggiungi = ['Aggiungi','Add']
Salva = ['Salva','Save']
Elimina = ['Elimina','Remove']
Annulla = ['Annulla','Discard']
Conferma = ['Conferma','Confirm']
Aggiornamento = ['Tempo di\naggiornamento','Refresh time']
Prodotto_esistente = ['Il prodotto è già presente', 'Already existing product']
Prodotto_inesistente = ['Il prodotto non è presente', 'Product does not exist']
Nessun_prodotto = ['Nessun prodotto salvato','No saved product']
Acquistato = ['Articolo acquistato a','Article bought for']
Guida = ['Guida','Guide']
Utilizzo = ['UTILIZZO','HOW TO USE']
DC = ['Download Chromedriver','Chromedriver download']
Indietro = ['Indietro','Go back']
Telegram_Username = ['Username Telegram','Telegram Username']
Dettagli_prod = ['Dettagli prodotto','Product details']
Codice = ['Codice prodotto','Product code']
Gestisci = ['Gestione prodotti','Manage products']
Prezzo = ['Prezzo','Price']
Prezzo_max = ['Prezzo massimo','Limit price']
Acquistare = ['Acquistare da Amazon...','Buying from Amazon...']
Dettagli_acc = ['Dettagli account','Account details']
Salva_credenziali = ['Salva\ncredenziali', 'Save\ncredentials']
Condizioni_prodotto = ['Non acquistare\nprodotti usati','Do not buy\nused products']
Modalita_notif = ['Modalità segnalazione','Notification only mode']
Segnalazioni = ['Segnalazioni: ', 'Reports: ']
Cronologia = ['Cancella\ncronologia','Delete\nhistory']
Avvia = ['Avvia','Start']
Esci = ['Esci','Exit']
Guida_utilizzo = ['Guida utilizzo','How to use']
Formato_dati = ['Formato dati errato','Invalid data']
Seleziona = ['Seleziona...','Select...']
Selezione = ['Seleziona prodotto','Select product']
Opzionale = ['@opzionale','@optional']
Opzioni = ['Altre opzioni...         ','Other options...      ']
Condizioni = {"title": ['Condizioni prodotto','Product conditions'],
              "any": ['Qualsiasi','Any'],
              "new": ['Solo nuovo','New only'],
              "used": ['Solo usato','Used only']}
Venditori = ['Venditori','Sellers']
Captcha = ['Captcha rilevato...\n','Captcha detected...\n']
Nome = ['Nome','Name']
Qualcosa = ['Qualcosa è andato storto :(','Something went wrong :(']
Version_error = ['Versione Chromedriver non supportata!\nScaricare una versione aggiornata...',
                 'Chromedriver version not supported!\nTry downloading a newer version...']
Si = ['Sì','Yes']
No = ['No','No']

INFO_SLR = ['Inserire i nomi dei venditori di cui controllare il prezzo\n'
            'separati da una virgola (se non si inserisce niente non\n'
            'verranno effettuati controlli sul venditore).\n\n'
            'Es: Amazon,nrsolutions,bell3',
            'Insert names of sellers you want to track,\n'
            'separated by a comma (if no seller is provided\n'
            'only lowest price offers will be checked)\n\n'
            'e.g.: Amazon,nrsolutions,bell3']

USED = {
    'it': "Usato",
    'uk': "Used",
    'de': "Used",
    'fr': "D'occasion",
    'es': "De 2ª mano"
}
SOLD_BY = {
    'it': "Venditore",
    'uk': "Sold by",
    'de': "Sold by",
    'fr': "Vendeur",
    'es': "Vendedor"
}

INFO_MNG_IT = 'Per aggiungere un prodotto inserire il suo codice e assegnargli\n' \
              ' un nome per identificarlo.\n' \
              'Per rimuovere un prodotto selezionarlo dal menu.\n'
INFO_MNG_EN = 'To add a product insert its code and give it a name.\n' \
              'To remove a product select it from the menu.\n'
INFO_MNG = [INFO_MNG_IT,INFO_MNG_EN]

GUIDE_TEXT_IT = '1) Chromedriver.exe\n\n ' \
                '    Se il file è già presente nella cartella del programma verrà rilevato automaticamente.\n' \
                '    È richiesta la stessa versione del Chrome installato nel PC (Chrome > Impostazioni > Informazioni)\n' \
                '    Chromedriver può essere scaricato anche dal pulsante in fondo alla guida.\n\n\n' \
                '2) Dettagli prodotto:\n\n' \
                '     ● Il Codice del prodotto ha 10 caratteri e si trova nel link della relativa pagina.\n' \
                '       es: https://www.amazon.it/dp/B0815XFSGK/ref=olp-opf-redir...\n' \
                '             il codice è B0815XFSGK\n\n' \
                '     ● Il campo Prezzo è in euro ed è un numero intero (no decimali). In caso di acquisto da Amazon UK\n' \
                '       il prezzo NON viene convertito in sterline (prezzo massimo 999.999).\n' \
                '       es: 150\n' \
                '             verrà acquistato il prodotto se sotto 150.99€/£\n\n\n' \
                '3) L\'acquisto dovrebbe andare a buon fine anche saltando questo passaggio, tuttavia meglio assicurarsi\n' \
                '    di avere un indirizzo e un metodo di pagamento predefiniti sul proprio account Amazon:\n' \
                '    nella pagina di conferma dell\'ordine deve essere subito visibile il pulsante \"Acquista ora\".\n' \
                '    Se così non fosse basta effettuare un ordine spuntando la casella per rendere le opzioni di\n' \
                '    consegna e di pagamento di default in futuro.\n\n\n' \
                'TELEGRAM\n' \
                '  ● Opzionalmente potete inserire il vostro username Telegram (@xyz) per ricevere una notifica\n' \
                '    sul gruppo quando l\'articolo viene acquistato.\n' \
                '  ● In modalità seganalazione il prodotto non verrà acquistato ma quando il prezzo scende\n ' \
                '    sotto il limite impostato riceverete una notifica sul gruppo Telegram con il link per\n' \
                '    acquistarlo manualmente (in questo caso è necessario inserire il proprio username).\n' \
                '  ● Se si presenta un problema dopo che il prezzo inserito è stato raggiunto verrà comunque\n' \
                '    inviata una notifica sul gruppo telegram per avvisarvi di completare l\'acquisto manualmente,\n' \
                '    a prescindere dal fatto che abbiate inserito uno username o meno.\n\n\n' \
                'EXTRA\n' \
                '  ● Dopo aver chiuso il software il processo rimarrà comunque aperto in background. Finchè non\n' \
                '    avrò trovato una soluzione chiudetelo manualmente dal task manager.\n' \

GUIDE_TEXT_EN = '1) Chromedriver.exe\n\n' \
                '   If the file is already present in the program directory it will be detected automatically.\n' \
                '   The file version must be the same of your Chrome browser (Chrome > Settings > Information)\n' \
                '   You can download Chromedriver from the button at the bottom of this guide.\n\n' \
                '2) Product details:\n\n' \
                '     ● Product code has 10 characters and it can be found in the link of the product page.\n' \
                '       e.g. https://www.amazon.it/dp/B0815XFSGK/ref=olp-opf-redir...\n' \
                '              The product code is B0815XFSGK\n\n' \
                '     ● Price field is an integer and will be considered £ if buying from Amazon UK, € otherwise\n' \
                '       (max price 999.999).\n' \
                '       e.g. 150\n' \
                '              the product will be bought once below 150.99€/£\n\n' \
                '3) There shouldn\'t be any issue if you skip this step, but better make sure you have a default\n' \
                '   address and payment method on your account.\n\n' \
                'TELEGRAM\n' \
                '  ● You can optionally insert your Telegram username (@xyz) to receive a message on the\n' \
                '    Telegram bot group when the article is purchased.\n' \
                '  ● In notification mode the product will not be purchased automatically, instead you will\n ' \
                '    receive a message on the Telegram group with current price and a link to the product page,\n' \
                '    so you can buy it manually (in this case the Telegram username is mandatory).\n' \
                '  ● If a problem occours after target price has been reached you will be notified on the\n' \
                '    telegram group so you can complete the purchase manually (this happens even if you\n' \
                '    didn\'t insert a username).\n\n\n' \
                'EXTRA\n' \
                '  ● After you close the software a process will still be active in background. Please close it\n' \
                '    manually from task manager until I find a solution\n'

GUIDE_TEXT = [GUIDE_TEXT_IT,GUIDE_TEXT_EN]

chrome_link = 'https://chromedriver.chromium.org/downloads'
discord_link = ''    # your discord server
telegram_link = ''    # your telegram group
support_link = 'https://www.paypal.me/ssswordsman'
