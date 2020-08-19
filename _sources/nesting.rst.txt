Nesting and refs
****************

* :verilog:ref:`Top1.a` - should link to ``Top1.a`` port declaration

* :verilog:ref:`Top1.Nested1.a` - should link to ``Top1.Nested1.a`` port declaration

* :verilog:ref:`Nested1.a` - shouldn't create a link (symbol does not exist in this scope)

* :verilog:ref:`InOtherFile.p` - should link to ``InOtherFile.p`` port declaration which is located in another file

* :verilog:ref:`NestTest` - should link to ``NestTest``, not to ``nesttest``

* :verilog:ref:`nesttest` - should link to ``nesttest``, not to ``NestTest``

* :verilog:ref:`$root` - shouldn't create a link

* :verilog:ref:`Top1.$root` - shouldn't create a link (invalid qualified name)

.. verilog:module:: module a(p);

.. verilog:module:: module Top1(a, b, c);

    ``a`` and ``b`` in the module declaration should link to following port declarations. ``c`` shouldn't be a link.

    .. verilog:port:: input a;

    .. verilog:port:: input b;

    Following port is a duplicate - the module shouldn't link to it in its ports list.

    .. verilog:port:: output b;

        Duplicated name test: created link target should be unique (compare with previous ``b`` declaration)

    .. verilog:module:: module \35(4p3|) (z);
        :refname: module_escaped

    .. verilog:module:: module Nested1(a, b, c);

        ``a`` and ``b`` in the module declaration should link to following port declarations. ``c`` shouldn't be a link.
        Note that ``b`` has ``:refname:`` set as it not normally referencable by ``b``

        .. verilog:port:: input a;

            .. verilog:module:: module InPortsContent1(a);

                ``a`` in the module declaration shouldn't be a link.

                This module is located inside ``input a``'s ReST directive's content. However, it should be registered directly in module ``Nested1`` scope.

        .. verilog:port:: input b;
            :refname: port_b_in_module_nested1

        Refs test:

        * :verilog:ref:`a`, :verilog:ref:`Nested1.a`, :verilog:ref:`Top1.Nested1.a` - should link to ``Top1.Nested1.a`` port declaration

        * :verilog:ref:`$root.a` - should link to ``a`` module declaration in toplevel scope

        * :verilog:ref:`b`, :verilog:ref:`Nested1.b`, :verilog:ref:`Top1.Nested1.b` - should link to ``Top1.Nested1`` module declaration. The module declares the port in its ports list, and no other declaration is available.

        * :verilog:ref:`c`, :verilog:ref:`Top1.c` - should link to ``Top1`` module declaration.

        * :verilog:ref:`Top1.a` - should link to ``Top1.a`` port declaration

        * :verilog:ref:`Top2.a` - should link to ``Top2.a`` port declaration

        * :verilog:ref:`module_escaped` (ref used in .rst is ``module_escaped``) - should link to ``Top1.\35(4p3|)`` module declaration (the declaration has ``refname``)

        * :verilog:ref:`\\35(4p3|)` - shouldn't create a link (``Top1.\35(4p3|)`` has ``refname`` specified)

        * :verilog:ref:`LoremIpsumDolorSitAmetNestTest` - shouldn't create a link (symbol does not exist)

        * :verilog:ref:`unique_port_name_in_nest_test` - shouldn't create a link (symbol does not exist in this scope)

.. verilog:port:: input \refname-use , \with-multiple-names ;
    :refname: refname_use_with_multiple_names

:verilog:ref:`refname_use_with_multiple_names` (``refname_use_with_multiple_names``) should refer to port definition above

.. verilog:module:: module Top2(a, b);

    ``a`` in the module declaration should link to following port declaration. ``b`` shouldn't be a link.

    .. verilog:port:: input a;

.. verilog:module:: module Top3(x, y, unique_port_name_in_nest_test);

    ``y`` in the module declaration should link to following port declaration. ``x`` and ``unique_port_name_in_nest_test`` shouldn't be a link.

    .. verilog:port:: input y;

.. verilog:port:: input nesttest0, nesttest;

.. verilog:port:: input NestTest, NestTest2;

----

Some text to enable scrolling...

- Lorem
- ipsum
- dolor
- sit
- amet,
- consectetur
- adipiscing
- elit.
- Donec
- ac
- mattis
- metus.
- Praesent
- faucibus
- tortor
- eu
- euismod
- imperdiet.
- Mauris
- a
- porta
- mauris,
- ac
- faucibus
- magna.
- Aliquam
- lacinia
- hendrerit
- interdum.
- Nullam
- tempor,
- massa
- ac
- scelerisque
- porta,
- nunc
- nunc
- dignissim
- ex,
- id
- commodo
- ligula
- lorem
- sit
- amet
- ligula.
- Morbi
- rhoncus
- et
- orci
- ut
- euismod.
- In
- eu
- scelerisque
- lectus,
- tempor
- vulputate
- risus.
- Proin
- imperdiet
- dignissim
- condimentum.
- Nunc
- ultrices
- laoreet
- faucibus.
- Morbi
- fringilla
- efficitur
- dolor,
- et
- eleifend
- erat
- pellentesque
- at.
- Donec
- sed
- ligula
- ac
- ligula
- consequat
- lobortis.
- Integer
- nec
- diam
- id
- magna
- scelerisque
- placerat.
