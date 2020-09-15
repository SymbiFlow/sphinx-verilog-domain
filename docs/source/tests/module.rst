verilog:module
**************

.. verilog:module:: module module_test();

ANSI style
==========

.. verilog:module:: module ansi_top (input wire i_clk, input wire i_inp, output reg o_out);

    References:
    :verilog:ref:`ansi_top`
    :verilog:ref:`i_clk`
    :verilog:ref:`i_inp`
    :verilog:ref:`o_out`

.. verilog:module:: module ansi_style_1(input x);

    References:
    :verilog:ref:`ansi_style_1`
    :verilog:ref:`x`

.. verilog:module:: module ansi_style_2(input x, output y);

    References:
    :verilog:ref:`ansi_style_2`
    :verilog:ref:`x`
    :verilog:ref:`y`

.. verilog:module:: module ansi_style_3(wire x);

    References:
    :verilog:ref:`ansi_style_3`
    :verilog:ref:`x`

.. verilog:module:: module ansi_style_4(output signed x);

    References:
    :verilog:ref:`ansi_style_4`
    :verilog:ref:`x`

.. verilog:module:: module ansi_style_5(output signed x = 1);

    References:
    :verilog:ref:`ansi_style_5`
    :verilog:ref:`x`

.. verilog:module:: module ansi_style_6(input x = 0, output y = 2*2);

    References:
    :verilog:ref:`ansi_style_6`
    :verilog:ref:`x`
    :verilog:ref:`y`

.. verilog:module:: module ansi_style_7(inout integer x);

    References:
    :verilog:ref:`ansi_style_7`
    :verilog:ref:`x`

.. verilog:module:: module ansi_style_8(output [7:0] x);

    References:
    :verilog:ref:`ansi_style_8`
    :verilog:ref:`x`

.. verilog:module:: module ansi_style_9(input signed [7:0] x);

    References:
    :verilog:ref:`ansi_style_9`
    :verilog:ref:`x`

.. verilog:module:: module ansi_style_10([7:0] x);

    References:
    :verilog:ref:`ansi_style_10`
    :verilog:ref:`x`

.. verilog:module:: module ansi_style_11([7:0] x, input y);

    References:
    :verilog:ref:`ansi_style_11`
    :verilog:ref:`x`
    :verilog:ref:`y`

.. verilog:module:: module ansi_style_12((* attr *) output integer x);

    References:
    :verilog:ref:`ansi_style_12`
    :verilog:ref:`x`

.. verilog:module:: module ansi_style_13((* attr *) output integer x, (* attr_other *) input [3:0] y);

    References:
    :verilog:ref:`ansi_style_13`
    :verilog:ref:`x`
    :verilog:ref:`y`

.. verilog:module:: module ansi_style_14((* attr *) output integer [7:0] x, (* other, attr *) wire y);

    References:
    :verilog:ref:`ansi_style_14`
    :verilog:ref:`x`
    :verilog:ref:`y`

.. verilog:module:: module ansi_style_15(ref [7:0] x, y);

    References:
    :verilog:ref:`ansi_style_15`
    :verilog:ref:`x`
    :verilog:ref:`y`

.. verilog:module:: module ansi_style_16(ref x [7:0], y);

    References:
    :verilog:ref:`ansi_style_16`
    :verilog:ref:`x`
    :verilog:ref:`y`

.. verilog:module:: module ansi_style_17(ref [7:0] x [7:0], y);

    References:
    :verilog:ref:`ansi_style_17`
    :verilog:ref:`x`
    :verilog:ref:`y`


.. verilog:module:: module ansi_style_18 (
                        input .ext1(x[7:4]),
                        input .ext2(x[3:0]),
                        inout y,
                        output .ext3(z)
                    );

    References:
    :verilog:ref:`ansi_style_18`
    :verilog:ref:`x`
    :verilog:ref:`y`
    :verilog:ref:`z`


.. verilog:module:: module ansi_style_19 (
                        input [7:0] a,
                        input signed [7:0] b, c, d,
                        output [7:0] e,
                        output var signed [7:0] f, g,
                        output signed [7:0] h
                    );

    References:
    :verilog:ref:`ansi_style_19`
    :verilog:ref:`a`
    :verilog:ref:`b`
    :verilog:ref:`c`
    :verilog:ref:`d`
    :verilog:ref:`e`
    :verilog:ref:`f`
    :verilog:ref:`g`
    :verilog:ref:`h`


Non-ANSI style
==============

.. verilog:module:: (* attr = 2 * 2 *) module test1(a,b,c,d,e,f,g,h);
.. verilog:module:: module test2(a,b,c,d,e,f,g,h);
.. verilog:module:: module complex_ports ( {c,d}, .e(f) );
.. verilog:module:: module split_ports (a[7:4], a[3:0]);
.. verilog:module:: module same_port (.a(i), .b(i));
.. verilog:module:: module renamed_concat (.a({b,c}), f, .g(h[1]));
.. verilog:module:: module same_input (a,a);
.. verilog:module:: module mixed_direction (.p({a, e}));

Module parameters
=================

.. verilog:module:: (* x=1 *) module non_ansi_params_test_1 #() (port_name);

    References:
    :verilog:ref:`non_ansi_params_test_1`

.. verilog:module:: (* x=1 *) module ansi_params_test_1 #() (input port_name);

    References:
    :verilog:ref:`ansi_params_test_1`

.. verilog:module:: (* x=1 *) module non_ansi_params_test_2 #(num = 3, other_num = 2 * 2) (port_name);

    References:
    :verilog:ref:`non_ansi_params_test_2`,
    :verilog:ref:`num`,
    :verilog:ref:`other_num`

.. verilog:module:: (* x=1 *) module ansi_params_test_2 #(num = 3, other_num = 2 * 2) (input port_name);

    References:
    :verilog:ref:`ansi_params_test_2`,
    :verilog:ref:`num`,
    :verilog:ref:`other_num`

.. verilog:module:: (* x=1 *) module non_ansi_params_test_3 #(num, other_num) (port_name);

    References:
    :verilog:ref:`non_ansi_params_test_3`,
    :verilog:ref:`num`,
    :verilog:ref:`other_num`

    Parameter :verilog:ref:`other_num` is explicitly described below. The declaration in module header should link to it.

    .. verilog:parameter:: parameter other_num = 2 * 2;

        Parameter description.

.. verilog:module:: (* x=1 *) module ansi_params_test_3 #(num, other_num) (input port_name);

    References:
    :verilog:ref:`ansi_params_test_3`,
    :verilog:ref:`num`,
    :verilog:ref:`other_num`

    Parameter :verilog:ref:`other_num` is explicitly described below. The declaration in module header should link to it.

    .. verilog:parameter:: parameter other_num = 2 * 2;

        Parameter description.

.. verilog:module:: (* x=1 *) module non_ansi_params_test_4 # (parameter num = 3, other_num = 2 * 2) (port_name);

    References:
    :verilog:ref:`non_ansi_params_test_4`,
    :verilog:ref:`num`,
    :verilog:ref:`other_num`

.. verilog:module:: (* x=1 *) module non_ansi_params_test_5 # (parameter num = 3, localparam other_num = 2 * 2, yet_another_one = 42) (port_name);

    References:
    :verilog:ref:`non_ansi_params_test_5`,
    :verilog:ref:`num`,
    :verilog:ref:`other_num`
    :verilog:ref:`yet_another_one`

    Parameter :verilog:ref:`num` is explicitly described below. The declaration in module header should link to it.

    .. verilog:parameter:: parameter num;

        Parameter description.

.. verilog:module:: (* x=1 *) module non_ansi_params_test_6 # (parameter num = 3, localparam other_num, yet_another_one = 42) (port_name);

    References:
    :verilog:ref:`non_ansi_params_test_6`,
    :verilog:ref:`num`,
    :verilog:ref:`other_num`
    :verilog:ref:`yet_another_one`
