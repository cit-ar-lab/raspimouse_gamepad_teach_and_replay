cmake_minimum_required(VERSION 2.8.3)
project(raspimouse_gamepad_teach_and_replay)

set(CMAKE_CXX_FLAGS "-std=c++0x ${CMAKE_CXX_FLAGS}")

find_package(catkin REQUIRED COMPONENTS
  rosbag
  roslib
  roscpp
  rospy
  std_msgs
  message_generation
)

add_message_files(
  FILES
  Event.msg
  PFoEOutput.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
)

catkin_package(
  CATKIN_DEPENDS roscpp rospy std_msgs
)

include_directories(
  ${catkin_INCLUDE_DIRS}
)

add_library(${PROJECT_NAME}_Observation src/Observation.cpp)
add_library(${PROJECT_NAME}_Event src/Event.cpp)
add_library(${PROJECT_NAME}_ParticleFilter src/ParticleFilter.cpp)
add_library(${PROJECT_NAME}_Episodes src/Episodes.cpp)
add_library(${PROJECT_NAME}_Particle src/Particle.cpp)

add_executable(${PROJECT_NAME}_replay src/replay.cpp)

add_dependencies(${PROJECT_NAME}_replay ${TARGET_NAME} ${PROJECT_NAME}_generate_messages_cpp)
add_dependencies(${PROJECT_NAME}_replay ${TARGET_NAME} raspimouse_ros_2_generate_messages_cpp)
add_dependencies(${PROJECT_NAME}_ParticleFilter ${TARGET_NAME} ${PROJECT_NAME}_generate_messages_cpp)
add_dependencies(${PROJECT_NAME}_ParticleFilter ${TARGET_NAME} raspimouse_ros_2_generate_messages_cpp)

target_link_libraries(${PROJECT_NAME}_replay ${catkin_LIBRARIES})
target_link_libraries(${PROJECT_NAME}_replay ${PROJECT_NAME}_Observation ${catkin_LIBRARIES})
target_link_libraries(${PROJECT_NAME}_replay ${PROJECT_NAME}_Event ${catkin_LIBRARIES})
target_link_libraries(${PROJECT_NAME}_replay ${PROJECT_NAME}_Episodes ${catkin_LIBRARIES})
target_link_libraries(${PROJECT_NAME}_replay ${PROJECT_NAME}_ParticleFilter ${catkin_LIBRARIES})
target_link_libraries(${PROJECT_NAME}_replay ${PROJECT_NAME}_Particle ${catkin_LIBRARIES})

set_target_properties(${PROJECT_NAME}_replay PROPERTIES OUTPUT_NAME replay PREFIX "")