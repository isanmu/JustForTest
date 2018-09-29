module tb_sample_adc;

reg ad_trig;
reg clk_20M;
reg nRst;
reg ad_convert_done;
wire [3:0] outstate;

initial begin
    $from_myhdl(
        ad_trig,
        clk_20M,
        nRst,
        ad_convert_done
    );
    $to_myhdl(
        outstate
    );
end

sample_adc dut(
    ad_trig,
    clk_20M,
    nRst,
    ad_convert_done,
    outstate
);

endmodule
