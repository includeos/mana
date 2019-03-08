cmake_minimum_required(VERSION 3.8.0)

project (mana_simple C CXX)

include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake OPTIONAL RESULT_VARIABLE HAS_CONAN)
if (NOT HAS_CONAN)
  message(FATAL_ERROR "missing conanbuildinfo.cmake did you forget to run conan install ?")
endif()
conan_basic_setup()

include(os)

os_add_executable(mana_simple "Mana Simple Example" service.cpp)
os_add_drivers(mana_simple virtionet)
