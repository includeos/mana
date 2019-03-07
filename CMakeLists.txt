cmake_minimum_required(VERSION 3.0)
#TODO bump to a newer version that works with the below as minimum


set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

#get arch the proper cmake way
if (NOT DEFINED ARCH)
  set(ARCH ${CMAKE_HOST_SYSTEM_PROCESSOR})
endif()

add_definitions(-DARCH_${ARCH})
add_definitions(-DARCH="${ARCH}")

#to run outside conan
# the easy way
# mkdir build && cd build
# conan link .. mana/<version>@<user>/<channel> --layout=../layout.txt
# conan install .. --no-imports <if not default profile add -pr conan_profile>
# cmake ..
# make
# hard way
# create your own layout file and build out of tree in a different location
# endif

if (EXISTS ${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
  include(${CMAKE_CURRENT_BINARY_DIR}/conanbuildinfo.cmake)
  conan_basic_setup()
else()
  if (NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE Release)
  endif()
  if (CONAN_PROFILE)
    set(CONANPROFILE PROFILE ${CONAN_PROFILE})
  endif()
  if(NOT EXISTS "${CMAKE_BINARY_DIR}/conan.cmake")
     message(STATUS "Downloading conan.cmake from https://github.com/conan-io/cmake-conan")
     file(DOWNLOAD "https://github.com/conan-io/cmake-conan/raw/v0.13/conan.cmake"
                   "${CMAKE_BINARY_DIR}/conan.cmake")
  endif()
  include(${CMAKE_BINARY_DIR}/conan.cmake)
  conan_cmake_run(
    CONANFILE conanfile.py
    BASIC_SETUP
    ${CONANPROFILE}
  )
endif()

include_directories(${CMAKE_CURRENT_SOURCE_DIR}/include)

set(MANA_OBJ
  src/request.cpp
  src/response.cpp
  src/server.cpp
  )

set(MANA_COMP
  src/components/dashboard/dashboard.cpp
  )

set(MANA_MWARE
  src/middleware/butler.cpp
  src/middleware/director.cpp
  src/middleware/parsley.cpp
  src/middleware/cookie_parser.cpp
  )

set(MANA_ATTR
  src/attributes/cookie_jar.cpp
  )

add_library(mana STATIC ${MANA_OBJ} ${MANA_COMP} ${MANA_MWARE} ${MANA_ATTR})

install(TARGETS mana DESTINATION ${LIB_PREFIX}lib)
install(DIRECTORY include/mana DESTINATION ${INCLUDE_PREFIX}include)
