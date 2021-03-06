`timescale 1ns/10ps

module bin2gray(B, G);

   parameter width = 8;
   input [width-1:0]  B;
   output [width-1:0] G;

   assign G = B[0]; //(B >> 1) ^ B;

endmodule // bin2gray