#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim_interfaces.msg import Position
from turtlesim_interfaces.srv import Predator2Processer
from functools import partial
from turtlesim.msg import Pose
import math

class PredatorNode(Node):
    def __init__(self):
        super().__init__('predator')

        self.subcriber_ = self.create_subscription(Position, '/position', self.call_pos, 10) # Yes
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.call_predator, 10)
        self.client_ = self.create_client(Predator2Processer, 'move') # 
        
        self.timer_ = self.create_timer(1.0, self.select_target)

        self.get_logger().info("Predator Node has beend started")

    def call_predator(self, msg):
        self.predator = msg

        self.get_logger().info('Infomation about Position of Predator is stored')

    def call_pos(self, msg: Position):
        self.turtles_x = msg.turtles_x
        self.turtles_y = msg.turtles_y

        # self.get_logger().info(f"Get: (lx = {self.turtles_x}; ly ={self.turtles_y})")

    def select_target(self):
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        pos = 0
        request = Predator2Processer.Request()
        request.x = self.turtles_x[pos]
        request.y = self.turtles_y[pos]
        request.p = pos

        future = self.client_.call_async(request)
        future.add_done_callback(partial(self.callback_move, request=request))

    def callback_move(self, future, request):
        response = future.result()
        self.get_logger().info(f"Is Target Killed: {response.status}")

def main(args=None):
    rclpy.init(args=args)
    node = PredatorNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()