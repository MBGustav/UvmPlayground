import cocotb
from cocotb.triggers import RisingEdge, ReadOnly
from cocotb.clock import Clock
from cocotb_bus.drivers import BusDriver
from dataclasses import dataclass
from random import randint, choice
from cocotb.binary import BinaryValue

null_value32bit = BinaryValue(32*'x', n_bits=32).binstr

# What we want to send to the DUT
@dataclass
class packet_data:
    i_wr_en: bool
    i_addr : int
    i_data : int = 0  # Only for writes


class InputDriver(BusDriver):
    #Declare Address and Data Inputs
    _signals = ["i_wr_en", "i_addr", "i_data" ]

    def __init__(self, dut, name, clk):
        super().__init__(dut, name, clk)
        self.clk = clk
        self.bus.i_wr_en.value = 0

    async def _driver_send(self, pkg: packet_data, sync = True):
        await RisingEdge(self.clk)
        print(f"Sending: {pkg}")
        await RisingEdge(self.clk)
        
        # Set the bus signals
        self.bus.i_wr_en.value = int(pkg.i_wr_en & 0x1)
        self.bus.i_data.value  = int(pkg.i_data  & 0xFFFFFFFF)
        self.bus.i_read_addr.value  = int(pkg.i_addr  & 0xFF)
        self.bus.i_wr_en.value = 0  # Desativa write

class OutputMonitor:
    _signals = ["o_data_ready", "o_data"]

    def __init__(self, dut, clk):
        self.dut = dut
        self.clk = clk

    async def get_read_data(self):
        while self.dut.o_data_ready.value != 1:
            await RisingEdge(self.clk)
        
        raw = self.dut.o_data.value

        if 'x' in raw.binstr or 'z' in raw.binstr:
            return null_value32bit
        return int(raw)

@cocotb.test()
async def memory_test(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    
    clk = dut.clk
    memory = {}  # SW model for comparison

    # Instantiate drivers
    input_drv = InputDriver(dut, "", clk)
    output_mon = OutputMonitor(dut, clk)


    for cycle in range(250):
        is_write = choice([True, False])
        addr = randint(0, 255)
        data = randint(0, 2**32 - 1)

        txn = packet_data(i_wr_en=is_write, i_addr=addr, i_data=data)

        # Send transaction
        await input_drv.send(txn)

        if is_write:
            memory[addr] = data
            dut._log.info(f"[WRITE] Addr={addr},\t Data={data}")
        else:
            # READ: Wait for output data
            read_data = await output_mon.get_read_data()
            #SubCase: nothing added in the addr - returns 32'bx
            expected = memory.get(addr, null_value32bit)

            assert str(read_data) == expected, f"[READ] Addr={addr}, Expected={expected}, Got={read_data}"
            dut._log.info(f"[READ ] Addr={addr},\t Data={read_data}")

    dut._log.info("Memory test PASSED!")


