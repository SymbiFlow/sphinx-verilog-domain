Verilog Diagrams compatibility test
***********************************

.. TODO: use original version (commented below) when ansi-style module declarations become supported
.. .. verilog:module:: module CARRY4(output [3:0] CO, O, input CI, CYINIT, input [3:0] DI, S);

.. verilog:module:: module CARRY4(CO, O, CI, CYINIT, DI, S);

    Source code without license:

    .. no-license:: verilog/carry4-whole.v
        :language: verilog
        :linenos:

    Diagram:

    .. verilog-diagram:: verilog/carry4-whole.v
        :type: netlistsvg
        :module: CARRY4
