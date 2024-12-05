// By:  Anjali Punnoose
//      LunaLink Systems
//      Fall 2024
// Program for Serial Communication with RPi to Control 1 Motor to move CW or CCW

// SW5 -> ON
// right dir = LOW
// left dir = HIGH


int pulsePin = 12; // Pulse pin
int dirPin = 11;   // Direction pin

char data;

void setup() {
  Serial.begin(9600);  // Start serial communication at 9600 baud 
  pinMode(pulsePin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, 0);    
}

void loop() {
  if (Serial.available() > 0) {
    String receivedWord = Serial.readStringUntil('\n');  // Read the incoming string until newline character
    receivedWord.trim();  // Trim any extra whitespaces or newlines

    String dir = receivedWord.substring(0,1);
    String stepStr = receivedWord.substring(2);
    int retVal = 0;

    // Step Motor based on Direction
    if (stepStr.length() > 0 && dir.length() > 0) {
      int steps = stepStr.toInt(); // Get steps
      if (dir == "R")
      {
        digitalWrite(dirPin, LOW); // set direction to right
        Serial.print("Right: ");
        Serial.println(steps);  
        retVal = stepMotor(steps);
      }
      else if (dir == "L")
      {
        digitalWrite(dirPin, HIGH); // set direction to left
        Serial.print("Left: ");
        Serial.println(steps);
        retVal = stepMotor(steps);
      }
    }
  
    if (retVal ==0)
      Serial.println("ERROR: Invalid input string format. Proper format: \"[L/R] [step count]\"");
    else
      Serial.println(retVal);
  }

  // Toggle BUILTIN LED to Check Program Running on Arduino
  digitalWrite(LED_BUILTIN, !digitalRead(LED_BUILTIN));     
  delay(1000);  // Small delay to avoid spamming
}


int stepMotor(int steps){
  int pulseDelay = 55; // Adjust this for speed (min val = 55)(lower delay val = higher speed)

  int stepCount=0;
  while(stepCount < steps)
  {
      digitalWrite(pulsePin, HIGH);
      delayMicroseconds(pulseDelay); 
      digitalWrite(pulsePin, LOW);
      delayMicroseconds(pulseDelay);
      Serial.println(stepCount);
      stepCount++;
  }

  return 1;
}
