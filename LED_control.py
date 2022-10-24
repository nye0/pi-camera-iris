import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
L_LED = 11
LR_IR = 12
R_LED = 35


def open_LED(pin, dim=False):
  GPIO.setup(pin, GPIO.OUT)
  if dim:
    pwm = GPIO.PWM(pin, 100)
    pwm.start(100 * dim)
  else:
    GPIO.output(pin, GPIO.HIGH)
  return pin

def close_LED(pin, sleep_t=0):
  sleep(sleep_t)
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)
  return pin


def control(start_key, 
            IR_dim=1, LED_dim=1, 
            LED_duration=0.5, LED_intervention=2,
            repeat=3):
  total_t = (LED_duration + LED_intervention) * 2 * repeat
  if start_key:
    open_LED(LR_IR, dim=IR_dim)
    for i in range(repeat):
      for d in [L_LED, R_LED]:
        close_LED(open_LED(d, dim=LED_dim), sleep_t=LED_duration)
        sleep(LED_intervention)
    close_LED(LR_IR)
   return total_t
