#include "task_controller/task_controller_node.hpp"

TaskControllerNode::TaskControllerNode(): rclcpp::Node("task_controller_node"){
    domain_expert_ = std::make_shared<plansys2::DomainExpertClient>();
    problem_expert_ = std::make_shared<plansys2::ProblemExpertClient>();
    planner_client_ = std::make_shared<plansys2::PlannerClient>();
    executor_client_ = std::make_shared<plansys2::ExecutorClient>();

    // set init knowledge
    problem_expert_->addInstance(plansys2::Instance{robot_name_, "robot"});

    for(const std::string &zone: zones_){
        problem_expert_->addInstance(plansys2::Instance{zone, "zone"});
    }

    problem_expert_->addPredicate(plansys2::Predicate("(robot_at " + robot_name_ + " " + zones_[0] + ")"));
    problem_expert_->addPredicate(plansys2::Predicate("(robot_available " + robot_name_ + ")"));

    problem_expert_->addPredicate(plansys2::Predicate("(is_unload_zone " + zones_[1] + ")"));

    for(int i = 2; i < 6; i++){
        problem_expert_->addPredicate(plansys2::Predicate("(is_reol_zone " + zones_[i] + ")"));
    }
    
    // node logic
    auto task_callback = [this](std_msgs::msg::String::UniquePtr msg) -> void{
        try{
            RCLCPP_INFO(this->get_logger(), "Received command: %s", msg->data.c_str());

            message_ = msg->data.c_str();

            get_problem_specific_knowledge(message_);
            get_plan_logic_and_start();

            while(true){
                if(!executor_client_->execute_and_check_plan()){
                    auto result = executor_client_->getResult();
                    if(result.value().success){
                        RCLCPP_INFO(this->get_logger(), "Plan finished.");
                        break;
                    }else{
                        RCLCPP_ERROR(this->get_logger(), "Error in plan execution.");
                        break;
                    }
                }
            }
        
        }catch(const rclcpp::exceptions::RCLError &e){
            RCLCPP_ERROR(this->get_logger(), "ROS 2 client error: %s", e.what());
        
        }catch(const std::exception &e){
            RCLCPP_ERROR(this->get_logger(), "Standard error: %s", e.what());
        }
    };
    
    subscriber_ = this->create_subscription<std_msgs::msg::String>("command", 10, task_callback);   
}

void TaskControllerNode::get_problem_specific_knowledge(std::string &command){
    std::istringstream command_stream(command);
    std::string single_command;
    std::vector<std::string> goal_container;
    std::string goals;

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
            // extract goals and append to goal_container
            std::string single_goal = single_command.substr(std::string("set goal ").length());
            auto first_separator_position = single_goal.find(" ");
            auto second_separator_position = single_goal.find(" ", first_separator_position + 1);

            std::string predicate = single_goal.substr(0, first_separator_position);
            std::string predicate_instance = single_goal.substr(first_separator_position + 1,
                                                            second_separator_position - first_separator_position - 1);
            std::string predicate_zone = single_goal.substr(second_separator_position + 1);

            goal_container.push_back("(" + predicate + " " + predicate_instance + " " + predicate_zone + ")");          
        }
    }

    // pass all goals from goal_container to problem expert
    if(!goal_container.empty()){
        goals = "(and ";
        for (const auto &goal: goal_container){
            goals += goal + " ";
        }
        goals += ")";

        problem_expert_->setGoal(plansys2::Goal(goals));
    }
}

bool TaskControllerNode::get_plan_logic_and_start(){
    auto domain = domain_expert_->getDomain();
    auto problem = problem_expert_->getProblem();
    auto plan = planner_client_->getPlan(domain, problem);

    // check if plan is valid
    if(!plan.has_value()){
        std::cout << "Could not find a suitable plan to reach goal "
                  << parser::pddl::toString(problem_expert_->getGoal())
                  << std::endl;
        
        return false;
    }

    // print plan to console
    std::cout << "---------------- Plan ----------------" << std::endl;
    for(const auto &plan_item: plan.value().items){
        std::cout << plan_item.time << ":\t" << plan_item.action << "\t[" <<
            plan_item.duration << "]" << std::endl;
    }
    std::cout << "--------------------------------------" << std::endl;

    // start plan execution
    if(!executor_client_->start_plan_execution(plan.value())){
        RCLCPP_ERROR(this->get_logger(), "Error starting a new plan (first).");

        return false;
    }

    return true;
}

int main(int argc, char **argv){
    rclcpp::init(argc, argv);
    auto node = std::make_shared<TaskControllerNode>();

    rclcpp::spin(node);

    rclcpp::shutdown();

    return 0;
}