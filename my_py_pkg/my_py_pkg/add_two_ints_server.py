#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddTwoIntServerNode(Node):
    def __init__(self):
        super().__init__('add_two_ints_server')
        self._service = self.create_service(AddTwoInts, 'add_two_ints', self._add_two_ints_callback)
        self.get_logger().info('Add Two Ints Service is ready.')

    def _add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(f"Incoming request: {request.a} + {request.b} = {response.sum}")
        return response

def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntServerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()