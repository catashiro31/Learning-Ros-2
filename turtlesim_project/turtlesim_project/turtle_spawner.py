#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from turtlesim_interfaces.msg import Position
from turtlesim_interfaces.srv import Processer2Pawner
from turtlesim.srv import Spawn, Kill
import random

class TurtleSpawnerNode(Node):
    def __init__(self):
        super().__init__('turtle_spawner')
        self.declare_parameter("timer_period", 0.1)
        self.timer_period = self.get_parameter("timer_period").value

        self.turtle_lx = []
        self.turtle_ly = []
        self.turtle_names = []
        self.count = 0

        self.publisher_ = self.create_publisher(Position, "/position", 10)
        self.timer_ = self.create_timer(self.timer_period, self.call_turtle_spawner)
        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.kill_client = self.create_client(Kill, '/kill')
        self.server_ = self.create_service(Processer2Pawner, 'notify', self.process_notification)
        self.get_logger().info("Turtle Spawner Node has been started")

    def spawn_real_turtle(self, x, y, name):
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...y')

        request = Spawn.Request()
        request.x = x
        request.y = y
        request.theta = random.uniform(0.0, 3.14)
        request.name = name

        self.spawn_client.call_async(request)

    def call_turtle_spawner(self):
        
        while len(self.turtle_lx) < 5:
            x = random.random()*10.5
            y = random.random()*10.5

            self.turtle_lx.append(x)
            self.turtle_ly.append(y)
            self.turtle_names.append(f"turtle_{self.count}")

            self.spawn_real_turtle(x,y,f"turtle_{self.count}")
            self.count += 1
            

        msg = Position()
        msg.turtles_x = self.turtle_lx.copy()
        msg.turtles_y = self.turtle_ly.copy()


        self.publisher_.publish(msg)

    def process_notification(self, request, response):

        self.get_logger().info(f"x={self.turtle_lx}, y={self.turtle_ly}")
        
        kill_req = Kill.Request()
        kill_req.name = self.turtle_names[request.p]
        self.kill_client.call_async(kill_req)

        del self.turtle_lx[request.p]
        del self.turtle_ly[request.p]
        del self.turtle_names[request.p]

        response.status = True
        self.get_logger().info(f"Position of killed Turtle: {request.p}")
        return response

def main(args=None):
    rclpy.init(args=args)
    node = TurtleSpawnerNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()