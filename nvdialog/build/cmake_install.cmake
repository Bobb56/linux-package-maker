# Install script for directory: /home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set path to fallback-tool for dependency-resolution.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/lib" TYPE STATIC_LIBRARY FILES "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/build/libnvdialog.a")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/nvdialog" TYPE FILE FILES
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/nvdialog_dialog.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/nvdialog_notification.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/nvdialog_core.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/nvdialog_capab.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/nvdialog_types.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/nvdialog_error.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/nvdialog_platform.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/nvdialog_image.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/nvdialog_string.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/nvdialog.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/include/nvdialog/dialogs" TYPE FILE FILES
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/dialogs/nvdialog_file_dialog.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/dialogs/nvdialog_about_dialog.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/dialogs/nvdialog_dialog_box.h"
    "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/include/dialogs/nvdialog_input_box.h"
    )
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  list(APPEND CMAKE_ABSOLUTE_DESTINATION_FILES
   "/usr/local/share/pkgconfig/nvdialog.pc")
  if(CMAKE_WARN_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(WARNING "ABSOLUTE path INSTALL DESTINATION : ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  if(CMAKE_ERROR_ON_ABSOLUTE_INSTALL_DESTINATION)
    message(FATAL_ERROR "ABSOLUTE path INSTALL DESTINATION forbidden (by caller): ${CMAKE_ABSOLUTE_DESTINATION_FILES}")
  endif()
  file(INSTALL DESTINATION "/usr/local/share/pkgconfig" TYPE FILE FILES "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/build/nvdialog.pc")
endif()

string(REPLACE ";" "\n" CMAKE_INSTALL_MANIFEST_CONTENT
       "${CMAKE_INSTALL_MANIFEST_FILES}")
if(CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/build/install_local_manifest.txt"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
if(CMAKE_INSTALL_COMPONENT)
  if(CMAKE_INSTALL_COMPONENT MATCHES "^[a-zA-Z0-9_.+-]+$")
    set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INSTALL_COMPONENT}.txt")
  else()
    string(MD5 CMAKE_INST_COMP_HASH "${CMAKE_INSTALL_COMPONENT}")
    set(CMAKE_INSTALL_MANIFEST "install_manifest_${CMAKE_INST_COMP_HASH}.txt")
    unset(CMAKE_INST_COMP_HASH)
  endif()
else()
  set(CMAKE_INSTALL_MANIFEST "install_manifest.txt")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  file(WRITE "/home/rlpuillandre/Documents/Projets fun/Linux-Package-Maker/nvdialog/build/${CMAKE_INSTALL_MANIFEST}"
     "${CMAKE_INSTALL_MANIFEST_CONTENT}")
endif()
