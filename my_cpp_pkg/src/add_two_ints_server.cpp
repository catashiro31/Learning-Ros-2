#include "rclcpp/rclcpp.hpp"
#include "example_interfaces/srv/add_two_ints.hpp"

using namespace std::placeholders;

class AddTwoInt: public rclcpp::Node {
    public:
        AddTwoInt() : Node("add_two_ints") {
            server = this->create_service<example_interfaces::srv::AddTwoInts>(
                "add_two_ints", 
                std::bind(&AddTwoInt::callback_add_two_ints, this, _1, _2)
            );
            RCLCPP_INFO(this->get_logger(), "Service 'add_two_ints' is ready to receive requests.");
        }
    
    private:
        rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr server;
        
        void callback_add_two_ints(
            const std::shared_ptr<example_interfaces::srv::AddTwoInts::Request> request,
            std::shared_ptr<example_interfaces::srv::AddTwoInts::Response> response
        ) {
            response->sum = request->a + request->b;
            RCLCPP_INFO(this->get_logger(), "Sum of a=%ld, b=%ld = %ld", request->a, request->b, response->sum);
        }
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<AddTwoInt>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}