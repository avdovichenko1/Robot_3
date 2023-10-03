from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from rclpy.node import Node
import rclpy
import sys
import math
import time
class TurtleBot(Node):

     def __init__(self):
         super().__init__('turtlebot_controller')
         self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
         self.subscriber = self.create_subscription(Pose, '/turtle1/pose', self.update_pose, 10)
         self.pose = Pose()
         self.timer = self.create_timer(0.1, self.move2goal)

     def update_pose(self, data):
         self.pose = data

     def move2goal(self):
         const = 5
         msg = Twist()
         goal_pose = Pose()
 
         goal_pose.x = float(sys.argv[1])
         goal_pose.y = float(sys.argv[2])
         goal_pose.theta = float(sys.argv[3]) * math.pi / 180
         
         if (goal_pose.x<0 or goal_pose.y<0):
            self.get_logger().info("Error, x and y must be more then 0")
            quit()
            
         rasst = math.sqrt(math.pow((goal_pose.x - self.pose.x), 2) + math.pow((goal_pose.y - self.pose.y), 2))
         angle = math.atan2(goal_pose.y - self.pose.y, goal_pose.x - self.pose.x)
         self.get_logger().info('%s" ' % self.pose.theta) 
         msg.angular.z = -self.pose.theta
         self.publisher.publish(msg)
         time.sleep(1)
         msg.angular.z = angle
         self.publisher.publish(msg)
         time.sleep(1)
         msg.linear.x = rasst
         msg.angular.z = 0.0
         self.publisher.publish(msg)
         time.sleep(1)
         msg.linear.x = 0.0
         msg.angular.z = -angle
         self.publisher.publish(msg)
         time.sleep(1)
         msg.angular.z = goal_pose.theta
         self.publisher.publish(msg)
         time.sleep(1)

         self.get_logger().info("Done")
         quit()
 
         
def main(args=None):
    rclpy.init(args=args)
    x = TurtleBot()
    rclpy.spin(x)
    x.destroy_node()
    rclpy.shutdown()

 
if __name__ == '__main__':
    main()
