#include <SoftwareSerial.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

SoftwareSerial mySerial(6, 3);  // RX, TX

int DE = 4;
int RE = 5;

unsigned long startTime = 0;

#define SCREEN_WIDTH 128    // OLED display width, in pixels
#define SCREEN_HEIGHT 64    // OLED display height, in pixels
#define OLED_RESET -1       // Reset pin # (or -1 if sharing Arduino reset pin)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
  Serial.begin(9600);
  mySerial.begin(9600);
  pinMode(DE, OUTPUT);
  pinMode(RE, OUTPUT);
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);

  display.begin(SSD1306_SWITCHCAPVCC, 0x3C); //initialize with the I2C addr 0x3C (128x64)
  delay(500);
  display.clearDisplay();
  display.setCursor(25, 15);
  display.setTextSize(1);
  display.setTextColor(WHITE);
  display.println(" NPK Sensor");
  display.setCursor(25, 35);
  display.setTextSize(1);
  display.print("Initializing");
  display.display();
  delay(3000);
}

void loop() {
  if (millis() - startTime < 30000) { // Wait for 30 seconds
    return;
  }

  byte queryDataNitro[] = {0x01, 0x03, 0x00, 0x1E, 0x00, 0x01, 0xE4, 0x0C};
  byte queryDataPhos[] = {0x01, 0x03, 0x00, 0x1F, 0x00, 0x01, 0xB5, 0xCC};
  byte queryDataPota[] = {0x01, 0x03, 0x00, 0x20, 0x00, 0x01, 0x85, 0xC0};

  byte receivedData[7];  // Adjust the size based on the expected response

  // Query Nitrogen
  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  mySerial.write(queryDataNitro, sizeof(queryDataNitro));
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);

  delay(500);  // Add a delay to allow the sensor to process the request

  unsigned int nitrogen = 0;
  if (mySerial.available() >= sizeof(receivedData)) {
    mySerial.readBytes(receivedData, sizeof(receivedData));

    // Parse the received Nitrogen value
    nitrogen = (receivedData[3] << 8) | receivedData[4];
  }

  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  mySerial.write(queryDataPhos, sizeof(queryDataPhos));
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);

  delay(500);  // Add a delay to allow the sensor to process the request

  unsigned int phosphorus = 0;
  if (mySerial.available() >= sizeof(receivedData)) {
    mySerial.readBytes(receivedData, sizeof(receivedData));

    // Parse the received Phosphorus value
    phosphorus = (receivedData[3] << 8) | receivedData[4];
  }

  digitalWrite(DE, HIGH);
  digitalWrite(RE, HIGH);
  mySerial.write(queryDataPota, sizeof(queryDataPota));
  digitalWrite(DE, LOW);
  digitalWrite(RE, LOW);

  delay(500);  // Add a delay to allow the sensor to process the request

  unsigned int potassium = 0;
  if (mySerial.available() >= sizeof(receivedData)) {
    mySerial.readBytes(receivedData, sizeof(receivedData));

    // Parse the received Potassium value
    potassium = (receivedData[3] << 8) | receivedData[4];
  }

  // Print NPK values
  Serial.print(nitrogen);
  Serial.print(", ");
  Serial.print(phosphorus);
  Serial.print(", ");
  Serial.println(potassium);

  // Display NPK values on OLED
  display.clearDisplay();
  display.setTextSize(1);      
  display.setTextColor(SSD1306_WHITE);  
  display.setCursor(0,5);     
  display.print("Nitrogen: ");
  display.println(nitrogen);
  display.setCursor(0,25);     
  display.print("Phosphorus: ");
  display.println(phosphorus);
  display.setCursor(0,45);     
  display.print("Potassium: ");
  display.println(potassium);
  display.display();

  // Reset timer
  startTime = millis();
}