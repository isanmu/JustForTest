`timescale 1ns/10ps
module dut_bin2gray;

//   reg [`width-1:0] B;
//   wire [`width-1:0] G;
    reg [8-1:0] B;
   wire [8-1:0] G;

   initial begin
       $dumpfile("hello.vcd");
       $dumpvars(0, dut_bin2gray);
       $display("hello");
       #100;
       B = 6;
       #100;
       $finish;
//       $from_myhdl(B);
//       $to_myhdl(G);
   end

   bin2gray dut (.B(B), .G(G));
//   defparam dut.width = `width;

endmodule