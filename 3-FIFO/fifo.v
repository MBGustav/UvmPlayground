module fifo #(
    parameter len_data = 32,
    parameter len_fifo = 16,
    localparam bit_len = $clog2(len_fifo)
)(
    input                  clk,
    input                  rst_n,
    input                  i_write,
    input                  i_read,   
    input  [len_data-1:0]  i_data,
    output [len_data-1:0]  o_data,
    output                 o_empty, o_full,
    output [bit_len:0]     dbg_counter // dbg purposes
);

    reg [len_data-1:0] fifo_mem [0:len_fifo-1];
    reg [$clog2(len_fifo):0] wr_ptr=0, rd_ptr=0, count=0;

    assign o_data  = (count > 0) ? fifo_mem[rd_ptr] : {len_data{1'b0}};
    assign o_empty = (count == 0);
    assign o_full  = (count >= len_fifo);
    assign dbg_counter = count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            wr_ptr <= 0;
            rd_ptr <= 0;
            count  <= 0;
        end else begin
            // i_write operation
            if (i_write && !o_full) begin
                fifo_mem[wr_ptr] <= i_data;
                wr_ptr <= (wr_ptr + 1) % len_fifo;
                count  <= count + 1;
            end
            // i_read operation
            if (i_read && !o_empty) begin
                rd_ptr <= (rd_ptr + 1) % len_fifo;
                count  <= count - 1;
            end
        end
    end


    initial begin
        $dumpfile("dump.vcd");
        $dumpvars(1,fifo);
    end


endmodule
