#include <ESP8266WiFi.h>//Biblioteca que gerencia o WiFi.
#include <WiFiServer.h>
#include <ESP8266mDNS.h>
#include <WiFiUdp.h>
#include <ESP8266WebServer.h>
#include <ArduinoOTA.h>
#include "DHT.h"
#include <Arduino.h>
#include <IRremoteESP8266.h>
#include <IRsend.h>

const uint16_t kIrLed = 4;  // ESP8266 GPIO pin to use. Recommended: 4 (D2).
IRsend emissorIR(kIrLed);  // Set the GPIO to be used to sending the message.

char command;
String txt;
const char* ssid = "DORETOALENCAR";
const char* password = "16043028";
#define tempoTecla 350
String tecla;
String req;

#define DHTPIN 5 // pino que estamos conectado
#define DHTTYPE DHT11 // DHT 11
ESP8266WebServer server(80);
WiFiClient cliente;

String page = "";
String text = "";
float h;
float t;
DHT dht(DHTPIN, DHTTYPE);

int pinoPir = 16;
//Inicia o sensor em estado 0, ou seja desligado.
int valuePir;
int valorSensor = 0;
int stateLight = 1;
int lampoff = 0;
//Variável para calibração do sensor
int calibracao = 15;

int s;


int ldr = 0; //Setando a utilizaçâo do LDR à porta ADC A0 do Nodemcu
int lum = 0;//variável para armazenar a leitura do ldr.
int controligh = 650;

signed long rssi = WiFi.RSSI();

void setup(void) {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  emissorIR.begin();
  dht.begin();
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
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

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
  Serial.println("Pronto");
  Serial.print("Endereco IP: ");
  Serial.println(WiFi.localIP());

server.on("/lum.txt", [](){
   text = (String)lum;
  server.send(200, "text/html", text);
 });
  server.on("/t.txt", [](){
   text = (String)t;
  server.send(200, "text/html", text);
 });
   server.on("/h.txt", [](){
   text = (String)h;
  server.send(200, "text/html", text);
 });
   server.on("/rssi.txt", [](){
   text = (String)rssi;
  server.send(200, "text/html", text);
 });
 server.on ("/genericArgs", handleGenericArgs); // Associe a função do manipulador ao caminho
 server.on("/", [](){
   page = "<!DOCTYPE html><html><head><title>Painel Sensores</title>";//Identificaçao e Titulo.
   page += "<style>h2{font-size:24px;color:black;}h3{font-size:18px;color:black;}</style></head>";//Cria uma nova fonte de tamanho e cor X.
   page += "<body bgcolor='#FFFAFA'><center>";//Cor do Background
   page += "<h2>SENSORES EM FUNCIONAMENTO</h2>";
   page += "<h3>Luminosidade:</h3> <h3 id=\"lum\">""</h3>\r\n";
   page += "<h3>Temperatura:</h3> <h3 id=\"t\">""</h3>";
   page += "<h3>Umidade:</h3> <h3 id=\"h\">""</h3>";
   page += "<h3>Intens. do Sinal:</h3> <h3 id=\"rssi\">""</h3>";
   page += "<script>\r\n";
   page += "var x = setInterval(function() {loadLum(\"lum.txt\",updateLum),loadT(\"t.txt\",updateT),loadH(\"h.txt\",updateH),loadRssi(\"rssi.txt\",updateRssi)}, 0);\r\n";
   page += "function loadLum(url, callback){\r\n";
   page += "var xhttp = new XMLHttpRequest();\r\n";
   page += "xhttp.onreadystatechange = function(){\r\n";
   page += " if(this.readyState == 4 && this.status == 200){\r\n";
   page += " callback.apply(xhttp);\r\n";
   page += " }\r\n";
   page += "};\r\n";
   page += "xhttp.open(\"GET\", url, true);\r\n";
   page += "xhttp.send();\r\n";
   page += "}\r\n";
   page += "function updateLum(){\r\n";
   page += " document.getElementById(\"lum\").innerHTML = this.responseText;\r\n";
   page += "}\r\n";
   page += "function loadT(url, callback){\r\n";
   page += "var xhttp = new XMLHttpRequest();\r\n";
   page += "xhttp.onreadystatechange = function(){\r\n";
   page += " if(this.readyState == 4 && this.status == 200){\r\n";
   page += " callback.apply(xhttp);\r\n";
   page += " }\r\n";
   page += "};\r\n";
   page += "xhttp.open(\"GET\", url, true);\r\n";
   page += "xhttp.send();\r\n";
   page += "}\r\n";
   page += "function updateT(){\r\n";
   page += " document.getElementById(\"t\").innerHTML = this.responseText;\r\n";
   page += "}\r\n";
   page += "function loadH(url, callback){\r\n";
   page += "var xhttp = new XMLHttpRequest();\r\n";
   page += "xhttp.onreadystatechange = function(){\r\n";
   page += " if(this.readyState == 4 && this.status == 200){\r\n";
   page += " callback.apply(xhttp);\r\n";
   page += " }\r\n";
   page += "};\r\n";
   page += "xhttp.open(\"GET\", url, true);\r\n";
   page += "xhttp.send();\r\n";
   page += "}\r\n";
   page += "function updateH(){\r\n";
   page += " document.getElementById(\"h\").innerHTML = this.responseText;\r\n";
   page += "}\r\n";
   page += "function loadRssi(url, callback){\r\n";
   page += "var xhttp = new XMLHttpRequest();\r\n";
   page += "xhttp.onreadystatechange = function(){\r\n";
   page += " if(this.readyState == 4 && this.status == 200){\r\n";
   page += " callback.apply(xhttp);\r\n";
   page += " }\r\n";
   page += "};\r\n";
   page += "xhttp.open(\"GET\", url, true);\r\n";
   page += "xhttp.send();\r\n";
   page += "}\r\n";
   page += "function updateRssi(){\r\n";
   page += " document.getElementById(\"rssi\").innerHTML = this.responseText;\r\n";
   page += "}\r\n";
   page += "</script>\r\n";
   server.send(200, "text/html", page);
});
 
 server.begin();
 Serial.println("Web server started!");
}

void loop() {
  char c = Serial.read();
  delay(500);
  h = dht.readHumidity();
  t = dht.readTemperature();
  lum = analogRead(0);
  rssi = WiFi.RSSI();
  valuePir = digitalRead(pinoPir);
  /*Serial.println(lum);
  Serial.println(h);
  Serial.println(t);
  

  Serial.print("Valor do Sensor PIR: ");
  Serial.println(valuePir);
if(valuePir == 1)
{digitalWrite(LED_BUILTIN, HIGH);}
else
{
  digitalWrite(LED_BUILTIN, LOW);
  }
  ////Verificando se ocorreu detecção de movimentos
  if (valuePir == 1 && lum < controligh) {
    light_on();
  } else if (valuePir == 0 || lum > controligh) {
    light_off();
  }
  */
  char i = Serial.read();
  selectMethod(i);
   server.handleClient();
  ArduinoOTA.handle();
  Serial.print(server.args());
}

void handleGenericArgs() { //Handler

String message = "Number of args received:";
message += server.args();            //Get number of parameters
message += "\n";                            //Add a new line

for (int i = 0; i < server.args(); i++) {

message += "Arg nº" + (String)i + " –> ";   //Include the current iteration value
message += server.argName(i) + ": ";     //Get the name of the parameter
message += server.arg(i) + "\n";              //Get the value of the parameter
Serial.println(server.arg(i)[0]);

if (server.argName(i) == "command")
{
  if (server.arg(i)[0] == 'e')
  {
    txt = server.arg(i+1);
    }
   selectMethod(server.arg(i)[0]);
  }
  txt = 'v';
} 
server.send(200, "text/plain", "Comando enviado com sucesso");          //Returns the HTTP response
}
char getcommand()
{
  if (req.indexOf("=") > 0)
  {
    return req[req.indexOf("=") + 1];
  }
  else
  {
    return 'z';
  }
}
void enterSequence()
{
  for (int i = 0; i < txt.indexOf("/"); i++)
  {
    selectMethod(txt[i]);
    delay(tempoTecla);
  }
}

void light_on() {  //Função que ativa o alarme - Detectou presença, o LED Vermelho fica acende
  //E o LED VERDE apaga.
  lampoff = 0;
  if (stateLight == 0)
  {
    selectMethod('a');
    stateLight = 1;

    
  }
}
void light_off() { //Função que desativa o alarme - N foi detectado presença, o LED Vermelho apaga
  //E o LED VERDE acende.
  lampoff = lampoff + 1;
  if ((lampoff == 30 || lum > controligh) && (stateLight == 1))
  {
    selectMethod('f');
    lampoff = 0;
    stateLight = 0;
  }
}

void selectMethod(char met)
{
  digitalWrite(LED_BUILTIN, HIGH);

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
      emissorIR.sendNEC(0xFF02FD, 32);
      Serial.println("acende a luz");
      delay(tempoTecla);
      break;
    case 'f':
      emissorIR.sendNEC(0xFF9867, 32);
      Serial.println("apaga a luz");
      delay(tempoTecla);
      break;
    case 'e':
      enterSequence();
  }
  digitalWrite(LED_BUILTIN, LOW);
}
