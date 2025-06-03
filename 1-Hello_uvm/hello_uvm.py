import cocotb
from cocotb.clock import Timer
from random import randint


def gen_random_inputs():
    in_a = randint(0, 15) # 4 bits
    in_b = randint(0, 15) # 4 bits
    out_y = in_a ^ in_b
    return (in_a, in_b, out_y)

@cocotb.test()
async def directed_test(dut):

    #we set the known cases
    known_cases = [
        (0b0000, 0b0000, 0b0000),
        (0b0101, 0b1010, 0b1111),
        (0b0001, 0b1000, 0b1001)
    ]

    for case in known_cases:
        a_in, b_in, exp_out = case

        dut.a.value = int(a_in)
        dut.b.value = int(b_in)
        await Timer(1, 'ns')

        assert dut.y.value == exp_out, 'f[ERROR] Y={dut.y.value}, Expected={exp_out}'
        dut._log.info(f'[INFO] {dut.y.value}={dut.a.value}^{dut.b.value}')


@cocotb.test()
async def random_test(dut):

    # defining a number of tests
    num_tests = 1024

    #iterate over the tests
    for test in range(num_tests):
        a, b, expect = gen_random_inputs()
        dut.a.value = int(a)
        dut.b.value = int(b)
        await Timer(1, 'ns')

        assert dut.y.value == expect, 'f[ERROR] Y={dut.y.value}, Expected={expect}'
        dut._log.info(f'[INFO] {dut.y.value}={dut.a.value} ^ {dut.b.value}')



