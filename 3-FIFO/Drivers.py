
import cocotb
from cocotb.triggers import RisingEdge, ReadOnly
from cocotb.clock import Clock
from cocotb_bus.drivers import BusDriver
from dataclasses import dataclass
from random import randint, choice
from cocotb.binary import BinaryValue

null_value32bit = BinaryValue(32*'x', n_bits=32).binstr


#defining the packet
@dataclass
class  packet_data:
    write : bool
    read  : bool
    data  : int



class InputDriver(BusDriver):
    _signals = ["i_write", "i_read", "i_data", "rst_n"]


    def __init__(self, dut, name, clk):
        super().__init__(dut, name, clk)
        self.clk = clk

        
    
    async def _driver_send(self, pkg: packet_data, sync=True):
        #set the values in the interface
        await RisingEdge(self.clk)
        self.bus.i_write.value = int(pkg.write)
        self.bus.i_read.value  = int(pkg.read)
        self.bus.i_data.value  = int(pkg.data)
        self.bus.rst_n = 1  # Ensure reset is not active
        await RisingEdge(self.clk)

    async def reset(self):
        # Reset the DUT
        # set input signals to 0
        for sgn in self._signals:
            getattr(self.bus, sgn).value = 0

        await RisingEdge(self.clk)
        self.bus.rst_n.value = 1
        await RisingEdge(self.clk)


class OutputMonitor:
    #output signals
    def __init__(self, dut, name, clk):
        self.dut = dut
        self.name = name
        self.clk = clk

    async def read_data(self):
        if self.dut.o_empty.value == 1:
            return null_value32bit # fifo empty
        # else, read the data
        #self.dut.i_read.value = 1
        raw = self.dut.o_data.value

        if 'x' in raw.binstr or 'z' in raw.binstr:
            return null_value32bit    
        return int(raw)
    
    async def read_signals(self):
        
        await ReadOnly()  # wait for the read mode to be stable
        signals = {
            "empty": bool(self.dut.o_empty.value),
            "full": bool(self.dut.o_full.value),
            "len": int(self.dut.dbg_counter.value)
        }

        for key, val in signals.items():
            if hasattr(val, "binstr") and ('x' in val.binstr or 'z' in val.binstr):
                signals[key] = 'x'
        return signals
    
    
    async def read(self):
        signals = await self.read_signals()
        data = await self.read_data()
        return data, signals