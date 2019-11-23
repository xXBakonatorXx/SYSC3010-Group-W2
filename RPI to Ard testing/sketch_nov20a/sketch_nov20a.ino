//Sample message text
String data="ayylmao";
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(data);
  delay(2000);
}
