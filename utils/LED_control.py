import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
L_LED = 11
R_IR = 12
L_IR = 16
R_LED = 35


def open_LED(pin, dim=False):
  GPIO.setup(pin, GPIO.OUT)
  if dim:
    # not work! 
    pwm = GPIO.PWM(pin, 100)
    pwm.start(pin, 100 * dim)
  else:
    GPIO.output(pin, GPIO.HIGH)
  return pin

def close_LED(pin, sleep_t=0):
  sleep(sleep_t)
  GPIO.setup(pin, GPIO.OUT)
  GPIO.output(pin, GPIO.LOW)
  return pin


class light_control: 
  def __init__(self, 
               IR_dim=False, LED_dim=False, 
               LED_duration=0.5, LED_intervention=2,
               repeat_n=3):
    self.IR_dim = IR_dim
    self.LED_dim = LED_dim
    self.LED_duration = LED_duration
    self.LED_intervention = LED_intervention
    self.repeat = repeat_n
    self.wait_time = (LED_duration + LED_intervention) * 2 * repeat_n
    
  def LED_run(self):
      for i in range(self.repeat):
        for d in [L_LED, R_LED]:
          close_LED(open_LED(d, dim=self.LED_dim), sleep_t=self.LED_duration)
          sleep(self.LED_intervention)
  
  def clean_up(self):
      for d in [L_LED, R_LED]:
        close_LED(d)

  def IR_open(self):
    open_LED(L_IR, dim=self.IR_dim)
    open_LED(R_IR, dim=self.IR_dim)

  def IR_close(self):
    close_LED(L_IR)
    close_LED(R_IR)
