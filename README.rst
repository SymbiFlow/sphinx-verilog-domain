Sphinx Verilog Domain
=====================

.. warning::
    This extension is in development stage.

.. note::
    This extension is not a part of sphinxcontrib yet.

Dependencies
------------

* ``lark-parser``

Enabling
--------

Add extension in ``conf.py``::

    extensions = [ 'sphinxcontrib.verilogdomain' ]

Usage
-----

Module headers (non-ANSI-style only for now)::

    .. verilog::module:: module Top(a, b);

Port declarations::

    .. verilog:port:: input wire [31:0] a, b;

Parameter declarations::

    .. verilog:parameter:: parameter logic param_name_05 = 1, param_name_05_b = 2;

Custom name for use in references::

    .. verilog:module:: module \35(4p3|) (z);
        :refname: module_escaped

References::

    Reference to :verilog:ref:`Top`
    Reference to :verilog:ref:`module_escaped` - links to ``\\35(4p3|)``

Nesting::

    .. verilog:module:: module Top1(a, b, c);

        .. verilog:port:: input a;

            Description of port ``a``

        .. verilog:port:: input b;

            Description of port ``b``

        .. verilog:module:: module Nested(a);

            .. verilog:port:: output a;

                Description of port ``a`` in ``Nested``

            Reference to module ``Top1``'s port ``a``: :verilog:ref:`Top1.a`.
