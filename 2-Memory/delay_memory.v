module delay_memory (
    input         clk, 
    //input Ports - addr | data
    input         i_wr_en,
    input  [ 7:0] i_read_addr,
    input  [ 7:0] i_write_addr,
    input  [31:0] i_data,
    output        o_data_ready, 
    output [31:0] o_data
);
//# OBS addr size depends on ram size:
//# 256 -> 2 ^8, where 256 is the ram size, 
//# and 8 equals to the bits required to address all pos.
    reg [31:0] MEM [255:0];

    localparam READ_DELAY = 3;
    reg [32:0] fifo_read [READ_DELAY-1:0]; // {data, done_sgn}


    always @(posedge clk) begin
        if(i_wr_en) begin
            MEM[i_write_addr] <= i_data;              //#write
            fifo_read[0] <= {32'bx, 1'b0};            // not read
        end else begin
            fifo_read[0] <= {MEM[i_read_addr], 1'b1}; //read
        end
    end

// Lets add some delay on read operation, making things more interesting... :)
    integer i;
    always @(posedge clk) begin
        for(i = 1; i < READ_DELAY; i = i + 1) begin
            fifo_read[i] <= fifo_read[i - 1];
        end
    end

    assign {o_data, o_data_ready} = fifo_read[READ_DELAY-1];

//Initialize fifo as zero
    integer itr;
    initial begin
        for(itr = 0; itr < READ_DELAY; itr = itr + 1)
            fifo_read[itr] = {32'bx,1'b0};
    end


endmodule