Verilog Domain test
###################

.. toctree::

   port
   parameter
   module
   nesting
   nesting2

   symbolator

----

.. verilog:module:: module d (  \
                        cos_z0, \
                        sin_z0, \
                        done,   \
                        z0,     \
                        start,  \
                        clock,  \
                        reset   \
                    );

   Sine and cosine computer. `Source <https://github.com/YosysHQ/yosys/blob/master/tests/simple/sincos.v>`_

   This module computes the sine and cosine of an input angle. The
   floating point numbers are represented as integers by scaling them
   up with a factor corresponding to the number of bits after the point.

   .. verilog:port:: output signed [19:0] cos_z0;
                     reg signed [19:0] cos_z0;

      cosine of the input angle

   .. verilog:port:: output signed [19:0] sin_z0;
                     reg signed [19:0] sin_z0;

      sine of the input angle

   .. verilog:port:: output done;
                     reg done;

      output flag indicated completion of the computation

   .. verilog:port:: input signed [19:0] z0;

      input angle

   .. verilog:port:: input start;

      input that starts the computation on a posedge

   .. verilog:port:: input clock;

      clock input

   .. verilog:port:: input reset;

      reset input

