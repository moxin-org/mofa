# CMakeList.txt : CMake project for xMind-Cli, include source and define
# project specific logic here.
#
cmake_minimum_required(VERSION 3.10)
project ("xmcli")

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

include_directories("../ThirdParty/xlang/Api")
include_directories("../Inc")

FILE(GLOB Xlang_Api_SRC "../ThirdParty/xlang/Api/*.cpp")
FILE(GLOB AppEntry_SRC "Main.cpp")


file(COPY "${PROJECT_SOURCE_DIR}/Scripts/" DESTINATION "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Scripts")

add_executable (${PROJECT_NAME}
	${Xlang_Api_SRC}
	${AppEntry_SRC}
)

 