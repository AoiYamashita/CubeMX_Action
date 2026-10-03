# CubeMX_Action
CubeMX Action for configuring a C++ project.  
It generates a C++-compatible Makefile and `main.cpp`.
> **Note:** Do not add a file extension when registering the Action in CubeMX.

# Usage
1. Add this repository to your CubeMX project directory.
2. In CubeMX, configure the following User Actions:
   - **Before Code Generation**
   - **After Code Generation**
> **Note:** Run `make clean` before switching from C to C++.
