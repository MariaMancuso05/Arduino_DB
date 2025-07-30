# SENSORE DI OMBRE CON ARDUINO

## OBIETTIVO

Questo progetto ha come obiettivo la realizzazione di un dispositivo Arduino capace di rilevare la presenza o l'assenza di luce e gestire la richiesta delle informazioni da parte dell'utente con una password.

La sensibilità dello strumento potrà essere customizzata dall'utente in base alle sue necessità, così come la password di accesso.

Insieme alle specifiche del dispositivo, questo progetto comprende un server Django su cui l'arduino invierà **live** i cambiamenti di stato luce/ombra. Il server registra sul database la data e ora in cui è avvenuto ogni cambiamento di stato

Il server è provvisto di un UI user friendly.

La sicurezza dell'arduino è rinforzata dalla necessità di digitare una password tramite terminale prima di ottenere accesso ai dati raccolti dallo strumento, anche mentre esso è in funzione.

E' inoltre presente un rinforzo aggiuntivo contro le strategie di brute force.


## COMPONENTI UTILIZZATI

- x1 Bread board

- x1 ESP32 con modulo Wi-Fi

- x1 Potenziometro

- x1 Buzzer

- x1 Fotoresistore

- x1 Transistor

- x1 LED

- x2 Resistore 220 Ohm
  
- x2 Resistore 10k Ohm

- x1 Resistore 1k Ohm

- x10 cavetti

- x1 cavo USB-C

- Fonti (3.3V, 5V)

## FUNZIONAMENTO

Quando acceso, il sensore rileva continuamente il livello di luce ambientale.

Se il valore è inferiore o supera la soglia impostata dall'utente l'arduino invia una segnale di cambiamento di stato, da luce a ombra o viceversa.

Il dispositivo invia una notifica al server e il server la archivia con relative data e ora.

Qualora si volesse osservare i dati direttamente dall'arduino invece di usare il database, per garantire maggiore sicurezza le informazioni sono visibili solo dopo aver digitato una password tramite terminale.

Contro le tecniche di brute force, qualora fosse digitata per tre volte una password errata, il dispositivo emetterà un suono d'allarme e bloccherà ogni successivo tentativo di login.

Per sbloccare il processo di login, sarà necessario resettarlo manualmente girando la rotellina presente sul dispositivo.


## POSSIBILI SVILUPPI FUTURI

Personalizzazione dinamica della soglia tramite interfaccia web o API.

Invio notifiche su dispositivi personali (tramite email, Telegram, ecc.).

Storico dei dati con visualizzazione tramite grafici.

## RAPPRESENTAZIONE DEL CIRCUITO

![Circuito](circuit.png)

## GUIDA AL DEBUGGING

Nonostante tutti contatti di output presenti sull'ESP32 supportino la tecnologia analogica, solamente quelli compresi tra 32 e 37 supportano l'analogico con il WiFI.

Per permettere la comunicazione tra l'arduino e il server Django è necessario disattivare il Firewall della macchina su cui si trova il server o, preferibilmente, impostare una regola specifica.

## REQUISITI

Python + Django installati su server locale o cloud

Libreria Wi-Fi per ESP32 (inclusa nell'IDE Arduino)

Conoscenze base di circuiti elettronici e programmazione embedded

## GUIDA ALL'INSTALLAZIONE
