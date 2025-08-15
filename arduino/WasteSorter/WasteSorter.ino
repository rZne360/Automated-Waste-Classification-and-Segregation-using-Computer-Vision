#include <Servo.h>

Servo binServo;  // MG995 (bin rotation)
Servo wiper;     // SG90 (pusher)

const int BIN_SERVO_PIN = 9;
const int WIPER_SERVO_PIN = 4;
const int KY036_DIG = 2;   // digital pin from KY-036
const int KY036_AO  = A0;  // optional analog read

// Positions for 3-bin drum (adjust to your geometry)
const int POS_PAPER   = 0;
const int POS_PLASTIC = 90;
const int POS_METAL   = 180;

const int WIPER_PUSH = 45;
const int WIPER_HOME = 0;

const unsigned long ROTATE_DELAY_MS = 2000;
const unsigned long PUSH_DELAY_MS   = 1500;

void setup() {
  Serial.begin(9600);
  pinMode(KY036_DIG, INPUT);
  binServo.attach(BIN_SERVO_PIN);
  wiper.attach(WIPER_SERVO_PIN);

  // Home position
  binServo.write(POS_PAPER);
  wiper.write(WIPER_HOME);

  Serial.println("Ready: '1'=paper, '2'=plastic, '3'=metal, '0'=idle.");
}

void loop() {
  // Hardware override from KY-036: treat as '3' (metal)
  if (digitalRead(KY036_DIG) == HIGH) {
    actuateFor('3');
  }

  if (Serial.available() > 0) {
    char c = Serial.read();
    if (c=='0' || c=='1' || c=='2' || c=='3') {
      actuateFor(c);
    }
  }
}

void actuateFor(char code) {
  int target = POS_PAPER;
  if (code=='1') target = POS_PAPER;
  else if (code=='2') target = POS_PLASTIC;
  else if (code=='3') target = POS_METAL;
  else if (code=='0') { wiper.write(WIPER_HOME); return; }

  binServo.write(target);
  delay(ROTATE_DELAY_MS);
  wiper.write(WIPER_PUSH);
  delay(PUSH_DELAY_MS);
  wiper.write(WIPER_HOME);
}
