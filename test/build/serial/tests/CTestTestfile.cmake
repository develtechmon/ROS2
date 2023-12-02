# CMake generated Testfile for 
# Source directory: /home/jlukas/My_Project/ROS2/test/src/serial/tests
# Build directory: /home/jlukas/My_Project/ROS2/test/build/serial/tests
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(serial-test "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/jlukas/My_Project/ROS2/test/build/serial/test_results/serial/serial-test.gtest.xml" "--package-name" "serial" "--output-file" "/home/jlukas/My_Project/ROS2/test/build/serial/ament_cmake_gtest/serial-test.txt" "--command" "/home/jlukas/My_Project/ROS2/test/build/serial/tests/serial-test" "--gtest_output=xml:/home/jlukas/My_Project/ROS2/test/build/serial/test_results/serial/serial-test.gtest.xml")
set_tests_properties(serial-test PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/jlukas/My_Project/ROS2/test/build/serial/tests/serial-test" TIMEOUT "60" WORKING_DIRECTORY "/home/jlukas/My_Project/ROS2/test/build/serial/tests" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/jlukas/My_Project/ROS2/test/src/serial/tests/CMakeLists.txt;5;ament_add_gtest;/home/jlukas/My_Project/ROS2/test/src/serial/tests/CMakeLists.txt;0;")
add_test(serial-test-timer "/usr/bin/python3.10" "-u" "/opt/ros/humble/share/ament_cmake_test/cmake/run_test.py" "/home/jlukas/My_Project/ROS2/test/build/serial/test_results/serial/serial-test-timer.gtest.xml" "--package-name" "serial" "--output-file" "/home/jlukas/My_Project/ROS2/test/build/serial/ament_cmake_gtest/serial-test-timer.txt" "--command" "/home/jlukas/My_Project/ROS2/test/build/serial/tests/serial-test-timer" "--gtest_output=xml:/home/jlukas/My_Project/ROS2/test/build/serial/test_results/serial/serial-test-timer.gtest.xml")
set_tests_properties(serial-test-timer PROPERTIES  LABELS "gtest" REQUIRED_FILES "/home/jlukas/My_Project/ROS2/test/build/serial/tests/serial-test-timer" TIMEOUT "60" WORKING_DIRECTORY "/home/jlukas/My_Project/ROS2/test/build/serial/tests" _BACKTRACE_TRIPLES "/opt/ros/humble/share/ament_cmake_test/cmake/ament_add_test.cmake;125;add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest_test.cmake;86;ament_add_test;/opt/ros/humble/share/ament_cmake_gtest/cmake/ament_add_gtest.cmake;93;ament_add_gtest_test;/home/jlukas/My_Project/ROS2/test/src/serial/tests/CMakeLists.txt;12;ament_add_gtest;/home/jlukas/My_Project/ROS2/test/src/serial/tests/CMakeLists.txt;0;")
subdirs("../gtest")
