# CMakeLists.txt : CMake project for xMind Project, include source and define
# project specific logic here.

cmake_minimum_required(VERSION 3.10)

# Project settings
project(xMind)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)
# Include directories
include_directories(
  "../ThirdParty/xlang/Api"
  "Inc"
  "Common"
  "Log"
  "."
  "Executor"
  "AgentGraph"

)

# Source files
file(GLOB Xlang_Api_SRC "../ThirdParty/xlang/Api/*.cpp")
file(GLOB AppEntry_SRC "*.cpp" "Executor/*.cpp")
file(GLOB Common_SRC "Common/*.cpp" "Log/*.cpp" "AgentGraph/*.cpp")

# Add executable
add_executable(${PROJECT_NAME}
  ${Xlang_Api_SRC}
  ${Common_SRC}
  ${AppEntry_SRC})

if(APPLE)
target_link_libraries(xMind PUBLIC "-framework CoreFoundation")
endif()
