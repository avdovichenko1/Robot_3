import rclpy
import sys
from rclpy.node import Node
from tutorial_interfaces.srv import FullNameSumService


class ClientName(Node):

    def __init__(self):
        super().__init__('client_name')
        self.client = self.create_client(FullNameSumService, 'summ_full_name')
        
        while not self.client.wait_for_service(timeout_sec=1.0):
        	self.get_logger().info('I am a very lazy')
        
        self.request = FullNameSumService.Request()
        

    def give_request(self, last_name, name, first_name):
        self.request.last_name = last_name
        self.request.name = name
        self.request.first_name = first_name
        
        res = self.client.call_async(self.request)
        rclpy.spin_until_future_complete(self, res)
        
        return res.result()


def main():
    rclpy.init()

    client_name = ClientName()
    
    res = client_name.give_request(sys.argv[1], sys.argv[2], sys.argv[3])
    
    if res:
    	client_name.get_logger().info('Full name: %s' % res.full_name)


    client_name.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
