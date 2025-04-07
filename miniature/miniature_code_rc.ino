// YouTube | Tech at Home

// RC input channels
double ch1 = 0;
double ch2 = 0;

// Motor A (Left)
int IN1 = 4;
int IN2 = 5;
int ENA = 9;

// Motor B (Right)
int IN3 = 6;
int IN4 = 7;
int ENB = 10;

void setup() {
  Serial.begin(9600);

  // RC input pins
  pinMode(2, INPUT);  // CH1
  pinMode(3, INPUT);  // CH2

  // Motor control pins
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENA, OUTPUT);

  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);
  pinMode(ENB, OUTPUT);
}

void loop() {
  // Read PWM input from RC receiver
  ch1 = pulseIn(2, HIGH);
  ch2 = pulseIn(3, HIGH);

  // Print channel values
  Serial.print("CH1: ");
  Serial.print(ch1);
  Serial.print("   CH2: ");
  Serial.println(ch2);

  // Set motor speed (0 to 255)
  int speed = 200; // you can adjust this

  analogWrite(ENA, speed); // Enable left motor
  analogWrite(ENB, speed); // Enable right motor

  // Control logic
  if ((ch1 == 0) && (ch2 == 0)) {
    stopMotors();
  }
  else if ((ch1 > 1530) && (ch2 > 1530)) {
    // Forward
    forward();
  }
  else if ((ch1 > 1530) && (ch2 < 1460)) {
    // Right turn
    turnRight();
  }
  else if ((ch1 < 1460) && (ch2 > 1530)) {
    // Left turn
    turnLeft();
  }
  else if ((ch1 < 1460) && (ch2 < 1460)) {
    // Reverse
    reverse();
  }
  else {
    stopMotors();
  }

  delay(100); // for serial monitor readability
}

void forward() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void reverse() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void turnLeft() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
}

void turnRight() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
}

void stopMotors() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
}