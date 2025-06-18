import cocotb
from cocotb.clock import Clock
from random import randint, choice


from Drivers import packet_data, InputDriver, OutputMonitor, null_value32bit

@cocotb.test()
async def randomized_test(dut):
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())
    
    clk = dut.clk
    memory = {}  # SW model for memory

    # Instantiate drivers
    # OBS "" => start of the name of the bus: "mybus"
    # generate signals: mybus_wr, mybus_data, my_bus..
    input_drv  = InputDriver(dut, "", clk)
    output_mon = OutputMonitor(dut, clk)


    for cycle in range(360):
        is_write = choice([True, False])
        addr = randint(0, 255)
        data = randint(0, 2**32 - 1)

        pkg = packet_data(i_wr_en=is_write, i_addr=addr, i_data=data)

        # Send transaction
        await input_drv.send(pkg)

        if is_write:
            memory[addr] = data
            dut._log.info(f"[WRITE] Addr={addr},\t Data={data}")
        else:
            # READ: Wait for output data
            read_data = await output_mon.get_read_data()
            
            #SubCase: nothing added in the addr - returns 32'bx
            expected = memory.get(addr, null_value32bit)

            assert read_data == expected, f"[READ] Addr={addr},\
                                Expected={expected}, Got={read_data}"
            
            dut._log.info(f"[READ ] Addr={addr},\t Data={read_data}")
    dut._log.info("[END] Simulation Completed Successfully")