#include <ESP8266WiFi.h>
#include <U8g2lib.h>

U8G2_SSD1306_128X64_NONAME_F_HW_I2C u8g2(U8G2_R0, U8X8_PIN_NONE);
const char *ssid = "2.4G-5A20";
const char *password = "chen8888";
WiFiServer server(8266);

String line;

void setup()
{
    Serial.begin(115200);
    delay(10);
    pinMode(LED_BUILTIN, OUTPUT);
    digitalWrite(LED_BUILTIN, 1);
    WiFi.begin(ssid, password);

    u8g2.begin();
    u8g2.enableUTF8Print();
    //https://github.com/larryli/u8g2_wqy
    u8g2.setFont(u8g2_font_wqy12_t_gb2312b);//设置字体
    u8g2.setFontPosTop();
    u8g2.clearDisplay();
    
    u8g2.setCursor(10, 30); //设置光标处
    u8g2.print("Connecting"); //输出内容
    while(WiFi.status() != WL_CONNECTED)
    {
      delay(500);
      Serial.print(".");
      
      u8g2.print(".");
      u8g2.sendBuffer();
    }
    
   server.begin();
   Serial.printf("Web server started, open %s in a web browser\n", WiFi.localIP().toString().c_str());
 
}
 
void loop()
{
   WiFiClient client = server.available();
   if (client)
   {
      Serial.println("\n[Client connected]");
      while (client.connected())
      {
    
          if (client.available())
          {
              //能够接受到数据，但显示内容、字体大小还未解决
              line = client.readStringUntil('\r');
              Serial.print(line);

              u8g2.clearDisplay();
              u8g2.setCursor(0, 30); //设置光标处
              u8g2.print(line); //输出内容
              u8g2.sendBuffer();//发送          
          }
      }  
   }

}
