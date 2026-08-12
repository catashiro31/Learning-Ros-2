#include<rclcpp/rclcpp.hpp>
#include<example_interfaces/srv/add_two_ints.hpp>

using namespace std::chrono_literals;
using namespace std::placeholders;

class AddTwoIntsClient : public rclcpp::Node {
    public:
        AddTwoIntsClient() : Node("add_two_ints_client") {
            client = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");
        }

        void callAddTwoIntsService(int a, int b) {
            while (!client->wait_for_service(1s)) {
                RCLCPP_WARN(this->get_logger(), "Service not available, waiting again...");
            }

            auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
            request->a = a;
            request->b = b;

            auto future = client->async_send_request(
                request,
                std::bind(&AddTwoIntsClient::callbackAddTwoInts, this, _1)
            );
        }
    
    private:
        void callbackAddTwoInts(rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future) {
            auto response = future.get();
            RCLCPP_INFO(this->get_logger(), "Result: %d", (int)response->sum);
        }
        rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client;
};

int main(int argc, char **argv) {
    rclcpp::init(argc, argv);
    auto node = std::make_shared<AddTwoIntsClient>();
    node->callAddTwoIntsService(3, 5);
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}