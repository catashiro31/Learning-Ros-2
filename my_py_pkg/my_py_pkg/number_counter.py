#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from example_interfaces.srv import SetBool

class NumberCounterNode(Node):
    def __init__(self):
        super().__init__('number_counter')
        self.counter = 0
        self.number = 0
        self.subscribers_ = self.create_subscription(Int64, 'number', self.callback, 10)
        self.publishers_ = self.create_publisher(Int64, 'number_count', 10)
        self.timers_ = self.create_timer(0.5, self.publish_count)
        self.service_server_ = self.create_service(SetBool, 'reset_counter', self.reset_counter_callback)

    def callback(self, msg):
        self.number = msg.data
        self.get_logger().info(f'Number received: {msg.data}')

    def publish_count(self):
        count_msg = Int64()
        count_msg.data = self.number + self.counter
        self.counter += 1
        self.publishers_.publish(count_msg)

    def reset_counter_callback(self, request: SetBool.Request, response: SetBool.Response):
        if request.data:
            self.counter = 0
            response.success = True
            response.message = 'Counter reset to zero.'
            self.get_logger().info('Counter has been reset.')
        else:
            response.success = False
            response.message = 'Counter not reset.'
            self.get_logger().info('Counter reset request denied.')
        return response

def main(args=None):
    rclpy.init(args=args)
    node = NumberCounterNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()