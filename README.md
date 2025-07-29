# SENSORE DI OMBRE CON ARDUINO

Questo progetto ha come obiettivo la realizzazione di un dispositivo Arduino capace di rilevare la presenza o l'assenza di luce, registrando quindi i risultati su un server/database Django in tempo reale.

## OBIETTIVO

Utilizzare un sensore fotosensibile per monitorare la luminosità ambientale e registrare la presenza o l'assanza di luce a seconda di una soglia predefinita.

## COMPONENTI UTILIZZATI

x1 Bread Board

x1 Fotoresistore

Resistenze (x1 220 Ohm, x1 10KOhm)

x1 LED

x1 Modulo Wi-Fi ESP32 

x1 cavo USB-C

## FUNZIONAMENTO

Il sensore rileva costantemente il livello di luce ambientale.

Se il valore scende o supera una certa soglia, viene determinato lo stato luce o ombra.

Il sistema invia una notifica al server informando del cambiamento e il server archivia il risultato con relative data e ora.

## POSSIBILI SVILUPPI FUTURI

Personalizzazione della soglia

Log storico degli stati

RAPPRESENTAZIONE DEL CIRCUITO

![Circuito](fotoREADME.jpg)

📄 Licenza

Questo progetto è distribuito sotto licenza MIT - vedi il file LICENSE per i dettagli.
