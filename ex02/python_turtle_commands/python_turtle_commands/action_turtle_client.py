import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
from action_turtle_commands.action import MessageTurtleCommands 

class CommandActionClient(Node):

    def __init__(self):
        super().__init__('action_turtle_client')
        self._action_client = ActionClient(self, MessageTurtleCommands, 'move_turtle')
        self.rasst = 0
        self.num=0
        self.send_goal()

    def send_goal(self):
        goal_msg = MessageTurtleCommands.Goal()
        self._action_client.wait_for_server()

        goal_msg.command = 'forward'
        goal_msg.angle = 0
        goal_msg.s = 2
        self.send_goal_with_delay(goal_msg, 2)

        goal_msg.command = 'turn_right'
        goal_msg.angle = 90
        goal_msg.s = 0
        self.send_goal_with_delay(goal_msg, 2) 

        goal_msg.command = 'forward'
        goal_msg.angle = 0
        goal_msg.s = 1
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback_result)
         

    def send_goal_with_delay(self, goal_msg, delay_seconds):
        self._send_goal_future = self._action_client.send_goal_async(goal_msg, feedback_callback=self.feedback_callback)
        self._send_goal_future.add_done_callback(self.goal_response_callback)
          

    def goal_response_callback_result(self, future):
    
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().info('Error')
            return
	
        else:
            self.get_logger().info('Success action')
        
        self._get_result_future = goal_handle.get_result_async()
        self._get_result_future.add_done_callback(self.get_result_callback)
        
    def goal_response_callback(self, future):
        goal_handle = future.result()
        
        if not goal_handle.accepted:
            self.get_logger().info('Error')
            return

        else:
            self.get_logger().info('Success action')
        
    def get_result_callback(self, future):
        result = future.result().result
        
        if not result.result:
            self.get_logger().info('Error')
            
        else:
            self.get_logger().info('Done')

        rclpy.shutdown()

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.odom))
        self.num+=1
        
        if self.num % 3 == 1:
            self.rasst+=2
            
        if self.num % 3 == 0:
            self.rasst+=1
            
        self.get_logger().info('Distance travell: {0}'.format(self.rasst))

def main(args=None):
    rclpy.init(args=args)
    action_client = CommandActionClient()
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()

