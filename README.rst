sphinx-verilog-domain
=====================

.. warning::

    This extension is in development stage.

Dependencies
------------

* ``lark-parser``

Enabling
--------

Add extension in ``conf.py``::

    extensions = [ 'sphinx_verilog_domain' ]

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

Namespaces
^^^^^^^^^^

There are three directives for changing current Verilog scope:

* ``.. verilog:namespace:: A::B`` - sets current scope to ``A::B``. Using ``$root`` as an argument or using the directive without argument at all sets global namespace.

* ``.. verilog:namespace-push:: C::D`` - sets current scope to ``C::D`` relatively to current scope

* ``.. verilog:namespace-pop::`` - restores scope which was active before previous ``namespace-push`` was called. If there is no matching ``namespace-push``, scope is set to global scope.

.. note::
    ``verilog::namespace`` resets push/pop stack

Example::

    .. verilog:namespace:: A::B
    .. verilog:port:: input inside_a_b;
    .. verilog:namespace-push:: C::D
    .. verilog:port:: input inside_a_b_c_d;
    .. verilog:namespace-pop::
    .. verilog:port:: input inside_a_b_again;
    .. verilog:namespace::
    .. verilog:port:: input in_global_namespace;

Development
-----------

To create and open the development environment with all system
and python packages use::

   make env
   source env/conda/bin/activate sphinx-verilog-domain
