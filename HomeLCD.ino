#include <RTClib.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <DHT.h>

dht DHT;
RTC_DS1307 rtc;
LiquidCrystal_I2C lcd(0x27, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

#define DHT11_PIN 2

void setup() {
  Serial.begin(9600);
  lcd.begin(16, 2);
  rtc.begin();
  if (! rtc.isrunning()) {
    rtc.adjust(DateTime(__DATE__,__TIME__));
  }
}

void loop() {
  // Get data from sensor
  int chk = DHT.read11(DHT11_PIN);
  float temp = (((DHT.temperature) * 1.8) + 32);
  float humid = DHT.humidity;
  DateTime curtime = rtc.now();

  // Output to lcd screen
  lcd.setCursor(0, 0)
  lcd.print("Temp: " + String(temp));
  lcd.setCursor(0, 1);
  lcd.print("%02d:%02d:%02d", now.hour(), now.minute(), now.second());
  Serial.print(String(temp) + "|" + String(humid) + "\n");
  delay(10000);
}
