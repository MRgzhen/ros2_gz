#include "rclcpp/rclcpp.hpp"
#include "control_msgs/msg/joint_jog.hpp"
#include <vector>
#include <string>


class RRBotPositionSubcriber : public rclcpp::Node {
public:
    RRBotPositionSubcriber() : Node("rrbotpositionsubscriber") {
        state_subscriber_ = this->create_subscription<control_msgs::msg::JointJog>("my_controller/state",10,
        std::bind(&RRBotPositionSubcriber::state_callback,this,std::placeholders::_1)
        );
    }
private:
    void state_callback(const control_msgs::msg::JointJog::SharedPtr msg) {
        RCLCPP_INFO(this->get_logger(),"time: %d",msg->header.stamp.sec);
        for(size_t i = 0; i < msg->joint_names.size()&& i < msg->displacements.size(); ++i) {
            RCLCPP_INFO(this->get_logger(),"%s: %.2f",
            msg->joint_names[i].c_str(),
            msg->displacements[i]
        );
    }
    RCLCPP_INFO(this->get_logger(),"-----------");        
    }
    rclcpp::Subscription<control_msgs::msg::JointJog>::SharedPtr state_subscriber_;
};

int main(int argc, char const *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<RRBotPositionSubcriber>());
    rclcpp::shutdown();
    return 0;
}