cmake_minimum_required(VERSION 3.1.0)

project(unittests C CXX)

enable_testing(ON)

set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

option(COVERAGE "Build with coverage generation" ON)
option(BUILD_MISSING "Build missing conan dependencies" OFF)
option(UPDATE "Force conan to search repo for newer packages" OFF)

if ("${ARCH}" STREQUAL "")
  message(STATUS "CMake detected host arch: ${CMAKE_HOST_SYSTEM_PROCESSOR}")
  set (ARCH ${CMAKE_HOST_SYSTEM_PROCESSOR})
endif("${ARCH}" STREQUAL "")

#can we get rid of these ?
add_definitions(-DARCH_${ARCH})
add_definitions(-DARCH="${ARCH}")

if(NOT CONAN_EXPORTED)
  if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
     message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
     file(DOWNLOAD "https://raw.githubusercontent.com/conan-io/cmake-conan/develop/conan.cmake"
                    "${CMAKE_BINARY_DIR}/conan.cmake")
  endif()
  include(${CMAKE_BINARY_DIR}/conan.cmake)
  if (CONAN_PROFILE)
    set(CONANPROFILE PROFILE ${CONAN_PROFILE})
  endif()
  if (UPDATE)
    set(CONAN_UPDATE UPDATE)
  endif()

  if (BUILD_MISSING)
    set(CONAN_BUILD "BUILD" "missing")
  endif()
  #not sure this is sane with respect to dependencies on includeos headers
  conan_cmake_run(
    CONANFILE conanfile.txt
    BASIC_SETUP
    ${CONAN_UPDATE}
    ${CONAN_BUILD}
    ${CONANPROFILE}
  )
endif()

#include_directories(../include)

#set(MANA_SOURCES
#  ../src/middleware/butler.cpp
#)

#add_library(mana ${MANA_SOURCES})


SET(TEST_SOURCES
  dummy.cpp
)

foreach(T ${TEST_SOURCES})

  #get the filename witout extension
  get_filename_component(NAME ${T} NAME_WE)
  add_executable(${NAME} ${T})
  target_link_libraries(${NAME} m stdc++)
  add_test(${NAME} bin/${NAME} -p )

  #add to list of tests for dependencies
  list(APPEND TEST_BINARIES ${NAME})
endforeach()
