module tb_m_ex1;

reg clk;
reg [7:0] xyz_x;
reg [3:0] xyz_y;
wire [8:0] xyz_z;

initial begin
    $from_myhdl(
        clk,
        xyz_x,
        xyz_y
    );
    $to_myhdl(
        xyz_z
    );
end

m_ex1 dut(
    clk,
    xyz_x,
    xyz_y,
    xyz_z
);

endmodule
