from cocotb.triggers import RisingEdge

from cocotb_bus.drivers import BusDriver
from dataclasses import dataclass

from cocotb.binary import BinaryValue

null_value32bit = BinaryValue(32*'x', n_bits=32).binstr

# What we want to send to the DUT
@dataclass
class packet_data:
    i_wr_en: bool
    i_addr: int
    i_data: int = 0  # Only for writes


class InputDriver(BusDriver):
    #Declare Address and Data Inputs
    _signals = ["i_wr_en", "i_addr", "i_data"]

    def __init__(self, dut, name, clk):
        super().__init__(dut, name, clk)
        self.clk = clk
        #self.bus.i_wr_en.value = 0

    async def _driver_send(self, pkg: packet_data, sync = True):
        self.bus.i_addr.value  = int(pkg.i_addr)
        self.bus.i_wr_en.value = int(pkg.i_wr_en)
        self.bus.i_data.value  = int(pkg.i_data)
        await RisingEdge(self.clk)
        self.bus.i_wr_en.value = 0  # Desativa write

    
class OutputMonitor:
    def __init__(self, dut, clk):
        self.dut = dut
        self.clk = clk

    async def get_read_data(self):
        await RisingEdge(self.clk)
        raw = self.dut.o_data.value
        if 'x' in raw.binstr or 'z' in raw.binstr:
            return null_value32bit
        
        return int(raw)
