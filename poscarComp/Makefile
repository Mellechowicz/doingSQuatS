#local path to spglib and XtalComp libraries

ifdef PATHTOLOCAL
   $(info Path to XtalComp and spglib is extenally defined as PATHTOLOCAL = $(PATHTOLOCAL)) 
else
   PATHTOLOCAL=$(shell dirname $(realpath $(firstword $(MAKEFILE_LIST))))/.local
   $(info Path to XtalComp and spglib is defined as PATHTOLOCAL = $(PATHTOLOCAL)) 
endif

# Compilators
CXX    = g++
CXXFLAGS = -std=c++20 -O3 -Wall -pedantic

INCLUDES = -I $(PATHTOLOCAL)/include

# Verbose
# If verbose mode is needed please use:
# make V=-D[verbose flag] instead of make
V = #-D_DEBUG

# Linking
STATIC = $(PATHTOLOCAL)/lib/libXtalComp.a $(PATHTOLOCAL)/lib/libsymspg.a -fopenmp
LFLAGS = -larmadillo $(STATIC) -fopenmp
 
# File names
EXEC = poscar_compare

# Sources
CXX_SOURCES = $(wildcard *.cpp)
CXX_OBJECTS = $(CXX_SOURCES:.cpp=.o)
 
#+++++++++++++++++++#
# COMPILATION RULES #
#+++++++++++++++++++#

# Main target
$(EXEC):  $(CXX_OBJECTS)
	$(CXX) $(CXX_OBJECTS) -o $(EXEC) $(LDPATH) $(LFLAGS)
 
# Other targets 
%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) $V -c $< -o $@
 
# Cleaning
clean:
	rm -f $(EXEC) $(CXX_OBJECTS)

# ExecCleaning
cleanexec:
	rm -f $(EXEC)

# all
all: clean $(EXEC)

# redo linking
link: cleanexec $(EXEC)
