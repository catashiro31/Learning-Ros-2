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
        self.move_timer = None

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
            angle_error = math.atan2(math.sin(angle_error), math.cos(angle_error))
            
            # 1. Hệ số góc xoay giữ ở mức vừa phải để cua êm
            msg.angular.z = 1.3 * angle_error
            
            # 2. TẠO ĐƯỜNG CONG (CURVE FACTOR)
            # Hàm cosin vẫn dùng để giảm tốc khi góc lệch lớn
            # NHƯNG ta cộng thêm 0.4 (40%) để đảm bảo rùa không bao giờ dừng hẳn.
            # Dù mục tiêu ở sau lưng, rùa vẫn lết tới trước 40% tốc độ trong lúc bẻ lái
            curve_factor = 0.4 + 0.6 * max(0.0, math.cos(angle_error))
            
            # 3. Tính toán và áp dụng
            raw_speed = 1.0 * distance
            msg.linear.x = min(raw_speed, 1.5) * curve_factor

            self.cmd_vel_pub.publish(msg)
            
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.cmd_vel_pub.publish(msg)
            
            self.move_timer.cancel()
            self.move_timer = None
            
            self.get_logger().info('One turtle is killed')
            self.call_notify()

    def callback_move(self, request, response):
        self.target_x = request.x
        self.target_y = request.y
        self.target_p = request.p

        if self.move_timer == None:
            self.get_logger().info("Predator is comming")
            self.move_timer = self.create_timer(0.05, self.move_predator)

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