import time
import board
import busio
import adafruit_vl53l0x

class Sonar():
    def __init__(self) -> None:
        # Initialize I2C bus and sensor.
        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.vl53 = adafruit_vl53l0x.VL53L0X(self.i2c)
        self.vl53.measurement_timing_budget = 200000
        
    def read(self):
        with self.vl53.continuous_mode():
            while True:
                #time.sleep(0.1)
                range = self.vl53.range
                return range
            
if __name__ == "__main__":
    while True:
        main = Sonar()
        value = main.read()
        print(value)

    

                
        
