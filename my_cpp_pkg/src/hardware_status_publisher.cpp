#include "rclcpp/rclcpp.hpp"
#include "my_robot_interfaces/msg/hardware_status.hpp"

using namespace std::chrono_literals;

class HardwareStatusPublisherNode : public rclcpp::Node {
    public:
        HardwareStatusPublisherNode() : Node("hardware_status") {
            publisher_ = this->create_publisher<my_robot_interfaces::msg::HardwareStatus>(
            "hardware_status", 10);
            timer_ = this->create_wall_timer(
            0.5s, 
            std::bind(&HardwareStatusPublisherNode::publish_hardware_status, this));
            RCLCPP_INFO(this->get_logger(), "Hardware Status Publisher Node has started");
        }
    
    private:
    rclcpp::Publisher<my_robot_interfaces::msg::HardwareStatus>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;

    void publish_hardware_status() {
        auto msg = my_robot_interfaces::msg::HardwareStatus();
        msg.temperature = 23.45;
        msg.are_motors_ready = true;
        msg.debug_message = "Motor is working fine";
        publisher_->publish(msg);
    }
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<HardwareStatusPublisherNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}