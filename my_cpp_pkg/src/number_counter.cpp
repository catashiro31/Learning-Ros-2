#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

using namespace std::chrono_literals;

class NumberCounterNode : public rclcpp::Node {
    public:
        NumberCounterNode() : Node("number_counter_node") {
            subscription_ = this->create_subscription<example_interfaces::msg::Int64>(
                "number",
                10,
                std::bind(&NumberCounterNode::callback, this, std::placeholders::_1)
            );
            publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number_count", 10);
            timer_ = this->create_wall_timer(
                0.5s,
                std::bind(&NumberCounterNode::publish, this)
            );
            RCLCPP_INFO(this->get_logger(), "Number Counter Node has been started.");
        }
    
    private:
        rclcpp::Subscription<example_interfaces::msg::Int64>::SharedPtr subscription_;
        rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
        rclcpp::TimerBase::SharedPtr timer_;
        int count = 0, number = 0;
        void callback(const example_interfaces::msg::Int64::SharedPtr msg) {
            RCLCPP_INFO(this->get_logger(), "Received number: %ld", msg->data);
            this->number = msg->data;
        }
        void publish() {
            auto msg = example_interfaces::msg::Int64();
            msg.data = this->number + this->count;
            this->count+=2;
            publisher_->publish(msg);
        }
        
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NumberCounterNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}