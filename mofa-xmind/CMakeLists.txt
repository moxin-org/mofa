# CMakeLists.txt : CMake project for xMind Project, include source and define
# project specific logic here.

cmake_minimum_required(VERSION 3.10)

# Project settings
project(xMindProject)

# Enable Hot Reload for MSVC compilers if supported
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT 
      "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,"
      "$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,"
      "$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()

# Output directories
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

if(MSVC)
    set(CMAKE_SHARED_LINKER_FLAGS_RELEASE "${CMAKE_SHARED_LINKER_FLAGS_RELEASE} /DEBUG /OPT:REF /OPT:ICF")
    set(CMAKE_EXE_LINKER_FLAGS_RELEASE "${CMAKE_EXE_LINKER_FLAGS_RELEASE} /DEBUG /OPT:REF /OPT:ICF")
endif()

# Add subdirectories
add_subdirectory("Main")
add_subdirectory("cli")
add_subdirectory("ThirdParty/xlang")

# Copy necessary directories to output
file(COPY "${PROJECT_SOURCE_DIR}/Service/" 
     DESTINATION "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Service")
file(COPY "${PROJECT_SOURCE_DIR}/Scripts/" 
     DESTINATION "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Scripts")
file(COPY "${PROJECT_SOURCE_DIR}/Config/" 
     DESTINATION "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Config")
file(COPY "${PROJECT_SOURCE_DIR}/Examples/" 
     DESTINATION "${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Examples")
