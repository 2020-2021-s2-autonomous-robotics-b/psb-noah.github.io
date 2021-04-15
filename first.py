from locorobo import LocoRobo
from locorobo import MotorDirection
from locorobo import Data
from locorobo import WaitType
from locorobo import Song
from locorobo import Note

def get_robot(robots, name):
    robot = None

    # Search through robots found during the scan for
    # the one we want
    for r in robots.values():
        if r.name == name:
            robot = r

            # We found the robot, so stop the for loop
            break

    # If we did not find the robot during the scan, stop the program
    if not robot:
        raise Exception('Could not find robot with specified name')

    return robot


def main():
    # Tell LocoRobo what serial port to use
    LocoRobo.setup("/dev/tty.usbmodem1")
    
    # Scan for robots
    robots = LocoRobo.scan(2000)

    # Use get_robots to find robot with name lr d2:fa in the scan result
    robot = get_robot(robots, "lr d2:fa")

    robot.connect()
    robot.activate_motors()
    robot.enable_sensor(Data.ULTRASONIC, True)
    
    #setup the distance to be travelled in centimeters
    distance_cm = 100
    
    # tried to use ultrasonic sensors to detect how far away a wall was, didn't go too well
    # distance_cm = robot.get_sensor_value(Data.ULTRASONIC) - 10 #so that the robot doesn't HIT the wall
    # print(distance_cm)
    
    robot.setup_wait(WaitType.DISTANCE, distance_cm * 1000)
    robot.move(MotorDirection.FORWARD, MotorDirection.FORWARD, 1, 1, True)
    
    robot.deactivate_motors()
    robot.disconnect()

# If we are on the main thread, run the program
if __name__ == "__main__":

    try:
        main()
    except:
        LocoRobo.stop()
        raise

    LocoRobo.stop()

    # For compatibility with webapp's python, we can't use finally.
    # If you are using local python, you can do the following
    #
    # try:
    #     main()
    # finally:
    #     LocoRobo.stop()
