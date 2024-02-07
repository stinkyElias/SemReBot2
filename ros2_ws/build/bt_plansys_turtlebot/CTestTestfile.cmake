# CMake generated Testfile for 
# Source directory: /home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot
# Build directory: /home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(cppcheck "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/test_results/bt_plansys_turtlebot/cppcheck.xunit.xml" "--package-name" "bt_plansys_turtlebot" "--output-file" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/ament_cppcheck/cppcheck.txt" "--command" "/opt/ros/humble/bin/ament_cppcheck" "--xunit-file" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/test_results/bt_plansys_turtlebot/cppcheck.xunit.xml" "--include_dirs" "/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot/include")
set_tests_properties(cppcheck PROPERTIES  LABELS "cppcheck;linter" TIMEOUT "300" WORKING_DIRECTORY "/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_cppcheck/cmake/ament_cppcheck.cmake;66;ament_add_test;/opt/ros/humble/share/ament_cmake_cppcheck/cmake/ament_cmake_cppcheck_lint_hook.cmake;87;ament_cppcheck;/opt/ros/humble/share/ament_cmake_cppcheck/cmake/ament_cmake_cppcheck_lint_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;21;ament_execute_extensions;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_package.cmake;66;ament_execute_extensions;/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot/CMakeLists.txt;94;ament_package;/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot/CMakeLists.txt;0;")
add_test(lint_cmake "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/test_results/bt_plansys_turtlebot/lint_cmake.xunit.xml" "--package-name" "bt_plansys_turtlebot" "--output-file" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/ament_lint_cmake/lint_cmake.txt" "--command" "/opt/ros/humble/bin/ament_lint_cmake" "--xunit-file" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/test_results/bt_plansys_turtlebot/lint_cmake.xunit.xml")
set_tests_properties(lint_cmake PROPERTIES  LABELS "lint_cmake;linter" TIMEOUT "60" WORKING_DIRECTORY "/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_lint_cmake/cmake/ament_lint_cmake.cmake;47;ament_add_test;/opt/ros/humble/share/ament_cmake_lint_cmake/cmake/ament_cmake_lint_cmake_lint_hook.cmake;21;ament_lint_cmake;/opt/ros/humble/share/ament_cmake_lint_cmake/cmake/ament_cmake_lint_cmake_lint_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;21;ament_execute_extensions;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_package.cmake;66;ament_execute_extensions;/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot/CMakeLists.txt;94;ament_package;/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot/CMakeLists.txt;0;")
add_test(uncrustify "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/test_results/bt_plansys_turtlebot/uncrustify.xunit.xml" "--package-name" "bt_plansys_turtlebot" "--output-file" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/ament_uncrustify/uncrustify.txt" "--command" "/opt/ros/humble/bin/ament_uncrustify" "--xunit-file" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/test_results/bt_plansys_turtlebot/uncrustify.xunit.xml")
set_tests_properties(uncrustify PROPERTIES  LABELS "uncrustify;linter" TIMEOUT "60" WORKING_DIRECTORY "/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_uncrustify/cmake/ament_uncrustify.cmake;70;ament_add_test;/opt/ros/humble/share/ament_cmake_uncrustify/cmake/ament_cmake_uncrustify_lint_hook.cmake;43;ament_uncrustify;/opt/ros/humble/share/ament_cmake_uncrustify/cmake/ament_cmake_uncrustify_lint_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;21;ament_execute_extensions;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_package.cmake;66;ament_execute_extensions;/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot/CMakeLists.txt;94;ament_package;/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot/CMakeLists.txt;0;")
add_test(xmllint "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/test_results/bt_plansys_turtlebot/xmllint.xunit.xml" "--package-name" "bt_plansys_turtlebot" "--output-file" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/ament_xmllint/xmllint.txt" "--command" "/opt/ros/humble/bin/ament_xmllint" "--xunit-file" "/home/stinky/Documents/semantic-robot/ros2_ws/build/bt_plansys_turtlebot/test_results/bt_plansys_turtlebot/xmllint.xunit.xml")
set_tests_properties(xmllint PROPERTIES  LABELS "xmllint;linter" TIMEOUT "60" WORKING_DIRECTORY "/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_xmllint/cmake/ament_xmllint.cmake;50;ament_add_test;/opt/ros/humble/share/ament_cmake_xmllint/cmake/ament_cmake_xmllint_lint_hook.cmake;18;ament_xmllint;/opt/ros/humble/share/ament_cmake_xmllint/cmake/ament_cmake_xmllint_lint_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;21;ament_execute_extensions;/opt/ros/humble/share/ament_lint_auto/cmake/ament_lint_auto_package_hook.cmake;0;;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_execute_extensions.cmake;48;include;/opt/ros/humble/share/ament_cmake_core/cmake/core/ament_package.cmake;66;ament_execute_extensions;/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot/CMakeLists.txt;94;ament_package;/home/stinky/Documents/semantic-robot/ros2_ws/src/bt_plansys_turtlebot/CMakeLists.txt;0;")
