module memory (
    input             clk, 
    input             i_wr_en,
    input      [ 7:0] i_addr,
    input      [31:0] i_data,
    output reg [31:0] o_data
);
//# OBS addr size depends on ram size:
//# 256 -> 2 ^8, where 256 \is the ram size, 
    reg [31:0] MEM [255:0];

    always @(posedge clk) begin
        if(i_wr_en) 
            MEM[i_addr] <= i_data;
        else
            o_data <= MEM[i_addr];
    end

endmodule