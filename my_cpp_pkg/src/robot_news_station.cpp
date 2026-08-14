#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/string.hpp"

using namespace std::chrono_literals;

class RobotNewsStationNode : public rclcpp::Node {
    public:
        RobotNewsStationNode() : Node("robot_news_station") {
            this->declare_parameter("robot_name", "Asimo");
            robot_name_ = this->get_parameter("robot_name").as_string();

            publisher_ = this->create_publisher<example_interfaces::msg::String>("robot_news", 10);
            timer_ = this->create_wall_timer(0.5s, std::bind(&RobotNewsStationNode::publish_news, this));
            RCLCPP_INFO(this->get_logger(), "Robot News Station Node has been started.");
        }
    
    private:
        rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
        void publish_news() {
            auto msg = example_interfaces::msg::String();
            msg.data = "Hello from " + robot_name_ + "!";
            publisher_->publish(msg);
        }
        std::string robot_name_;
        rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<RobotNewsStationNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}