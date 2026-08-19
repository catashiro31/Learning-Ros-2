#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim_interfaces.srv import Predator2Processer
from turtlesim_interfaces.srv import Processer2Pawner
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
import math
from functools import partial

class ProcesserNode(Node):
    def __init__(self):
        super().__init__('processer')

        self.distance_tolerance = 0.1

        self.cmd_vel_pub = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.callback_pos, 10)
        self.server_ = self.create_service(Predator2Processer, 'move', self.callback_move)
        self.client_ = self.create_client(Processer2Pawner, 'notify')
        self.get_logger().info("Processer Node has been started")

    def callback_pos(self, msg):
        self.predator = msg

        # self.get_logger().info(f"Predator Position: x = {self.predator.x}; y = {self.predator.y}")

    def move_predator(self):
        msg = Twist()

        distance = math.sqrt((self.target_x-self.predator.x)**2 + (self.target_y-self.predator.y)**2)

        if distance >= self.distance_tolerance:
            target_angle = math.atan2(self.target_y - self.predator.y, 
                                      self.target_x - self.predator.x)
            angle_error = target_angle - self.predator.theta
            msg.angular.z = 4.0 * angle_error
            msg.linear.x = 1.0 * distance

            self.cmd_vel_pub.publish(msg)
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.cmd_vel_pub.publish(msg)
            self.timer.cancel()

    def callback_move(self, request, response):
        self.target_x = request.x
        self.target_y = request.y
        self.target_p = request.p

        self.get_logger().info("Predator is comming")
        self.timer = self.create_timer(1.0, self.move_predator)
        self.get_logger().info('One turtle is killed')
        self.timer = self.create_timer(1.0, self.call_notify)

        response.status = True

        return response

    def call_notify(self):
        while not self.client_.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        request = Processer2Pawner.Request()
        request.p = self.target_p

        future = self.client_.call_async(request)
        future.add_done_callback(partial(self.callback_notify, request=request))

    def callback_notify(self, future, request):
        response = future.result()
        self.get_logger().info(f"Notified to Turtle Spawner: {response.status}")


def main(args=None):
    rclpy.init(args=args)
    node = ProcesserNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()