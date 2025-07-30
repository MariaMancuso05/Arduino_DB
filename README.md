# SENSORE DI OMBRE CON ARDUINO

## OBIETTIVO

Questo progetto ha come obiettivo la realizzazione di un dispositivo Arduino capace di rilevare la presenza o l'assenza di luce e gestire la richiesta delle informazioni da parte dell'utente con una password.

La sensibilità dello strumento potrà essere customizzata dall'utente in base alle sue necessità, così come la password di accesso.

Insieme alle specifiche del dispositivo, questo progetto comprende un server Django su cui l'arduino invierà **live** i cambiamenti di stato luce/ombra. Il server registrerà sul database la data e ora in cui è avvenuto ogni cambiamento di stato

Il server è provvisto di un UI user friendly.


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

Attraverso il serial monitor sarà possibile, inserendo la password corretta, avere informazioni riguardo lo stato attuale del LED.

In caso si facessero 3 errori consecutivi cercando di inserire la password, il buzzer emetterà un suono e non sarà possibile inserire password fino a che non verrà fatto uno sblocco manuale ruotando il potenziometro.

## POSSIBILI SVILUPPI FUTURI

Personalizzazione dinamica della soglia tramite interfaccia web o API.

Invio notifiche su dispositivi personali (tramite email, Telegram, ecc.).

Storico dei dati con visualizzazione tramite grafici.

## RAPPRESENTAZIONE DEL CIRCUITO

![Circuito](circuit.png)

## GUIDA AL DEBUGGING

Nonostante tutti contatti di output presenti sull'ESP32 suppotino la tecnologia analogica, solamente quelli compresi tra 32 e 37 supportano l'analogico con il WiFI.

Per permettere la comunicazione tra l'arduino e il server Django è necessario disattivare il Firewall della macchina su cui si trova il server o, preferibilmente, impostare una regola specifica.

## REQUISITI

Python + Django installati su server locale o cloud

Libreria Wi-Fi per ESP32 (inclusa nell'IDE Arduino)

Conoscenze base di circuiti elettronici e programmazione embedded
