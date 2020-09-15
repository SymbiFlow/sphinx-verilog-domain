verilog:port
************

.. verilog:port:: input [0:1]                port_name_01;
.. verilog:port:: input                      port_name_02 [0:1];
.. verilog:port:: input [0:1]                port_name_03 [0:1];
.. verilog:port:: input [0:1]                port_name_04 [0:1], other_name_04;
.. verilog:port:: input [0:1] other_name_05, port_name_05 [0:1];
.. verilog:port:: input [0:1]                port_name_06 [0:1], other_name_06 [0:1];
.. verilog:port:: input[0:1]port_name_07[0:1],other_name_07[0:1];
.. verilog:port:: input [ 0 : 1 ] port_name_08 [ 0 : 1 ] , other_name_08 [ 0 : 1 ] ;

...............................................................................

.. verilog:port:: input [CONST/(2 * a)]                port_name_12;
.. verilog:port:: input                                port_name_13 [CONST/(2 * a)];
.. verilog:port:: input [CONST/(2 * a)]                port_name_14 [CONST/(2 * a)];
.. verilog:port:: input [CONST/(2 * a)]                port_name_15 [CONST/(2 * a)], other_name_15;
.. verilog:port:: input [CONST/(2 * a)] other_name_16, port_name_16 [CONST/(2 * a)];
.. verilog:port:: input [CONST/(2 * a)]                port_name_17 [CONST/(2 * a)], other_name_17 [CONST/(2 * a)];
.. verilog:port:: input[CONST/(2*a)]port_name_18[CONST/(2*a)],other_name_18[CONST/(2*a)];
.. verilog:port:: input [ CONST / (2 * a) ] port_name_19 [ CONST / (2 * a) ] , other_name_19 [ CONST / (2 * a) ] ;

...............................................................................

.. verilog:port:: input []                port_name_23;
.. verilog:port:: input                   port_name_24 [];
.. verilog:port:: input []                port_name_25 [];
.. verilog:port:: input []                port_name_26 [], other_name_26;
.. verilog:port:: input [] other_name_27, port_name_27 [];
.. verilog:port:: input []                port_name_28 [], other_name_28 [];
.. verilog:port:: input[]port_name_29[],other_name_29[];
.. verilog:port:: input [ ] port_name_30 [ ] , other_name_30 [ ] ;

...............................................................................

.. verilog:port:: input [0:1][2:3]                port_name_34;
.. verilog:port:: input                           port_name_35 [0:1][2:3];
.. verilog:port:: input [0:1][2:3]                port_name_36 [0:1][2:3];
.. verilog:port:: input [0:1][2:3]                port_name_37 [0:1][2:3], other_name_37;
.. verilog:port:: input [0:1][2:3] other_name_38, port_name_38 [0:1][2:3];
.. verilog:port:: input [0:1][2:3]                port_name_39 [0:1][2:3], other_name_39 [0:1][2:3];
.. verilog:port:: input[0:1][2:3]port_name_40[0:1][2:3],other_name_40[0:1][2:3];
.. verilog:port:: input [ 0 : 1 ] [ 2 : 3 ] port_name_41 [ 0 : 1 ] [ 2 : 3 ] , other_name_41 [ 0 : 1 ] [ 2 : 3 ] ;

...............................................................................

.. verilog:port:: input [0] [CONST/(2 * a) : 4]                port_name_45;
.. verilog:port:: input                                        port_name_46 [0][CONST/(2 * a) : 4];
.. verilog:port:: input [0] [CONST/(2 * a) : 4]                port_name_47 [0][CONST/(2 * a) : 4];
.. verilog:port:: input [0] [CONST/(2 * a) : 4]                port_name_48 [0][CONST/(2 * a) : 4], other_name_48;
.. verilog:port:: input [0] [CONST/(2 * a) : 4] other_name_49, port_name_49 [0][CONST/(2 * a) : 4];
.. verilog:port:: input [0] [CONST/(2 * a) : 4]                port_name_50 [0][CONST/(2 * a) : 4], other_name_50 [0][CONST/(2 * a) : 4];
.. verilog:port:: input[0][CONST/(2*a):4]port_name_51[0][CONST/(2*a):4],other_name_51[0][CONST/(2*a):4];
.. verilog:port:: input [ 0 ] [ CONST / (2 * a) : 4 ] port_name_52 [ 0 ] [ CONST / (2 * a) : 4 ] , other_name_52 [ 0 ] [ CONST / (2 * a) : 4 ] ;

...............................................................................

.. verilog:port:: input [0] [CONST/(2 * a)][]                port_name_56;
.. verilog:port:: input                                      port_name_57 [0][CONST/(2 * a)][];
.. verilog:port:: input [0] [CONST/(2 * a)][]                port_name_58 [0][CONST/(2 * a)][];
.. verilog:port:: input [0] [CONST/(2 * a)][]                port_name_59 [0][CONST/(2 * a)][], other_name_59;
.. verilog:port:: input [0] [CONST/(2 * a)][] other_name_60, port_name_60 [0][CONST/(2 * a)][];
.. verilog:port:: input [0] [CONST/(2 * a)][]                port_name_61 [0][CONST/(2 * a)][], other_name_61 [0][CONST/(2 * a)][];
.. verilog:port:: input[0][CONST/(2*a)][]port_name_62[0][CONST/(2*a)][],other_name_62[0][CONST/(2*a)][];
.. verilog:port:: input [ 0 ] [ CONST / (2 * a) ] [ ] port_name_63 [ 0 ] [ CONST / (2 * a) ] [ ] , other_name_63 [ 0 ] [ CONST / (2 * a) ] [ ] ;

...............................................................................

.. verilog:port:: (* $flowmap_level = 1 * 2, attr = 4 *) input  wire [  DATA_WIDTH - 1:0  ] a1, b1, c1;
.. verilog:port:: (* $flowmap_level=1 *) input a2;
.. verilog:port:: (*$flowmap_level=1*) input \esc{aped[]tok()en ;
.. verilog:port:: inout       fbmimicbidir;
.. verilog:port:: inout DDRCASB;
.. verilog:port:: inout [width_b-1:0] q_b;
.. verilog:port:: inout wire  PACKAGE_PIN;
.. verilog:port:: input		DataOut_i;
.. verilog:port:: input		clk, kld;
.. verilog:port:: input	wire	[31:0]	a3, b2;
.. verilog:port:: input                                    configupdate;
.. verilog:port:: input                         dataa, datab, datac, datad;
.. verilog:port:: input                    cam_enable;
.. verilog:port:: input                  A1EN;
.. verilog:port:: input   clock,reset,req_0,req_1;
.. verilog:port:: input  B1EN;
.. verilog:port:: input  [7:0] tx_data        ;
.. verilog:port:: input  [SIZE-1:0]  state ;
.. verilog:port:: input  enable ;
.. verilog:port:: input  in;
.. verilog:port:: input  wire I;
.. verilog:port:: input  wire [7:0] inp_b;
.. verilog:port:: input  wire [WIDTH-1:0] I;
.. verilog:port:: input  wire clk;
.. verilog:port:: input Data0, Data1, Data2, Data3, Data4, Data5, Data6, Data7, Data8, Data9, Data10, Data11, Data12, Data13, Data14, Data15, Data16, Data17, Data18, Data19, Data20, Data21, Data22, Data23, Data24, Data25, Data26, Data27, Data28, Data29, Data30, Data31, Data32, Data33, Data34, Data35, Data36, Data37, Data38, Data39, Data40, Data41, Data42, Data43, Data44, Data45, Data46, Data47, Data48, Data49, Data50, Data51, Data52, Data53, Data54, Data55, Data56, Data57, Data58, Data59, Data60, Data61, Data62, Data63;
.. verilog:port:: input [width_clock-1:0] clk;
.. verilog:port:: input clock ;
.. verilog:port:: input clk;
.. verilog:port:: input cl$k, \reset* ;
.. verilog:port:: input data, clk, reset ;
.. verilog:port:: input data_in ;
.. verilog:port:: input din_0, din_1, sel ;
.. verilog:port:: input enable ;
.. verilog:port:: input integer a, b;
.. verilog:port:: input m_eth_payload_axis_tready;
.. verilog:port:: input reg [11:0] zero2;
.. verilog:port:: input reg zero1;
.. verilog:port:: input req_3 ;
.. verilog:port:: input reset   ;
.. verilog:port:: input signed      wire4;
.. verilog:port:: input signed [(B_WIDTH - 1):0] b;
.. verilog:port:: input wire				ci;
.. verilog:port:: input wire 		  S;
.. verilog:port:: input wire  D_OUT_0;
.. verilog:port:: input wire S0, S1, S2, S3;
.. verilog:port:: input wire [(DataWidth - 1):0] wdata_a_i;
.. verilog:port:: input wire [6:0]  OPMODE;
.. verilog:port:: input wire [DATA_WIDTH/2-1:0] b;
.. verilog:port:: input wire [NBITS-1:0] I1;
.. verilog:port:: input wire wrclk;
.. verilog:port:: output	reg		[31:0]	sum;
.. verilog:port:: output                 CO;
.. verilog:port:: output              clk_out                  ;
.. verilog:port:: output       rx_empty       ;
.. verilog:port:: output      y      ;
.. verilog:port:: output     clk_out    ;
.. verilog:port:: output  data_out_ack;
.. verilog:port:: output  out;
.. verilog:port:: output  parity_out ;
.. verilog:port:: output  reg out;
.. verilog:port:: output UUT_CO, UUT_ACCUMCO, UUT_SIGNEXTOUT;
.. verilog:port:: output [15:0] decoder_out ;
.. verilog:port:: output [3:0] binary_out  ;
.. verilog:port:: output [7 : 0] count;
.. verilog:port:: output [7:0] count;
.. verilog:port:: output [7:0] rx_data        ;
.. verilog:port:: output [WIDTHA+WIDTHB-1:0] RES;
.. verilog:port:: output [Y_WIDTH-1:0] X, Y, CO;
.. verilog:port:: output [number_of_channels-1:0] dataout;
.. verilog:port:: output gnt_0 ;
.. verilog:port:: output q, \q~ ;
.. verilog:port:: output reg	fs_ce;
.. verilog:port:: output reg  [WIDTH-1:0] out;
.. verilog:port:: output reg Q0, Q1, Q2, Q3;
.. verilog:port:: output reg [7:0] x, y, z, w;
.. verilog:port:: output reg carry_out, borrow_out, parity_out;
.. verilog:port:: output reg wfi_insn_o;
.. verilog:port:: output reg[WIDTH-1:0] POUT;
.. verilog:port:: output sbox_decrypt_o;
.. verilog:port:: output signed [SIZEOUT-1:0] REF_accum_out, accum_out;
.. verilog:port:: output wand Y;
.. verilog:port:: output wand [3:0] Y;
.. verilog:port:: output wire 	      CARRYCASCOUT;
.. verilog:port:: output wire 	     CIN;
.. verilog:port:: output wire [(DataWidth - 1):0] rdata_a_o;
.. verilog:port:: output wire [0:(PMPNumChan - 1)] pmp_req_err_o;
.. verilog:port:: output wire [3:0]  CARRYOUT;
.. verilog:port:: output wire [DATA_WIDTH-1:0] cout;
.. verilog:port:: output wire [NBITS-1:0] O;
.. verilog:port:: output wire wrclk;
.. verilog:port:: output wire[WIDTH-1:0] POUT;
.. verilog:port:: output wor X;
.. verilog:port:: output wor [3:0] X;

