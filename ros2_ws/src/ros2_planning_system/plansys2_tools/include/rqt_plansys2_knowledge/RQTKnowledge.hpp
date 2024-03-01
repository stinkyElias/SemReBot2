// Copyright 2022 Intelligent Robotics Lab
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

#ifndef RQT_PLANSYS2_KNOWLEDGE__RQTKNOWLEDGE_HPP_
#define RQT_PLANSYS2_KNOWLEDGE__RQTKNOWLEDGE_HPP_

#include <ui_rqt_plansys2_knowledge.h>
#include <rqt_gui_cpp/plugin.h>


#include <QAction>
#include <QImage>
#include <QList>
#include <QString>
#include <QSet>
#include <QSize>
#include <QWidget>

#include <map>
#include <memory>

#include "rqt_plansys2_knowledge/KnowledgeTree.hpp"
#include "plansys2_problem_expert/ProblemExpertClient.hpp"

#include "plansys2_msgs/msg/knowledge.hpp"
#include "rclcpp/rclcpp.hpp"

namespace rqt_plansys2_knowledge
{


class RQTKnowledge
  : public rqt_gui_cpp::Plugin
{
  Q_OBJECT

public:
  RQTKnowledge();

  virtual void initPlugin(qt_gui_cpp::PluginContext & context);
  virtual void shutdownPlugin();
  virtual void saveSettings(
    qt_gui_cpp::Settings & plugin_settings, qt_gui_cpp::Settings & instance_settings) const;
  virtual void restoreSettings(
    const qt_gui_cpp::Settings & plugin_settings, const qt_gui_cpp::Settings & instance_settings);

protected slots:
  void spin_loop();

protected:
  Ui::RqtPlansys2Knowledge ui_;
  QWidget * widget_;

private:
  QTimer * controller_spin_timer_;
  KnowledgeTree * knowledge_tree_;

  plansys2_msgs::msg::Knowledge::UniquePtr last_msg_;
  bool need_repaint_;

  void knowledge_callback(plansys2_msgs::msg::Knowledge::UniquePtr msg);
  rclcpp::Subscription<plansys2_msgs::msg::Knowledge>::SharedPtr knowledge_sub_;
  std::shared_ptr<plansys2::ProblemExpertClient> problem_;
};

}  // namespace rqt_plansys2_knowledge

#endif  // RQT_PLANSYS2_KNOWLEDGE__RQTKNOWLEDGE_HPP_
