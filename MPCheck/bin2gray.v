`timescale 1ns/10ps

module bin2gray (
    B,
    G
);
// Gray encoder.
// 
// B -- binary input 
// G -- Gray encoded output
parameter width = 8;
input [width-1:0] B;
output [width-1:0] G;
wire [width-1:0] G;




assign G = ((B >>> 1) ^ B);

endmodule