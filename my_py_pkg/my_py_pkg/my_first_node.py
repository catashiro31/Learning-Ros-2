#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

class My_Node(Node):
    def __init__(self):
        super().__init__('Test_node')
        self.get_logger().info('Hello ROS2')
        self.counter = 0
        self.create_timer(1.0, self.callback)

    def callback(self):
        self.get_logger().info('ROS2' + str(self.counter))
        self.counter += 1

def main(args=None):
    rclpy.init(args=args)
    node = My_Node()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()