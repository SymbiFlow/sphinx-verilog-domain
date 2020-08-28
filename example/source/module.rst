verilog:module
**************

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

.. verilog:module:: (* x=1 *) module non_ansi_params_test_2 #(num = 3, other_num = 2 * 2) (port_name);

    References:
    :verilog:ref:`non_ansi_params_test_2`,
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
