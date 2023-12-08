
// Arduino Nano
//#define PWMPin 9
//#define directionPin1 6 // in2
//#define directionPin2 7 // in1

//#define encoder0PinA 3 // c2      
//#define encoder0PinB 2 // c1    

// ESP-32
#define PWMPinA 21
#define PWMPinB 26

#define directionPin1 19  // in2
#define directionPin2 18  // in1

#define directionPin3 13  // in2
#define directionPin4 12  // in1

#define encoder0PinA 23  // c2
#define encoder0PinB 22  // c1

#define encoder0PinC 14  // c2
#define encoder0PinD 27  // c1

unsigned long currentMillis;
unsigned long previousMillis;

volatile long encoder0Pos = 0;    // encoder 1
volatile long encoder1Pos = 0;    // encoder 1

int PWMValue = 0;
int motorDirection = 0;

//Target values - Also called as setpoint!
int targetPosition = 1320; // 1 rotation only -- quadrate encoder cpr = 11 x 4 = 44 and then output shaft cpr = 44 x 30 (gear ratio) = 1320 (This is equivalent to 1320 cpr of encoder to 1 revolution of output shaft)
//int targetPosition = 2640; // 1 rotation only -- quadrate encoder cpr = 11 x 4 = 44 and then output shaft cpr = 44 x 30 (gear ratio) = 2640 x 2 (This is equivalent to 2640 cpr of encoder to 2 revolution of output shaft)

//Measured values
volatile float motorPosition = 0; //position based on the encoder
float previousMotorPosition = -1; //helps to keep track of changes (useful for the display update)

//PID parameters - tuned by the user
float proportional = 1.5; //1.35; //k_p = 0.5
float integral = 0.00005; //k_i = 3
float derivative = 0.01; //k_d = 1
float controlSignal = 0; //u - Also called as process variable (PV)

//PID-related
float previousTime = 0; //for calculating delta t
float previousError = 0; //for calculating the derivative (edot)
float errorIntegral = 0; //integral error
float currentTime = 0; //time in the moment of calculation
float deltaTime = 0; //time difference
float errorValue = 0; //error
float edot = 0; //derivative (de/dt)

//Statuses of the DT and CLK pins on the encoder
int CLKNow;
int CLKPrevious;
int DTNow;
int DTPrevious;

void setup() {
  Serial.begin(57600);
  pinMode(PWMPinA, OUTPUT);
  pinMode(directionPin1, OUTPUT);
  pinMode(directionPin2, OUTPUT);

  pinMode(PWMPinB, OUTPUT);
  pinMode(directionPin3, OUTPUT);
  pinMode(directionPin4, OUTPUT);

  pinMode(encoder0PinA, INPUT_PULLUP);    
  pinMode(encoder0PinB, INPUT_PULLUP);

  pinMode(encoder0PinC, INPUT_PULLUP);    
  pinMode(encoder0PinD, INPUT_PULLUP);
    
  attachInterrupt(digitalPinToInterrupt(encoder0PinA), doEncoderA, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoder0PinB), doEncoderB, CHANGE); 

  attachInterrupt(digitalPinToInterrupt(encoder0PinC), doEncoderC, CHANGE);
  attachInterrupt(digitalPinToInterrupt(encoder0PinD), doEncoderD, CHANGE); 

  //Set initial rotation direction
  digitalWrite(directionPin1, LOW);
  digitalWrite(directionPin2, LOW);

  digitalWrite(directionPin3, LOW);
  digitalWrite(directionPin4, LOW);
}

void loop() {

   calculatedPID();
   driveMotor();

//  currentMillis = millis();   // bookmark the time 
//  if (currentMillis - previousMillis >= 10) {  // start timed loop for everything else
//         previousMillis = currentMillis;
//           Serial.print(encoder0Pos);
//           Serial.print(",");
//           Serial.println(targetPosition);
//  }
}

void driveMotor()
{ 
  // Motor Direction
  if (controlSignal < 0) // negative value: CCW
  {
    motorDirection = -1;
  }

  else if (controlSignal > 0) // positive value: CW
  {
    motorDirection = 1;
  }

  else{ // STOP
    motorDirection = 0;
  }

  // Motor Speed
  PWMValue = (int)fabs(controlSignal); //PWM values cannot be negative and have to be integers
  
  if (PWMValue > 255){
    PWMValue = 255;
  }

  if (PWMValue < 30 && errorValue !=0)
  {
    PWMValue = 30;
  }

   if (motorDirection == -1) //-1 == CCW
  {
    digitalWrite(directionPin1, LOW);
    digitalWrite(directionPin2, HIGH);
    digitalWrite(directionPin3, LOW);
    digitalWrite(directionPin4, HIGH);
  }

   else if (motorDirection == 1) // == 1, CW
  {
    digitalWrite(directionPin1, HIGH);
    digitalWrite(directionPin2, LOW);
    digitalWrite(directionPin3, HIGH);
    digitalWrite(directionPin4, LOW);
  }

   else // == 0, stop/break
  {
    digitalWrite(directionPin1, LOW);
    digitalWrite(directionPin2, LOW);
    digitalWrite(directionPin3, LOW);
    digitalWrite(directionPin4, LOW);
    PWMValue = 0;
  }

  //Then we set the motor speed
  analogWrite(PWMPinA, PWMValue);
  analogWrite(PWMPinB, PWMValue);

  Serial.print(encoder0Pos);
  Serial.print(",");
  Serial.print(encoder1Pos);
  Serial.print(",");
  Serial.print(targetPosition);
  Serial.print(",");
  Serial.print(PWMValue);
  Serial.print(",");
  Serial.print(errorValue);
  Serial.println();
}

void calculatedPID()
{
  //Determining the elapsed time
  currentTime = micros(); //current time
  deltaTime = (currentTime - previousTime) / 1000000.0; //time difference in seconds
  previousTime = currentTime; //save the current time for the next iteration to get the time difference

  errorValue = encoder0Pos - targetPosition; //Current position - target position (or setpoint)
  edot = (errorValue - previousError) / deltaTime; //edot = de/dt - derivative term

  errorIntegral = errorIntegral + (errorValue * deltaTime); //integral term - Newton-Leibniz, notice, this is a running sum!

  controlSignal = (proportional * errorValue) + (derivative * edot) + (integral * errorIntegral); //final sum, proportional term also calculated here

  previousError = errorValue; //save the error for the next iteration to get the difference (for edot)
}

////////////////////////////////////////////////////////////////////////////////////////////////////////
void doEncoderA(){  

  // look for a low-to-high on channel A
  if (digitalRead(encoder0PinA) == HIGH) { 
    // check channel B to see which way encoder is turning
    if (digitalRead(encoder0PinB) == LOW) {  
      encoder0Pos = encoder0Pos + 1; // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1; // CCW
    }
  }
  else   // must be a high-to-low edge on channel A                                       
  { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(encoder0PinB) == HIGH) {   
      encoder0Pos = encoder0Pos + 1; // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1; // CCW
    }
  }
}

void doEncoderB(){  

  // look for a low-to-high on channel B
  if (digitalRead(encoder0PinB) == HIGH) {   
   // check channel A to see which way encoder is turning
    if (digitalRead(encoder0PinA) == HIGH) {  
      encoder0Pos = encoder0Pos + 1; // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1; // CCW
    }
  }
  // Look for a high-to-low on channel B
  else { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(encoder0PinA) == LOW) {   
      encoder0Pos = encoder0Pos + 1; // CW
    } 
    else {
      encoder0Pos = encoder0Pos - 1; // CCW
    }
  }
}

////////////////////////////////////////////////////////////////////////////////////////////////////////
void doEncoderC(){  

  // look for a low-to-high on channel A
  if (digitalRead(encoder0PinC) == HIGH) { 
    // check channel B to see which way encoder is turning
    if (digitalRead(encoder0PinD) == LOW) {  
      encoder1Pos = encoder1Pos + 1; // CW
    } 
    else {
      encoder1Pos = encoder1Pos - 1; // CCW
    }
  }
  else   // must be a high-to-low edge on channel A                                       
  { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(encoder0PinD) == HIGH) {   
      encoder1Pos = encoder1Pos + 1; // CW
    } 
    else {
      encoder1Pos = encoder1Pos - 1; // CCW
    }
  }
}

void doEncoderD(){  

  // look for a low-to-high on channel B
  if (digitalRead(encoder0PinD) == HIGH) {   
   // check channel A to see which way encoder is turning
    if (digitalRead(encoder0PinC) == HIGH) {  
      encoder1Pos = encoder1Pos + 1; // CW
    } 
    else {
      encoder1Pos = encoder1Pos - 1; // CCW
    }
  }
  // Look for a high-to-low on channel B
  else { 
    // check channel B to see which way encoder is turning  
    if (digitalRead(encoder0PinC) == LOW) {   
      encoder1Pos = encoder1Pos + 1; // CW
    } 
    else {
      encoder1Pos = encoder1Pos - 1; // CCW
    }
  }
}
