#define BLYNK_PRINT Serial
#include <ESP8266WiFi.h>
#include <BlynkSimpleEsp8266.h>
#include <WiFiServer.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ESP8266WebServer.h>
#include <ArduinoOTA.h>
#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <NTPClient.h>//Biblioteca do NTP.
#define SEALEVELPRESSURE_HPA (1013.25)

#define pinoPir 16

Adafruit_BME280 bme;

const uint16_t kIrLed = 0; 
IRsend emissorIR(kIrLed);

WidgetLED ledPir(V6);

WiFiUDP udp;//Cria um objeto "UDP".
NTPClient ntp(udp, "a.st1.ntp.br", -3 * 3600, 60000);
ESP8266WebServer server(80);
WiFiClient cliente;

char command;
String txt;
String page = "";
String text = "";
const char* ssid = "DORETOALENCAR";
const char* password = "16043028";
char auth[] = "UWz7EPfyUAD_kJPb6h0bckmoVo0uhz9I";
String req;

#define tempoTecla 350
float h,t,pres, alt;
int valuePir;
int lum = 0;
signed long rssi = WiFi.RSSI();



void setup(void) {
  
  Blynk.begin(auth, ssid, password);  
  
  pinMode(pinoPir, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, HIGH);
  bme.begin(0x76);   
  emissorIR.begin();
  Serial.begin(9600);
  Serial.print("Conectando à ");
  Serial.println(ssid);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500); //Condição de verificação que ENQUANTO a rede não conectar, ele continurá printando “.”.

    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi conectado");
  // Wait for connection
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  ntp.begin();//Inicia o NTP.
  ntp.forceUpdate();//Força o Update.
  ArduinoOTA.onStart([]() {
    Serial.println("Inicio...");
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("nFim!");
  });
  ArduinoOTA.onProgress([](unsigned int progress, unsigned int total) {
    Serial.printf("Progresso: %u%%r", (progress / (total / 100)));
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("Erro [%u]: ", error);
    if (error == OTA_AUTH_ERROR) Serial.println("Autenticacao Falhou");
    else if (error == OTA_BEGIN_ERROR) Serial.println("Falha no Inicio");
    else if (error == OTA_CONNECT_ERROR) Serial.println("Falha na Conexao");
    else if (error == OTA_RECEIVE_ERROR) Serial.println("Falha na Recepcao");
    else if (error == OTA_END_ERROR) Serial.println("Falha no Fim");
  });
  ArduinoOTA.begin();


 server.on("/sensors", [](){
   text = "{\"lum\":" + String(lum) + ", \"t\": " + String(t) + ", \"h\": " + String(h) + ",\"pres\": " + String(pres) + ",\"alt\": " + String(alt)+ ",\"rssi\": " + String(rssi) + "}";
  server.send(200, "application/json", text);
 });
 server.on ("/genericArgs", handleGenericArgs); // Associe a função do manipulador ao caminho
 server.on("/", [](){
   page = "<!DOCTYPE html><html><head> <meta http-equiv = 'Content-Type' content = 'text / html; charset = utf-8'><title>Painel Sensores</title>";//Identificaçao e Titulo.
   page += "<style>body{margin-top: 50px;} h2 {color: #444444;margin: 50px auto 30px;} html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;} p {font-size: 24px;color: #444444;margin-bottom: 10px;}</style></head>";//Cria uma nova fonte de tamanho e cor X.
   page += "<body bgcolor='#FFFAFA'><center>";//Cor do Background
   page += "<h2>SENSORES EM FUNCIONAMENTO</h2>";
   page += "<p>Luminosidade:<span id=\"lum\">""</span></p>";
   page += "<p>Temperatura: <span id=\"t\">""</span>&deg;C</p>";
   page += "<p>Umidade:<span id=\"h\">""</span>%</p>";
   page += "<p>Pressão atmosférica: <span id=\"pres\">""</span>hPa</p>";
   page += "<p>Altitude: <span id=\"alt\">""</span>m</p>";
   page += "<p>Intens. do Sinal: <span id=\"rssi\">""</span></p>";
   page += "<script>\r\n";
   page += "requestData(); setInterval(requestData, 1000);";
   page += "function requestData() {  var xhr = new XMLHttpRequest();  xhr.open('GET', 'sensors');  xhr.onload = function() {    if (xhr.status === 200 && xhr.responseText) {  var data = JSON.parse(xhr.responseText);";
   page += "   document.getElementById(\"lum\").innerText = data.lum; document.getElementById(\"t\").innerText = data.t; document.getElementById(\"h\").innerText = data.h; document.getElementById(\"pres\").innerText = data.pres; document.getElementById(\"alt\").innerText = data.alt; document.getElementById(\"rssi\").innerText = data.rssi; }";
   page += "};  xhr.send();}\r\n";
   page += "</script>\r\n";
   server.send(200, "text/html", page);
});
 
 server.begin();
 Serial.println("Web server started!");
}

void loop() {
  t = bme.readTemperature();
  h = bme.readHumidity();
  pres = bme.readPressure() / 100.0F;
  alt = bme.readAltitude(SEALEVELPRESSURE_HPA);
  lum = analogRead(0);
  rssi = WiFi.RSSI();
  valuePir = digitalRead(pinoPir);
  
  if (valuePir == 1 && lum <300) 
    {switchLight();}  
  /*
  if (valuePir == 0 && lum>300 && lum<450 &&(ntp.getHours()<5 || ntp.getHours()>17))
    {switchLight();}
*/
  if(valuePir == 1)
    {ledPir.on();}
  else
    {ledPir.off();}
  Blynk.virtualWrite(V0, t);
  Blynk.virtualWrite(V1, h);
  Blynk.virtualWrite(V2, pres);
  Blynk.virtualWrite(V3, alt);
  Blynk.virtualWrite(V4, rssi);
  Blynk.virtualWrite(V5, lum);
  Blynk.virtualWrite(V6, valuePir);
  Blynk.run();
  server.handleClient();
  ArduinoOTA.handle();
}

void handleGenericArgs() { //Handler

  for (int i = 0; i < server.args(); i++) {
  
    if (server.argName(i) == "command")
    {
      if (server.arg(i)[0] == 'e')
      {
        txt = server.arg(i+1);
        }
       selectMethod(server.arg(i)[0]);
      }
      txt = 'z';
    } 
  server.send(200, "text/plain", "Comando enviado com sucesso");          //Returns the HTTP response
}

void enterSequence()
{
  for (int i = 0; i < txt.indexOf("/"); i++)
  {
    selectMethod(txt[i]);
  }
}

void switchLight() { 
  emissorIR.sendNEC(0xFF02FD, 32);
  delay(200);
  if (abs(lum - analogRead(0)) <10)
  {
    emissorIR.sendNEC(0xFF9867, 32);
    }
}

void selectMethod(char met)
{
  digitalWrite(LED_BUILTIN, LOW);

  switch (met) {
    case 'c':
      emissorIR.sendNEC(0x8E7807F, 32);
      Serial.println("Power Caixa de Som");
      delay(tempoTecla);
      break;

    case 'b':
      emissorIR.sendNEC(0x8E750AF, 32);
      Serial.println("bluetooth caixa de som");
      delay(tempoTecla);
      break;
    case 'l':
      emissorIR.sendNEC(0x8E7A857, 32);
      Serial.println("linha caixa de som");
      delay(tempoTecla);
      break;
    case '+':
      emissorIR.sendNEC(0x8E7906F, 32);
      Serial.println("volume + caixa de som");
      delay(tempoTecla);
      break;

    case '-':
      emissorIR.sendNEC(0x8E730CF, 32);
      Serial.println("volume- caixa de som");
      delay(tempoTecla);
      break;

    case 't':
      emissorIR.sendNEC(0x20DF10EF, 32);
      Serial.println("Power TV");
      delay(tempoTecla);
      break;

    case 'n':
      emissorIR.sendNEC(0xE17A48B7, 32);
      Serial.println("power net");
      delay(tempoTecla);
      break;

    case '1':
      emissorIR.sendNEC(0xE17A807F, 32);
      Serial.println("1");
      delay(tempoTecla);
      break;
    case '2':
      emissorIR.sendNEC(0xE17A40BF, 32);
      Serial.println("2");
      delay(tempoTecla);
      break;

    case '3':
      emissorIR.sendNEC(0xE17AC03F, 32);
      Serial.println("3");
      delay(tempoTecla);
      break;

    case '4':
      emissorIR.sendNEC(0xE17A20DF, 32);
      Serial.println("4");
      delay(tempoTecla);
      break;
    case '5':
      emissorIR.sendNEC(0xE17AA05F, 32);
      Serial.println("5");
      delay(tempoTecla);
      break;
    case '6':
      emissorIR.sendNEC(0xE17A609F, 32);
      Serial.println("6");
      delay(tempoTecla);
      break;
    case '7':
      emissorIR.sendNEC(0xE17AE01F, 32);
      Serial.println("7");
      delay(tempoTecla);
      break;
    case '8':
      emissorIR.sendNEC(0xE17A10EF, 32);
      Serial.println("8");
      delay(tempoTecla);
      break;
    case '9':
      emissorIR.sendNEC(0xE17A906F, 32);
      Serial.println("9");
      delay(tempoTecla);
      break;
    case '0':
      emissorIR.sendNEC(0xE17A00FF, 32);
      Serial.println("0");
      delay(tempoTecla);
      break;
    case '>':
      emissorIR.sendNEC(0xE17AB04F, 32);
      Serial.println("+ volume net");
      delay(tempoTecla);
      break;
    case '<':
      emissorIR.sendNEC(0xE17A708F, 32);
      Serial.println("- volume net");
      delay(tempoTecla);
      break;
    case 's':
      emissorIR.sendNEC(0x20DF1EE1, 32);
      Serial.println("SearchTv");
      delay(tempoTecla);
      break;
    case 'a':
      switchLight();
      Serial.println("switch luz");
      delay(tempoTecla);
      break;
    case 'p':
      emissorIR.sendNEC(0xE17A7887, 32);
      Serial.println("Programação NET");
      delay(tempoTecla);
      break;
    case 'v':
      emissorIR.sendNEC(0xE17A8877, 32);
      Serial.println("Voltar NET");
      delay(tempoTecla);
      break;
    case 'e':
      enterSequence();
  }
  digitalWrite(LED_BUILTIN, HIGH);
}
