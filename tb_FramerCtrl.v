module tb_FramerCtrl;

wire SOF;
wire [1:0] state;
reg syncFlag;
reg clk;
reg reset_n;
reg [3:0] B;
wire [3:0] G;
wire [3:0] G2;

initial begin
    $from_myhdl(
        syncFlag,
        clk,
        reset_n,
        B
    );
    $to_myhdl(
        SOF,
        state,
        G,
        G2
    );
end

FramerCtrl dut(
    SOF,
    state,
    syncFlag,
    clk,
    reset_n,
    B,
    G,
    G2
);

endmodule
