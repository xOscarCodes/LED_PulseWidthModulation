import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

TRIG = 16
ECHO = 18
LED = 32

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT)
led_pwm = GPIO.PWM(LED, 1000)   # Creating pwm object 
led_pwm.start(0)                # Starting the pwm duty cycle at 0 which means the led will not glow now

GPIO.output(TRIG, False)
time.sleep(1)

def calculate_distance():
    """
    This function calculates the distance of the object form the sensor by sending a
    pulse.
    :return: distance from sensor in cm
    """
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    # Calculating the time taken by the pulse to reflect back
    pulse_duration = pulse_end - pulse_start

    """ The speed of sound in air 343 m/s which is 34300 cm/s
    Distance from the object = (Time taken to travel to object and reflect back * speed of sound in air) / 2
    """
    distance = (pulse_duration * 34300) / 2

    time.sleep(0.1)
    return distance


try:
    while True:
        # We have the distance of the object from the calculate_distance() function
        distance = calculate_distance()

        print(distance)

        if distance > 50:               # if the distance is greater than 50cm the led will not glow
            GPIO.output(LED, GPIO.LOW)
        elif distance < 50:             # else if the distance is smaller than 50cm the led will gradually glow as the object comes close.
            led_pwm.ChangeDutyCycle(50 - distance)
        else:
            GPIO.output(LED, GPIO.LOW)

except KeyboardInterrupt:
    GPIO.cleanup()
