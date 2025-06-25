import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, ReadOnly, Timer
from random import randint, choice

from Fifo import Fifo

from Drivers import packet_data, InputDriver, OutputMonitor, null_value32bit

def rnd_pkt():
    read = choice([True, False])
    write = not read #choice([True, False])
    data = (randint(0, 1 << 32 - 1))  # 32 bits
    return packet_data(write=write, read=read, data=data)


@cocotb.test()
async def rand_signals_testing(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    clk = dut.clk

    total_samples = 100
    len_fifo = 16
    len_data = 32

    #instantiate drivers
    in_drv  = InputDriver(dut, "", clk)
    out_mon = OutputMonitor(dut, "",clk)

    #Instantiate fifo (Sofware model)
    sw_fifo = Fifo(len_data=len_data, len_fifo=len_fifo)

    # Reset the FIFO and DUT
    dut._log.info("[INFO] Resetting DUT")
    await in_drv.reset()
    
    for cycle in range(total_samples):
        pkg = rnd_pkt()
        dut._log.debug(f"Cycle {cycle}: Sending packet: {pkg}")
        
        # Send the packet to the DUT and read
        await in_drv.send(pkg)
        expected = sw_fifo.send(pkg) #software FIFO
        data, signals = await out_mon.read()

        if pkg.write:
            dut._log.debug(f"[DGB/WRITE] Data={pkg.data}")

        if pkg.read:
            dut._log.debug(f"[DGB/READ] empty={signals['empty']}, len={signals['len']}")
            expected = null_value32bit if expected is None else expected
            assert data == expected, f"[READ] Expected={expected}, Got={data}"

        # Check control signals
        for dut_attr, fifo_attr in zip(signals.items(), sw_fifo.get_signals().items()):
            assert dut_attr == fifo_attr, f"Control signal mismatch: {dut_attr} != {fifo_attr}"
