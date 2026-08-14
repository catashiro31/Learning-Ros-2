#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.msg import Int64
from rclpy.parameter import Parameter


class NumberPublisherNode(Node):
    def __init__(self):
        super().__init__('number_publisher')
        self.declare_parameter("number", 2)
        self.declare_parameter("timer_period", 1.0)

        self.number = self.get_parameter("number").value
        self.timer_period = self.get_parameter("timer_period").value
        self.add_post_set_parameters_callback(self.parameters_callback)

        self.publishers_ = self.create_publisher(Int64, 'number', 10)
        self.timers_ = self.create_timer(self.timer_period, self.publish_number)
        self.get_logger().info('Number Publisher Node has been started.')

    def publish_number(self):
        msg = Int64()
        msg.data = self.number
        self.publishers_.publish(msg)

    def parameters_callback(self, params: list[Parameter]):
        for param in params:
            if param.name == "number":
                self.number = param.value
                

def main(args=None):
    rclpy.init(args=args)
    node = NumberPublisherNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()