#include <WiFi.h>
#include <AsyncTCP.h>
#include <ESPAsyncWebServer.h>

const char* ssid = "id_wifi";
const char* password = "psw_wifi";

const int ledPin = 32; // Pin led udoo
AsyncWebServer server(80);

void setup() {
  Serial.begin(115200);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW); // Low start

  // Connessione alla rete Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to the Wi-Fi network...");
  }

  Serial.println("Connected to the Wi-Fi network!");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

  // Config rout to manage HTTP requests
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(200, "text/html", generateHtmlPage());
  });

  server.on("/turn_on", HTTP_GET, [](AsyncWebServerRequest *request){
    digitalWrite(ledPin, HIGH); // turn_on il LED
    request->send(200, "text/plain", "LED ON");
  });

  server.on("/turn_off", HTTP_GET, [](AsyncWebServerRequest *request){
    digitalWrite(ledPin, LOW); // turn_off il LED
    request->send(200, "text/plain", "LED OFF");
  });

  server.begin();
  Serial.println("Server avviato!");
}

void loop() {
  // Other 
}

String generateHtmlPage() {
  String htmlPage = "<!DOCTYPE html>\n";
  htmlPage += "<html>\n";
  htmlPage += "<head><title>Control LED</title></head>\n";
  htmlPage += "<body>\n";
  htmlPage += "<h1>Controllo LED</h1>\n";
  htmlPage += "<button onclick=\"turn_on_Led()\">Turn on LED</button>\n";
  htmlPage += "<button onclick=\"turn_off_Led()\">Turn off LED</button>\n";
  htmlPage += "<script>\n";
  htmlPage += "function turn_on_Led() {\n";
  htmlPage += "  fetch('/turn_on')\n";
  htmlPage += "    .then(response => console.log('LED ON'))\n";
  htmlPage += "    .catch(error => console.error('Error turn on LED:', error));\n";
  htmlPage += "}\n";
  htmlPage += "function turn_off_Led() {\n";
  htmlPage += "  fetch('/turn_off')\n";
  htmlPage += "    .then(response => console.log('LED OFF'))\n";
  htmlPage += "    .catch(error => console.error('Error turn off LED:', error));\n";
  htmlPage += "}\n";
  htmlPage += "</script>\n";
  htmlPage += "</body>\n";
  htmlPage += "</html>\n";

  return htmlPage;
}
