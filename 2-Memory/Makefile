# defaults
SIM ?= icarus
WAVES=1
TOPLEVEL_LANG ?= verilog

export COCOTB_ENABLE_TRACE=1

# use VHDL_SOURCES for VHDL files
VERILOG_SOURCES += $(PWD)/delay_memory.v
VERILOG_SOURCES += $(PWD)/memory.v


# TOPLEVEL: name of the toplevel - Verilog or VHDL file
# MODULE: basename of Python file 

delay_memory:
	rm -rf sim_build 
	$(MAKE) sim MODULE=delay_tb TOPLEVEL=delay_memory


memory:
	rm -rf sim_build 
	$(MAKE) sim MODULE=mem_tb TOPLEVEL=memory

# include cocotb's make rules to take care of the simulator setup
include $(shell cocotb-config --makefiles)/Makefile.sim