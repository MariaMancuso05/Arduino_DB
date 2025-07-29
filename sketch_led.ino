#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

char ssid[] = "ArzWiFi";
char pass[] = "ArzMat02";

const char* serverURL = "http://10.86.167.11:8000/api/light/";

#define PIN_LED 12
#define PIN_ANALOG_IN 33
#define SOGLIA_LUCE 100

WiFiClient client;

bool stato = false;
bool stato_precedente = stato;

void setup() {
  Serial.begin(115200);
  pinMode(PIN_LED, OUTPUT);

  WiFi.begin(ssid, pass);
  Serial.println("Connessione in corso...");
  while (WiFi.status() != WL_CONNECTED)  {
    Serial.print(".");
    delay(400);
  }
  Serial.println("");
  Serial.println("WiFi connesso");
  Serial.println("Indirizzo IP: ");
  Serial.println(WiFi.localIP());
  delay(500);

  Serial.print("Connecting to ");

}

void loop(){
  int adcVal = analogRead(PIN_ANALOG_IN);
  int luce = map(adcVal, 0, 4095, 0, 255);
  controlloLed(luce);
  int a = trovaTransizione(stato, stato_precedente);
  if (a != 0) {
    switch (a) {
      case 1 :
        mandaStato(1);
        stato_precedente = stato;
        break;
      case -1 :
        mandaStato(-1);
        stato_precedente = stato;
        break;
    }
  }
  delay (200);
}

void controlloLed(int luce) {

  //Serial.print(" - Luce mappata: ");
  //Serial.println(luce);

  if (luce <= SOGLIA_LUCE) {
    digitalWrite(PIN_LED, HIGH);
    stato = true;
  }
  else {
    digitalWrite(PIN_LED, LOW);
    stato = false;
  }
}

int trovaTransizione(bool corrente,bool precedente) {
  if (!precedente && corrente)
    return 1; //da spento a acceso
  else if (precedente && !corrente)
    return -1; //da acceso a spento
  else 
    return 0; //nessun cambiamento
}

void mandaStato(int stato) {
  String stringStato;
  if (stato == 1)
    stringStato = "acceso";
  else if (stato == -1)
    stringStato = "spento";
  HTTPClient http;
  http.begin(serverURL);
  http.addHeader("Content-Type", "application/json");

  StaticJsonDocument<200> doc;
  doc["stato"] = stringStato;

  String jsonString;
  serializeJson(doc, jsonString);

  int httpCode = http.POST(jsonString);
  
  if (httpCode == 200 || httpCode == 201) {
    Serial.println("Dati inviati con successo!");
    String response = http.getString();
    Serial.println("Risposta server: " + response);
  } else {
    Serial.println("Errore invio: " + String(httpCode));
  }
  http.end();
}




