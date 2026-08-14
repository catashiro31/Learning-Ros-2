#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from my_robot_interfaces.msg import LEDPanelStatus
from my_robot_interfaces.srv import SetLED

class LEDPanelNode(Node):
    def __init__(self):
        super().__init__('led_panel_node')
        self.declare_parameter("led_states",[0, 0, 0])
        self.led_states = self.get_parameter("led_states").value

        self.publisher_ = self.create_publisher(LEDPanelStatus, 'led_panel_status', 10)
        self.service_ = self.create_service(SetLED, 'set_led', self.callback_set_led)
        self.timer_ = self.create_timer(0.5, self.publish_led_pannel_state)

        self.get_logger().info("LEDPanel has been started!")


    def publish_led_pannel_state(self):
        msg = LEDPanelStatus()
        msg.led_panel_status = self.led_states
        self.publisher_.publish(msg)

    def callback_set_led(self, request: SetLED.Request, response: SetLED.Response):
        if request.led_number < 0 or request.led_number >= len(self.led_states):
            response.success = False
            return response

        if request.state not in [0,1]:
            response.success = False
            return response

        self.led_states[request.led_number] = request.state
        response.success = True

        return response

def main(args=None):
    rclpy.init(args=args)
    node = LEDPanelNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()