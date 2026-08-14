#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/msg/int64.hpp"

using namespace std::chrono_literals;
using namespace std::placeholders;

class NumberPublisherNode : public rclcpp::Node {
    public:
        NumberPublisherNode() : Node("number_publisher") {
            this->declare_parameter("number", 2);
            this->declare_parameter("timer_period",1.0);

            number_ = this->get_parameter("number").as_int();
            double timer_period_ = this->get_parameter("timer_period").as_double();

            publisher_ = this->create_publisher<example_interfaces::msg::Int64>("number", 10);
            timer_ = this->create_wall_timer(
                std::chrono::duration<double>(timer_period_),
                std::bind(&NumberPublisherNode::publish_number, this)
            );

            param_callback_handle_ = this->add_post_set_parameters_callback(
                std::bind(&NumberPublisherNode::parametersCallback, this, _1)
            );

            RCLCPP_INFO(this->get_logger(), "Number Publisher Node has been started.");
        }
    
    private:
        rclcpp::Publisher<example_interfaces::msg::Int64>::SharedPtr publisher_;
        void publish_number() {
            auto msg = example_interfaces::msg::Int64();
            msg.data = number_;
            publisher_->publish(msg);
        }

        void parametersCallback(const std::vector<rclcpp::Parameter> & parameters) {
            for (const auto &param : parameters) {
                if (param.get_name() == "number") {
                    number_ = param.as_int();
                }
            }
        }

        int number_;
        rclcpp::TimerBase::SharedPtr timer_;
        PostSetParametersCallbackHandle::SharedPtr param_callback_handle_;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<NumberPublisherNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}