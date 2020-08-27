from collections import defaultdict

from docutils.parsers.rst import directives

from sphinx import addnodes
from docutils import nodes
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain
from sphinx.domains import Index
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_refnode
import lark
import re
from os import path

from sphinx.util import logging
log = logging.getLogger(__name__)

_csi_sequences = {
    "B": "\033[1m",  # bold/bright
    "D": "\033[2m",  # dim
    "n": "\033[22m", # normal intensity
    "I": "\033[3m",  # italic on
    "i": "\033[23m", # italic off
    "R": "\033[7m",  # reverse on
    "r": "\033[27m", # reverse off
}

def debug(name, msg, *args, **kwargs):
    log.info("\033[94m{B}{R}{}{r}{n} {}\033[0m".format(name, msg, **_csi_sequences),
            *args, **kwargs)

def _format_location(srcdoc, dstdoc, line):
    return f"on line {line}" if srcdoc == dstdoc else f"in '{dstdoc}', on line {line}"

#-------------------------------------------------------------------------------

def visualize_tree(root, children_iter_func, format_func):
    lines = []
    OUTER_PREFIXES = ("├─ ", "└─ ")
    INNER_PREFIXES = ("│  ", "   ")
    def process_children(node, prefix=""):
        children, count = children_iter_func(node)
        for i, child in enumerate(children):
           lines.append("\033[2m{}\033[22m{}".format(prefix + OUTER_PREFIXES[0 if i<count-1 else 1], str(format_func(child))))
           process_children(child, prefix + INNER_PREFIXES[0 if i<count-1 else 1])

    lines.append(format_func(root))
    process_children(root)

    return "\n".join(lines)

#-------------------------------------------------------------------------------

escaped_line_break_re = re.compile(r"\\\n\s*")
strip_backslash_re = re.compile(r"\\(.)")

class VerilogParser(lark.Lark):
    def __init__(self):
        grammar_file = path.join(path.dirname(__file__), "verilog.lark")
        with open(grammar_file, "r") as f:
            grammar = f.read()

        # Remove escaped line breaks and leading whitespace in the next line
        grammar = escaped_line_break_re.sub("", grammar)

        super().__init__(grammar,
                parser="lalr",
                start=["port", "module", "parameter"]
            )


class BaseVerilogDirective(ObjectDescription):
    start_rule = ""
    creates_scope = True

    parser = VerilogParser()

    def __init__(self, *args, **kwargs):
        self.all_names = set()
        super().__init__(*args, **kwargs)

    #------------------------
    # Parser tree processing
    #------------------------

    def process_tree(self, tree):
        self._prev_token = None
        nodes = []
        names = []
        placeholders = []
        for typ, item in self._process_nodes(tree):
            if typ == "name": names.append(item)
            elif typ == "node": nodes.append(item)
            elif typ == "placeholder": placeholders.append(item)
            else: assert False
        return (nodes, names, placeholders)

    def _process_nodes(self, item, rules=[]):
        if isinstance(item, lark.Tree):
            for i in item.children:
                yield from self._process_nodes(i, [item.data] + rules)
        elif isinstance(item, lark.Token):
            if self.should_insert_space(item):
                yield ("node", nodes.Text(" "))
            yield from self.process_token(item, rules)
            self._prev_token = item

    def process_token(self, token, rules=[]):
        type_parts = token.type.split("_")
        prev_parts = self._prev_token.type.split("_") if self._prev_token else [""]

        if type_parts[0] == "KW":
            yield ("node", addnodes.desc_type(text=token.value))
        elif type_parts[0] == "SYM":
            yield ("node", addnodes.desc_sig_punctuation(text=token.value))
        elif type_parts[0] == "ID":
            if "id_ext_port" in rules:
                yield ("node", addnodes.desc_addname(text=token.value))
            else:
                yield ("node", addnodes.desc_name(text=token.value))
        elif type_parts[0] == "TEXT":
            yield ("node", addnodes.desc_sig_element(text=token.value.strip()))
        else:
            yield ("node", addnodes.desc_sig_element(text=token.value))

    def should_insert_space(self, token):
        c = token.type.split("_")
        p = self._prev_token.type.split("_") if self._prev_token else [""]
        return (
                (p[0] in ["KW", "ID", "TEXT"] and c[0] in ["KW", "ID", "TEXT"]) or
                (p[0] in ["KW"] and c[-1] in ["L"]) or
                ((p == "SYM_ATTR_PAREN_L".split("_")) or (c == "SYM_ATTR_PAREN_R".split("_"))) or
                (p[0] in ["SYM"] and p[-1] not in ["L"] and c[0] in ["KW", "ID", "TEXT", "OP"]) or
                (p == "OP_EQUAL".split("_") or c == "OP_EQUAL".split("_"))
                )

    #---------
    # Helpers
    #---------

    def _loc(self):
        return (self.env.docname, self.lineno)

    def _dbg_print_tree(self, sig, tree):
        if self._debug_enabled("print_parser_tree"):
            def print_tree(tree, block_indent='', indent="\033[90m:   \033[0m", indent_level=0):
                if isinstance(tree, lark.Tree):
                    yield f"{block_indent}{indent * indent_level}[{tree.data}]"
                    for n in tree.children:
                        yield from print_tree(n, block_indent, indent, indent_level+1)
                elif isinstance(tree, lark.Token):
                    yield f"{block_indent}{indent * indent_level}[{tree.type}] \033[94m{repr(str(tree))}\033[0m"

            msg = [
                f"{self.name}:",
                f"  \033[94m{repr(sig)}\033[0m\033[0m",
                *(list(print_tree(tree, '  '))),
                "",
            ]
            log.info("\n".join(msg), location=self._loc())

    def _debug_enabled(self, cat):
        global_debug = cat in self.env.app.config.verilog_domain_debug
        object_debug = "debug" in self.options
        return global_debug or object_debug

    #-----------------------------
    # ObjectDescription interface
    #-----------------------------

    has_content = True
    required_arguments = 1

    option_spec = dict(ObjectDescription.option_spec,
        debug = directives.flag,
        refname = directives.unchanged,
    )

    @property
    def current_object(self):
        domain = self.env.get_domain("verilog")
        return self.env.temp_data.setdefault("verilog:current_object", domain.root_object)

    @current_object.setter
    def current_object(self, value):
        self.env.temp_data["verilog:current_object"] = value

    def push_namespace(self, identifier):
        namespace = self.current_object.setdefault(identifier, VerilogDomainObject(identifier))
        self.current_object = namespace

    def run(self):
        try:
            self.refname = VerilogIdentifier(self.options.get("refname", "").strip())
        except:
            self.refname = None
        self.parent_object = self.current_object
        nodes = super().run()
        self.current_object = self.parent_object
        return nodes

    def transform_content(self, contentnode):
        if not self._debug_enabled("add_debug_content"):
            return super().transform_content(contentnode)

        dbg_info = nodes.paragraph()
        contentnode.insert(0, dbg_info)

        src_line = nodes.line(text="Src: ")
        dbg_info += src_line
        lb = nodes.literal(text='\n'.join(self.get_signatures()))
        lb["language"] = "text"
        src_line += lb

        def list_join(joiner, values):
            new_values=[joiner] * (2*len(values) - 1)
            new_values[0::2] = values
            return new_values


        names = []
        placeholders = []
        for n,p in self.names:
            names.extend(n)
            placeholders.extend(p)

        if names:
            decls = nodes.line(text="Declares: ")
            dbg_info += decls
            if not self.refname:
                decls += list_join(nodes.Text(","), [nodes.literal(text=n.strip()) for n in names])
            else:
                decls += nodes.literal(text=names[0].strip())
                decls += nodes.Text(" as ")
                decls += nodes.literal(text=self.refname)

            namespace = self.parent_object.qualified_name
            if len(namespace) > 0:
                decls += nodes.Text(" in ")
                decls += nodes.literal(text=".".join(namespace))
        if placeholders:
            refs = nodes.line(text="Placeholders: ")
            dbg_info += refs
            refs += list_join(nodes.Text(","), [nodes.literal(text=n.strip()) for n in placeholders])

    def get_signatures(self):
        if self.creates_scope:
            # Only one declaration per directive
            signature = escaped_line_break_re.sub('', self.arguments[0])
            if self.config.strip_signature_backslash:
                signature = strip_backslash_re.sub(r'\1', signature)
            return [signature]
        else:
            return super().get_signatures()

    def handle_signature(self, sig, signode):
        nodes = []
        try:
            tree = self.parser.parse(text=sig, start=self.start_rule)
        except lark.UnexpectedToken as e:
            msg = [
                f"{self.name}: Unexpected token {repr(e.token)} at column {e.column}:",
                *(e.get_context(text=sig).split("\n")),
                "Expected one of: " + ", ".join(e.expected) + "\n"
            ]
            log.error("\n\t".join(msg), location=self._loc())
            raise ValueError()
        except Exception as e:
            log.error(f"{self.name}: {e}", location=self._loc())
            raise ValueError()

        nodes, names, placeholders = self.process_tree(tree)
        self._dbg_print_tree(sig, tree)
        signode += nodes
        return (names, placeholders)

    def add_target_and_index(self, names_placeholders, sig, signode):
        names, placeholders = names_placeholders
        if not names:
            log.warning("{caller}: no name declarations found in signature: {sig}".format(
                caller = self.name,
                sig = sig,
            ), location=self._loc())
            return

        def make_unique_linktarget(refname, obj, used_ids):
            if obj.parent:
                if obj.parent.linktarget:
                    parent_linktarget = obj.parent.linktarget
                else:
                    parent_linktarget = make_unique_linktarget(obj.name.normalize(), obj.parent, used_ids)
            else:
                assert obj.name == VerilogIdentifier.ROOT_NAME, "Object must be added to domain's object tree before calling this function."
                return "verilog"

            preferred_linktarget = parent_linktarget + "-" + refname
            linktarget = nodes.make_id(preferred_linktarget)
            i = 1
            while linktarget in used_ids:
                linktarget = nodes.make_id(preferred_linktarget + "-" + str(i))
                i += 1
            return linktarget

        for name in names:
            if name in self.all_names:
                continue
            self.all_names.add(name)

            refname = str(self.refname or name.normalize())

            if refname in self.parent_object:
                obj = self.parent_object[refname]
                if not (obj.is_only_namespace() or obj.is_placeholder()):
                    log.warning("{caller}: name already declared ({loc}): {name}".format(
                        caller = self.name,
                        name = obj.qualified_name,
                        loc = _format_location(self.env.docname, obj.docname, obj.lineno)
                    ), location=self._loc())
                    return
            else:
                obj = self.parent_object[refname] = VerilogDomainObject()

            obj.name = name
            obj.linktarget = make_unique_linktarget(refname, obj, self.state.document.ids)
            obj.docname = self.env.docname
            obj.lineno = self.lineno
            obj.objtype = self.objtype

            signode["ids"].append(obj.linktarget)
            self.state.document.note_explicit_target(signode)
            # Refname allows for only one name per signature
            if self.refname:
                break

        for placeholder in placeholders:
            if placeholder not in self.current_object:
                self.current_object[placeholder] = VerilogDomainObject(name=placeholder,
                        linktarget=self.current_object.linktarget,
                        docname=self.current_object.docname,
                        lineno=self.current_object.lineno)

#-------------------------------------------------------------------------------

class PortDirective(BaseVerilogDirective):
    start_rule = "port"
    creates_scope = False

    def process_token(self, token, rules=[]):
        yield from super().process_token(token, rules)
        if token.type == "ID" and "id_port" in rules:
            yield ("name", VerilogIdentifier(token.value))


class ParameterDirective(BaseVerilogDirective):
    start_rule = "parameter"
    creates_scope = False

    def process_token(self, token, rules=[]):
        yield from super().process_token(token, rules)
        if token.type == "ID" and "id_parameter" in rules:
            yield ("name", VerilogIdentifier(token.value))


class ModuleDirective(BaseVerilogDirective):
    start_rule = "module"

    def process_token(self, token, rules=[]):
        if token.type == "ID" and "id_port" in rules:
            name = VerilogIdentifier(token.value)
            yield ("placeholder", name)

            qualified_name = self.current_object.qualified_name + name

            ref = addnodes.pending_xref("", refdomain="verilog", reftype="childref", refwarn=False, reftarget=str(qualified_name))
            ref.line = self.lineno
            ref["verilog:parent_object"] = self.current_object

            port_node = addnodes.desc_addname(text=token.value)
            ref += port_node
            yield ("node", ref)
        else:
            yield from super().process_token(token, rules)
            if token.type == "ID" and "id_module" in rules:
                name = VerilogIdentifier(token.value)
                self.push_namespace(self.refname or name)
                yield ("name", name)


class VerilogXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title: bool, title: str, target: str):
        refnode["verilog:parent_object"] = env.temp_data.get("verilog:current_object")
        return super().process_link(env, refnode, has_explicit_title, title, target)

#-------------------------------------------------------------------------------

class VerilogIdentifier(str):
    _simple_identifier_re = re.compile(r"[a-zA-Z_][a-zA-Z0-9_$]*")
    _any_identifier_re = re.compile(_simple_identifier_re.pattern + r"|\\[\x21-\x7E]+(?: |$)" + r"|\$root")

    ROOT_NAME = "$root"

    def __new__(cls, value):
        if isinstance(value, cls):
            return value
        if not isinstance(value, str):
            raise TypeError(f"{cls.__name__}() argument must be a string or {cls.__name__}, not {repr(type(value).__name__)}")
        if not VerilogIdentifier._any_identifier_re.fullmatch(str(value)):
            raise ValueError(f"Invalid identifier for {cls.__name__}(): {repr(value)}")
        return super().__new__(cls, value)

    def is_escaped(self):
        return self[-1] == " " and self[0] == "\\"

    def normalize(self):
        """Returns unescaped name if the identifier is escaped and can be represented as a simple identifier.
        Otherwise returns name without changes.
        """
        if self.is_escaped() and VerilogIdentifier._simple_identifier_re.fullmatch(self[1:-1]):
            return str(self[1:-1])
        else:
            return str(self)

    def __eq__(self, other):
        return str(self) == str(other) or self.normalize() == VerilogIdentifier(other).normalize()

    def __hash__(self):
        return hash(self.normalize())

    def __add__(self, other):
        if isinstance(other, str):
            return VerilogQualifiedIdentifier((self, other))
        raise NotImplemented()

    def __radd__(self, other):
        if isinstance(other, str):
            return VerilogQualifiedIdentifier((other, self))
        raise NotImplemented()


class VerilogQualifiedIdentifier(tuple):
    def __new__(cls, values):
        # To prevent common error, raise error when str (or VerilogIdentifier) is passed directly as an argument.
        if isinstance(values, str):
            raise TypeError(f"{cls.__name__}() argument must be any iterable except string. Try wrapping it in a list.")
        return super().__new__(cls, [VerilogIdentifier(value) for value in values])

    @classmethod
    def fromstring(cls, s):
        if not isinstance(s, str):
            raise TypeError(f"{cls.__name__}() argument must be a string, not {repr(type(s).__name__)}")
        return cls(VerilogIdentifier._any_identifier_re.findall(s))

    def __str__(self): return "::".join(self)

    def normalize(self):
        return VerilogQualifiedIdentifier([vi.normalize() for vi in self])

    def __add__(self, other):
        if isinstance(other, str):
            return VerilogQualifiedIdentifier((*self, other))
        elif isinstance(other, VerilogQualifiedIdentifier):
            return VerilogQualifiedIdentifier((*self, *other))
        raise NotImplemented()

    def __radd__(self, other):
        if isinstance(other, str):
            return VerilogQualifiedIdentifier((other, *self))
        raise NotImplemented()

#-------------------------------------------------------------------------------

class VerilogDomainObject:
    def __init__(self, name=None, linktarget=None, docname=None, lineno=None, objtype=None):
        # Identifier name used to refer to the object in the document's text.
        self.name = VerilogIdentifier(name) if name else None
        # Target used by hyperlinks
        self.linktarget = linktarget
        # Parent object
        self._parent = None
        self._children = {}

        self.docname = docname
        self.lineno = lineno

        self.objtype = objtype

    @property
    def qualified_name(self): return VerilogQualifiedIdentifier([o.name for o in self.path()])

    @property
    def parent(self): return self._parent

    def path(self):
        """Returns a list of all objects which create a path from the tree root to this object.
        """
        objects = [self]
        while objects[-1].parent is not None:
            objects.append(objects[-1].parent)
        return list(reversed(objects))

    def is_placeholder(self):
        return self.parent is not None and self.linktarget and self.linktarget == self.parent.linktarget

    def is_only_namespace(self):
        return self.linktarget is None

    def __str__(self):
        s = str(self.qualified_name)
        if self.linktarget:
            s += f" #{self.linktarget}"
        if self.docname or self.lineno:
            s += ", in " + (self.docname or "?") + (f":{self.lineno}" if self.lineno is not None else "")
        return s

    # dict-like interface

    def items(self):
        return self._children.items()

    def get(self, key, default=None):
        return self._children.get(key, default)

    def values(self):
        return self._children.values()

    def setdefault(self, k, default):
        if k not in self:
            self[k] = default
        return self[k]

    def __iter__(self):
        return self._children.__iter__()

    def __contains__(self, key):
        return key in self._children

    def __getitem__(self, key):
        return self._children[key]

    def __setitem__(self, key, obj):
        assert isinstance(obj, VerilogDomainObject)
        assert obj not in self.path()
        key = VerilogIdentifier(key)
        if key == VerilogIdentifier.ROOT_NAME:
            raise ValueError(f"Invalid identifier: {key}")

        if key in self:
            del self[key]

        if obj.parent:
            for k,v in obj.parent.items():
                if v == obj:
                    del obj.parent[k]
                    break
        obj._parent = self
        self._children[key] = obj

    def __delitem__(self, key):
        assert key in self._children

        self._children[key]._parent = None
        del self._children[key]

    def visualize_tree(self):
        def obj_children_iter(kv):
            key, obj = kv
            return (obj._children.items(), len(obj._children))

        def obj_format(kv):
            key, obj = kv
            slist = ["{B}{name}{n}"]
            if key and key != obj.name: slist.insert(0, "{D}[{n}{B}{key}{n}{D}]{n}")
            if obj.linktarget: slist.append("{D}#{n}{linktarget}")
            if obj.docname and obj.lineno: slist.append("{D}({n}{docname}{D}:{n}{lineno}{D}){n}")
            if obj.is_only_namespace(): slist.append("{D}{I}namespace{i}{n}")
            if obj.is_placeholder(): slist.append("{D}{I}placeholder{i}{n}")
            return " ".join(slist).format(**_csi_sequences, key=key, name=obj.name, docname=obj.docname, lineno=obj.lineno, linktarget=obj.linktarget)

        return visualize_tree(('', self), obj_children_iter, obj_format)

#-------------------------------------------------------------------------------

class VerilogDomain(Domain):
    name = "verilog"
    label = "Verilog domain"
    roles = {
        "ref": VerilogXRefRole(warn_dangling=True)
    }
    directives = {
        "module": ModuleDirective,
        "parameter": ParameterDirective,
        "port": PortDirective,
    }
    initial_data = {
        "objects": VerilogDomainObject(name=VerilogIdentifier.ROOT_NAME),
    }

    @property
    def root_object(self):
        return self.data["objects"]

    def _debug_enabled(self, cat):
        return cat in self.env.app.config.verilog_domain_debug

    def get_objects(self):
        def iter_tree(obj):
            yield obj
            for child in obj.values():
                yield from iter_tree(child)

        for obj in iter_tree(self.root_object):
            if not (obj.is_only_namespace() or obj.is_placeholder()):
                yield str(obj.qualified_name), str(obj.qualified_name), obj.objtype or "", obj.docname, obj.linktarget, 1

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        if self._debug_enabled("print_objects_tree") and not hasattr(self, "_dbg_resolve_xref_executed"):
            self._dbg_resolve_xref_executed = True
            debug("objects_tree", self.root_object.visualize_tree())

        try:
            target_identifier = VerilogQualifiedIdentifier.fromstring(target)
        except:
            return None

        # Special case for childrefs, e.g. port names in module declaration
        if typ == "childref":
            identifier = target_identifier[-1]
            parent_obj = node.attributes.get("verilog:parent_object")
            if parent_obj:
                obj = parent_obj.get(identifier)
                if not obj or obj.is_placeholder():
                    # Workaround for childrefs to targets with "refname" set.
                    for candidate in parent_obj.values():
                        if candidate.name == identifier:
                            obj = candidate
                if obj and not obj.is_placeholder():
                    tooltip = f"{obj.objtype} {obj.name}" if obj.objtype else f"{obj.name}"
                    return make_refnode(builder, fromdocname, obj.docname, obj.linktarget, contnode, tooltip)
            return None

        # Find leading identifier's object
        leading_identifier = target_identifier[0]
        if leading_identifier == VerilogIdentifier.ROOT_NAME:
            obj = self.root_object
        else:
            obj = node.attributes.get("verilog:parent_object") or self.root_object
            while obj and leading_identifier not in obj:
                obj = obj.parent
            if not obj:
                return None
            obj = obj[leading_identifier]

        # Find remaining identifiers
        try:
            for identifier in target_identifier[1:]:
                obj = obj[identifier]
        except:
            return None

        if not obj.linktarget:
            return None

        # Skip "$root" prefix
        qualified_name_without_root = VerilogQualifiedIdentifier(obj.qualified_name[1:])
        tooltip = f"{obj.objtype} {qualified_name_without_root}" if obj.objtype else f"{qualified_name_without_root}"
        return make_refnode(builder, fromdocname, obj.docname, obj.linktarget, contnode, tooltip)

def setup(app):
    app.add_config_value('verilog_domain_debug', [], '')
    app.add_domain(VerilogDomain)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
