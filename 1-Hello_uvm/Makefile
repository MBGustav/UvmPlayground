# defaults
SIM ?= icarus
WAVES=1
TOPLEVEL_LANG ?= verilog

export COCOTB_ENABLE_TRACE=1

VERILOG_SOURCES += $(wildcard $(PWD)/*.v)
# use VHDL_SOURCES for VHDL files


# TOPLEVEL: name of the toplevel - Verilog or VHDL file
TOPLEVEL=XOR_module

# MODULE: basename of Python file 
MODULE=hello_uvm

all: project

project:
	rm -rf sim_build 
	$(MAKE) sim MODULE=$(MODULE) TOPLEVEL=$(TOPLEVEL)



# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim