cmake_minimum_required(VERSION 3.5)

project(zenoh-cpp)

find_package(ament_cmake REQUIRED)
find_package(libzenohc REQUIRED)

add_executable(zenoh-cpp
  src/main.cpp
)
target_link_libraries(zenoh-cpp
  ${zenohc_LIBRARIES}
)
target_include_directories(zenoh-cpp
  PUBLIC
    ${zenohc_INCLUDE_DIRECTORIES}
)

install(
  TARGETS zenoh-cpp
  RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
  LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
  ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

ament_package()
