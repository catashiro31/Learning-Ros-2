#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"
#include "example_interfaces/srv/set_bool.hpp"

using namespace std::chrono_literals;
using namespace std::placeholders;

class NumberCounterNode : public rclcpp::Node {
    public:
        NumberCounterNode() : Node("number_counter_node") {
            subscription_ = this->create_subscription<example_interfaces::msg::Int64>(
                "number",
                10,
                std::bind(&NumberCounterNode::callback, this, _1)
            );
            publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number_count", 10);
            timer_ = this->create_wall_timer(
                0.5s,
                std::bind(&NumberCounterNode::publish, this)
            );
            service_ = this->create_service<example_interfaces::srv::SetBool>(
                "reset_counter",
                std::bind(&NumberCounterNode::reset_counter_callback, this, _1, _2)
            );
            RCLCPP_INFO(this->get_logger(), "Number Counter Node has been started.");
        }
    
    private:
        rclcpp::Subscription<example_interfaces::msg::Int64>::SharedPtr subscription_;
        rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
        rclcpp::Service<example_interfaces::srv::SetBool>::SharedPtr service_;
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
        void reset_counter_callback(
            const std::shared_ptr<example_interfaces::srv::SetBool::Request> request,
            std::shared_ptr<example_interfaces::srv::SetBool::Response> response) {
            if (request->data) {
                this->count = 0;
                response->success = true;
                response->message = "Counter has been reset.";
                RCLCPP_INFO(this->get_logger(), "Counter has been reset.");
            } else {
                response->success = false;
                response->message = "Counter reset request was false.";
                RCLCPP_WARN(this->get_logger(), "Counter reset request was false.");
            }
        }
        
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NumberCounterNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}