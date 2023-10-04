from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from rclpy.node import Node
import rclpy
import sys
import math
import time

class TurtleBot(Node):

     def __init__(self):
         super().__init__('move_to_goal')
         
         self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
         self.subscriber = self.create_subscription(Pose, '/turtle1/pose', self.update_pose, 10)
         
         self.pose = Pose()
         
         self.timer = self.create_timer(0.1, self.move2goal)


     def update_pose(self, data):
         self.pose = data

     def move2goal(self):
     
         self.goal_x = float(sys.argv[1])
         self.goal_y = float(sys.argv[2])
         self.goal_theta = float(sys.argv[3]) * math.pi / 180
     
         msg = Twist()

         rasst = math.sqrt(math.pow((self.goal_x - self.pose.x), 2) + math.pow((self.goal_y - self.pose.y), 2))
         angle = math.atan2(self.goal_y - self.pose.y, self.goal_x - self.pose.x)

         msg.linear.x = rasst
         msg.angular.z = 4.0 * (angle - self.pose.theta)
         self.publisher.publish(msg)
         
         if rasst < 0.01 and abs(angle) > 0.01:
            msg.angular.z = - self.goal_theta
            self.publisher.publish(msg)
 
            flag = 10
            while flag !=0:  
                self.publisher.publish(msg)
                time.sleep(0.1)  
                flag -= 1  
            
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            
            self.timer.cancel()
            self.publisher.publish(msg)
            quit()

def main(args=None):
    rclpy.init(args=args)
    x = TurtleBot()
    rclpy.spin(x)
    x.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
