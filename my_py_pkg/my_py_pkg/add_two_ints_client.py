#!/usr/bin/env python3
from functools import partial

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class AddTwoIntClientNode(Node):
    def __init__(self):
        super().__init__('add_two_ints_client')
        self.client = self.create_client(AddTwoInts, 'add_two_ints')

    def call_add_two_ints(self, a: int, b: int):
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        request = AddTwoInts.Request()
        request.a = a
        request.b = b

        future = self.client.call_async(request)
        future.add_done_callback(partial(self.callback_add_two_ints, request=request))

    def callback_add_two_ints(self, future, request):
        response = future.result()
        self.get_logger().info(f"Result: {response.sum}")


def main(args=None):
    rclpy.init(args=args)
    node = AddTwoIntClientNode()
    node.call_add_two_ints(5, 3)
    node.call_add_two_ints(10, 3)
    node.call_add_two_ints(6, 1)
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()