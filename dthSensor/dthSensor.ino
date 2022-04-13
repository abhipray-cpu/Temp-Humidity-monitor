#include<ESP8266WiFi.h>
#include<FirebaseESP8266.h>
#include "DHT.h"        // including the library of DHT11 temperature and humidity sensor
#define DHTTYPE DHT11   // DHT 11

#define WIFI_SSID "Heavy Driver"
#define WIFI_PASSWORD "maakabhosda"
#define FIREBASE_AUTH "J7zZWSjFYt1VW2h3Y6SgGz8JW7okCe1qrYYEnEe0"
#define FIREBASE_HOST "channel-relay-control-3a865-default-rtdb.asia-southeast1.firebasedatabase.app/"
#define dht_dpin 12
DHT dht(dht_dpin, DHTTYPE); 
FirebaseData firebaseData;
FirebaseJson json;
FirebaseData fbdo;
void setup(void)
{ 
  dht.begin();
  Serial.begin(115200);
  WiFi.begin(WIFI_SSID,WIFI_PASSWORD);
  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(300);
  }
   Serial.println();
   Serial.print("Connected with IP: ");
   Serial.println(WiFi.localIP());
   Serial.println(); 
   Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
   Serial.println("Humidity and temperature\n\n");
  delay(700);

}
void loop() { 
    float h = dht.readHumidity();
    float t = dht.readTemperature();         
    // Read temperature as Fahrenheit
  float f = dht.readTemperature(true);
   // Compute heat index
  // Must send in temp in Fahrenheit!
  float hi = dht.computeHeatIndex(f, h);
  float hiDegC = dht.convertFtoC(hi);
  double dew=dewPoint(t, h);
  Serial.print("Humidity: ");
  Serial.println(h);
  Serial.print(" %\t");
  Serial.print("Temperature: ");
  Serial.println(t);
  Serial.print(" *C ");
  Serial.println(f);
  Serial.print(" *F\t");
  Serial.print("Heat index: ");
  Serial.println(hiDegC);
  Serial.print(" *C ");
  Serial.println(hi);
  Serial.print(" *F ");
  Serial.print("Dew Point (*C): ");
  Serial.println(dewPoint(t, h));
 
  writeData(h,t,f,hiDegC,hi,dew);
}
//float h,float t,float f,float hi,float hicC,doubleDew
void writeData(float humidity,float tempC,float tempF,float heatIndexC,float heatIndexF,double dewPoint){
  //writing humidity value to firebase
     if(Firebase.setFloat(fbdo, F("/values/humidity"),humidity))
     {
      Serial.println("Updated humidity successfully");
      }
      else
      {
        Serial.println("Failed to update data");
        Serial.println(fbdo.errorReason().c_str());
        }

   //writing tempearature celsius value to firebase
     if(Firebase.setFloat(fbdo, F("/values/tempC"),tempC))
     {
      Serial.println("Updated farhenite celsius successfully");
      }
      else
      {
        Serial.println("Failed to update data");
        Serial.println(fbdo.errorReason().c_str());
        }

    //writing tempeature farhenite value to firebase
     if(Firebase.setFloat(fbdo, F("/values/tempF"),tempF))
     {
      Serial.println("Updated temperature farhenite successfully");
      }
      else
      {
        Serial.println("Failed to update data");
        Serial.println(fbdo.errorReason().c_str());
        }

    //writing humdity index celsius  value to firebase
     if(Firebase.setFloat(fbdo, F("/values/heatIndexC"),heatIndexC))
     {
      Serial.println("Updated heat index (celsius) successfully");
      }
      else
      {
        Serial.println("Failed to update data");
        Serial.println(fbdo.errorReason().c_str());
        }


    //writing humdity index farhenite  value to firebase
     if(Firebase.setFloat(fbdo, F("/values/heatIndexF"),heatIndexF))
     {
      Serial.println("Updated heat index(Farhenite) successfully");
      }
      else
      {
        Serial.println("Failed to update data");
        Serial.println(fbdo.errorReason().c_str());
        }

     //writing dew point  value to firebase
     if(Firebase.setFloat(fbdo, F("/values/dewPoint"),dewPoint))
     {
      Serial.println("Updated dew point successfully");
      }
      else
      {
        Serial.println("Failed to update data");
        Serial.println(fbdo.errorReason().c_str());
        }
  }
double dewPoint(double celsius, double humidity)
{
  // (1) Saturation Vapor Pressure = ESGG(T)
  double RATIO = 373.15 / (273.15 + celsius);
  double RHS = -7.90298 * (RATIO - 1);
  RHS += 5.02808 * log10(RATIO);
  RHS += -1.3816e-7 * (pow(10, (11.344 * (1 - 1 / RATIO ))) - 1) ;
  RHS += 8.1328e-3 * (pow(10, (-3.49149 * (RATIO - 1))) - 1) ;
  RHS += log10(1013.246);

  // factor -3 is to adjust units - Vapor Pressure SVP * humidity
  double VP = pow(10, RHS - 3) * humidity;

  // (2) DEWPOINT = F(Vapor Pressure)
  double T = log(VP / 0.61078); // temp var
  return (241.88 * T) / (17.558 - T);
}
