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

