#include "task_controller/task_controller_node.hpp"

TaskControllerNode::TaskControllerNode(): rclcpp::Node("navigate_node"){
    auto task_callback = [this](std_msgs::msg::String::UniquePtr msg) -> void {
        RCLCPP_INFO(this->get_logger(), "Received command.");

        std::cout << msg->data.c_str() << std::endl;
        
        // std::lock_guard<std::mutex> lock(command_mutex_);
        message_ = msg->data.c_str();
        received_command_ = true;
        // condition_variable_.notify_one();

        if(received_command_){
            if(this->init()){
                this->step();
            }
        }
    };

    subscriber_ = this->create_subscription<std_msgs::msg::String>("command", 10, task_callback); 
}

bool TaskControllerNode::init(){
//    std::unique_lock<std::mutex> lock(command_mutex_);
//    condition_variable_.wait(lock, [this]{return received_command_;});

    while (rclcpp::ok() && !received_command_) {
        RCLCPP_INFO(this->get_logger(), "Waiting for command...");
        rclcpp::sleep_for(std::chrono::milliseconds(500));
    }

    domain_expert_ = std::make_shared<plansys2::DomainExpertClient>();
    problem_expert_ = std::make_shared<plansys2::ProblemExpertClient>();
    planner_client_ = std::make_shared<plansys2::PlannerClient>();
    executor_client_ = std::make_shared<plansys2::ExecutorClient>();

    // add the robot and warehouse zones to the PDDL problem
    problem_expert_->addInstance(plansys2::Instance{robot_name_, "robot"});

    for(const std::string &zone: zones_){
        problem_expert_->addInstance(plansys2::Instance{zone, "zone"});
    }

    // set the robot's initial position and availability
    problem_expert_->addPredicate(plansys2::Predicate("(robot_at " + robot_name_ + " " + zones_[0] + ")"));
    problem_expert_->addPredicate(plansys2::Predicate("(robot_available " + robot_name_ + ")"));

    problem_expert_->addPredicate(plansys2::Predicate("(is_unload_zone " + zones_[1] + ")"));

    for(int i = 2; i < 6; i++){
        problem_expert_->addPredicate(plansys2::Predicate("(is_reol_zone " + zones_[i] + ")"));
    }

    // get predicates, instances and goal
    this->new_knowledge(this->message_);

    // get domain, problem and plan
    auto domain = domain_expert_->getDomain();
    auto problem = problem_expert_->getProblem();
    auto plan = planner_client_->getPlan(domain, problem);

    if(!plan.has_value()){
        std::cout << "Could not find a plan to reach goal "
                  << parser::pddl::toString(problem_expert_->getGoal())
                  << std::endl;

        return false;
    }

    // print the plan to console
    std::cout << "---------------- Plan ----------------" << std::endl;
    for(const auto &plan_item: plan.value().items){
        std::cout << plan_item.time << ":\t" << plan_item.action << "\t[" <<
            plan_item.duration << "]" << std::endl;
    }
    std::cout << "--------------------------------------" << std::endl;

    if(!executor_client_->start_plan_execution(plan.value())){
        RCLCPP_ERROR(this->get_logger(), "Error starting a new plan (first)");

        return false;
    }

    return true;
}

void TaskControllerNode::new_knowledge(std::string &command){
    std::istringstream command_stream(command);
    std::string single_command;

    while(std::getline(command_stream, single_command, '|')){
        if(single_command.find("set instance") == 0){
            // Extract instance name and type
            std::string instance = single_command.substr(std::string("set instance ").length());
            auto separator_position = instance.find(" ");
            std::string name = instance.substr(0, separator_position);
            std::string type = instance.substr(separator_position + 1);

            // make sure that the type is allowed
            if(type == "pallet"){
                problem_expert_->addInstance(plansys2::Instance{name, type});
            }else{
                RCLCPP_ERROR(this->get_logger(), "Type <%s> is not allowed.", type.c_str());
                return;
            }

        }else if(single_command.find("set predicate") == 0){
            // extract predicate
            std::string full_predicate = single_command.substr(std::string("set predicate ").length());
            auto first_separator_position = full_predicate.find(" ");
            
            std::string predicate = full_predicate.substr(0, first_separator_position);
            // check what predicate is being passed as 'pallet_at' has two arguments and 'pallet_not_moved' has one
            if(predicate == "pallet_at"){
                auto second_separator_position = full_predicate.find(" ", first_separator_position + 1);

                std::string predicate_instance = full_predicate.substr(first_separator_position + 1,
                                                                        second_separator_position - first_separator_position - 1);
                std::string predicate_zone = full_predicate.substr(second_separator_position + 1);

                problem_expert_->addPredicate(plansys2::Predicate("("+predicate+" "+predicate_instance+" "+predicate_zone+")" ));
            }else{
                std::string predicate_instance = full_predicate.substr(first_separator_position + 1);

                problem_expert_->addPredicate(plansys2::Predicate("("+predicate+" "+predicate_instance+")" ));
            }
            
        }else if(single_command.find("set goal") == 0){
            // extract goal
            std::string goal = single_command.substr(std::string("set goal ").length());
            auto first_separator_position = goal.find(" ");
            auto second_separator_position = goal.find(" ", first_separator_position + 1);

            std::string predicate = goal.substr(0, first_separator_position);
            std::string predicate_instance = goal.substr(first_separator_position + 1,
                                                            second_separator_position - first_separator_position - 1);
            std::string predicate_zone = goal.substr(second_separator_position + 1);

            problem_expert_->setGoal(plansys2::Goal("(and("+predicate+" "+predicate_instance+" "+predicate_zone+"))"));
        }
    }
}

void TaskControllerNode::step(){
    if(!executor_client_->execute_and_check_plan()){
        auto result = executor_client_->getResult();
        if(result.value().success){
            RCLCPP_INFO(this->get_logger(), "Plan successfully finished");
        }else{
            RCLCPP_ERROR(this->get_logger(), "Plan finished with error");
        }
    }
}

int main(int argc, char **argv){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TaskControllerNode>();

    rclcpp::spin_some(node->get_node_base_interface());

    rclcpp::shutdown();
  
    return 0;
}

