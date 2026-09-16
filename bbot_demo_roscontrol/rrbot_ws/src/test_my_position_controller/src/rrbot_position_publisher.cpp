#include "rclcpp/rclcpp.hpp"
#include "control_msgs/msg/joint_jog.hpp"
#include <vector>
#include <chrono>

using namespace std::chrono_literals;

class RRBotPositionPublisher : public rclcpp::Node {
public:
    RRBotPositionPublisher() : Node("rrbotpositionpublisher"),index_(0) {
        position_publisher_ = this->create_publisher<control_msgs::msg::JointJog>("my_controller/reference",10);
        msg_.joint_names = {"joint1","joint2"};
        displacements_ = {
          {0.0,0.0},
          {1.0,1.0},
          {0.0,0.0},
          {-1.0,-1.0}
        };
        time_ = this->create_wall_timer(3s, std::bind(&RRBotPositionPublisher::time_callback,this));
    }

private:
    void time_callback() {
      const auto &disp = displacements_[index_ % displacements_.size()];
      msg_.displacements = disp;
      position_publisher_->publish(msg_);
      index_++;
      RCLCPP_INFO(this->get_logger(),"Published displacement:[%.2f, %.2f]",
                    disp[0],disp[1]);
    }

    rclcpp::Publisher<control_msgs::msg::JointJog>::SharedPtr position_publisher_;
    control_msgs::msg::JointJog msg_;
    std::vector<std::vector<double>> displacements_; 
    rclcpp::TimerBase::SharedPtr time_;
    size_t index_;
};

int main(int argc, char const *argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<RRBotPositionPublisher>());
    rclcpp::shutdown();
    return 0;
}