# defaults
SIM ?= icarus
WAVES=1
TOPLEVEL_LANG ?= verilog

#export COCOTB_ENABLE_TRACE=0 
export COCOTB_LOG_LEVEL=INFO #(use DEBUG for more info)
VERILOG_SOURCES += $(wildcard $(PWD)/*.v)
# use VHDL_SOURCES for VHDL files


# TOPLEVEL: name of the toplevel - Verilog or VHDL file
TOPLEVEL=fifo

# MODULE: basename of Python file 
MODULE=coco_tb

all: project

project:
	rm -rf sim_build 
	$(MAKE) sim MODULE=$(MODULE) TOPLEVEL=$(TOPLEVEL)


# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim