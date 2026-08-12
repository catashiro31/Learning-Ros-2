#include "rclcpp/rclcpp.hpp"

class My_Node : public rclcpp::Node {
public:
    My_Node() : Node("Test_node") {
        RCLCPP_INFO(this->get_logger(), "Hello ROS2");
        timer_ = this->create_wall_timer(std::chrono::seconds(1), std::bind(&My_Node::callback, this));
    }
private:
    void callback() {
        RCLCPP_INFO(this->get_logger(), "ROS2 %d", counter_);
        counter_++;
    }
    rclcpp::TimerBase::SharedPtr timer_;
    int counter_ = 0;
};

int main(int argc, char **argv) {
  rclcpp::init(argc, argv);
  auto node = std::make_shared<My_Node>();
  rclcpp::spin(node);
  rclcpp::shutdown();
  return 0;
}