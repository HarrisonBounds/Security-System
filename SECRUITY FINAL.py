import RPi.GPIO as GPIO
import time
from picamera import PiCamera




def switch_handler(pin):
    global n, nn
    time.sleep(0.01)
    print('EVENT DETECTED!')
    n = n + 1
    if n < n + 1:
        nn = not nn
    else:
        nn = nn

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
BUZZER = 26 #GPIO PIN FOR THE BUZZER
switch_pin = 21 # GPIO pin for the REED SWITCH
GPIO.setup(BUZZER,GPIO.OUT)
GPIO.setup(switch_pin,GPIO.IN,pull_up_down=GPIO.PUD_DOWN) #event detection
GPIO.add_event_detect(switch_pin, GPIO.BOTH, callback=switch_handler, bouncetime=500) #event detection
# set up the buzzer as a PWM object
freq = 4000 # Hertz
my_pwm = GPIO.PWM(BUZZER, freq)



# start the buzzer object
duty_cycle = 100 # percentage, 0% = OFF, 100% = fully ON
my_pwm.start(duty_cycle)

pause_time = 1 # seconds



MATRIX = [
     [1,2,3,'A'],
     [4,5,6,'B'],
     [7,8,9,'C'],
     ['*',0,'#','D']
]

ROW = [4, 17, 27, 22]
COL = [18, 23, 24, 25]

for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)

for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down = GPIO.PUD_UP)
    
#Start with a blank list
userEntry = []
# Define the correct answer
correctKey = [1,2,3,4]

arming = False
camera = PiCamera()
n = 0
nn = True
my_test = False
attempt = 0
counter = 0
try:
    my_pwm.ChangeDutyCycle(0)
    while(True):
        while arming == False:
            if len(userEntry) < len(correctKey) and counter == 0:
                for j in range(4):
                    GPIO.output(COL[j],0)

                    for i in range(4):
                        if GPIO.input(ROW[i]) == 0:
                            #print (MATRIX[i][j])
                            userEntry.append(MATRIX[i][j])
                            print(userEntry)
                            #print('sleeping')
                            time.sleep(0.2)
                            while(GPIO.input(ROW[i]) == 0):
                                #print('passing')
                                pass


                    GPIO.output(COL[j],1)
                    #print('sleeping again')
                    if len(userEntry) == len(correctKey):
                        #If they match, check to see if the value is correct
                        if userEntry == correctKey:
                            print("Correct, system is arming")
                            time.sleep(1)
                            print("system armed!!")
                            print('starting system...')
                            while userEntry == correctKey:
                                print('system monitoring!')
                                if nn == False:
                                    print('door is open')
                                    my_pwm.ChangeDutyCycle(duty_cycle) #turns alarm on
                                    print('alarm is sounding!')
                                    camera.start_preview() ##opens camera display window
                                    time.sleep(2) #delay before taking picture
                                    print('CAPTURING IMAGE OF INTRUDER!')
                                    camera.capture("intruder_TEST_image.jpg") #saves image
                                    time.sleep(1)
                                    camera.stop_preview() #closes camera window
                                    time.sleep(0.03)
                                else:
                                    print('door is closed')
                                    my_pwm.ChangeDutyCycle(0) #turns the alarm off
                                time.sleep(0.25)    


                            
                        
                        else:
                            print('WRONG CODE! TRY AGAIN, YOU HAVE ', 3- attempt, ' TRIES REMAINING!\n')
                            attempt = attempt + 1
                            while attempt > 3:
                                my_pwm.ChangeDutyCycle(duty_cycle)
                                camera.start_preview() ##opens camera display window
                                time.sleep(2) #delay before taking picture
                                camera.capture("intruder_image.jpg") #saves image
                                time.sleep(1)
                                camera.stop_preview() #closes camera window
                                        #Clear the list for next time.
                            userEntry.clear()
                    time.sleep(0.01)

                        
        print(arming)
except KeyboardInterrupt:
    GPIO.cleanup()