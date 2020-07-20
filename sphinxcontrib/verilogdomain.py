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

termfmt_re = re.compile(r"\(\x1b\[([0-9,;]+)\]|\033\)")
def termfmt(s):
    sl = list(termfmt_re.split(s))
    r = sl.pop(0)
    stack = []
    for attr,text in zip(sl[0::2], sl[1::2]):
        if attr is not None:
            stack.append(attr)
            r += "\033[" + attr + "m" + text
        else:
            if len(stack) > 0:
                del stack[-1]
            r += "\033[" + ";".join(["0"] + stack) + "m" + text
    return r

def debug(name, msg, *args, **kwargs):
    log.info(termfmt(f"(\033[34](\033[7]{name}\033) {msg}\033)"), *args, **kwargs)


_simple_identifier_re = re.compile(r"[a-zA-Z_][a-zA-Z0-9_$]*")
_any_identifier_re = re.compile(_simple_identifier_re.pattern + r"|\\[\x21-\x7E]+ " + r"|\$root")

def _normalize_identifier(identifier: str):
    assert(identifier and _any_identifier_re.fullmatch(identifier))
    if identifier[-1] == " " and identifier[0] == "\\" and _simple_identifier_re.fullmatch(identifier[1:-1]):
        return identifier[1:-1]
    else:
        return identifier

def _split_qualified_identifier(qualified_identifier: str) -> list:
    # In some cases (e.g. in :ref: argument) space required by escaped identifiers can't be placed as a string's last character.
    # Add one just in case. It will be ignored if not needed.
    return _any_identifier_re.findall(qualified_identifier + " ")

def _make_qualified_identifier(identifiers: list) -> str:
    assert(all([_any_identifier_re.fullmatch(id) for id in identifiers]))
    return ".".join(identifiers)

#-------------------------------------------------------------------------------

class VerilogParser(lark.Lark):
    def __init__(self):
        grammar_file = path.join(path.dirname(__file__), "verilog.lark")
        with open(grammar_file, "r") as f:
            grammar = f.read()

        # Remove escaped line breaks and leading whitespace in the next line
        escaped_line_end_re = re.compile(r"\\\n\s*")
        grammar = escaped_line_end_re.sub("", grammar)

        super().__init__(grammar,
                parser="lalr",
                start=["port", "module", "parameter"]
            )


class BaseVerilogDirective(ObjectDescription):
    start_rule = ""
    creates_scope = True

    parser = VerilogParser()

    def __init__(self, *args, **kwargs):
        self.decl_names = []
        self.placeholders = []
        super().__init__(*args, **kwargs)

    #------------------------
    # Parser tree processing
    #------------------------

    def process_tree(self, tree):
        self._prev_token = None
        return list(self._process_nodes(tree))

    def _process_nodes(self, item, rules=[]):
        if isinstance(item, lark.Tree):
            for i in item.children:
                yield from self._process_nodes(i, [item.data] + rules)
        elif isinstance(item, lark.Token):
            if self.should_insert_space(item):
                yield nodes.Text(" ")
            yield from self.process_token(item, rules)
            self._prev_token = item

    def process_token(self, token, rules=[]):
        type_parts = token.type.split("_")
        prev_parts = self._prev_token.type.split("_") if self._prev_token else [""]

        if type_parts[0] == "KW":
            yield addnodes.desc_type(text=token.value)
        elif type_parts[0] == "SYM":
            yield addnodes.desc_sig_punctuation(text=token.value)
        elif type_parts[0] == "ID":
            if "id_ext_port" in rules:
                yield addnodes.desc_addname(text=token.value)
            else:
                yield addnodes.desc_name(text=token.value)
        elif type_parts[0] == "TEXT":
            yield addnodes.desc_sig_element(text=token.value.strip())
        else:
            yield addnodes.desc_sig_element(text=token.value)

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
                f"  decl names: {self.decl_names}",
                f"  placeholders: {[p[0] for p in self.placeholders]}",
            ]
            log.info("\n".join(msg), location=self._loc())

    @property
    def _verilog_scope(self) -> list:
        return self.env.temp_data.setdefault("verilog:scope", [])

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
        alias = directives.unchanged,
    )

    def transform_content(self, contentnode):
        if not self._debug_enabled("add_debug_content"):
            return super().transform_content(contentnode)

        dbg_info = nodes.paragraph()
        contentnode.insert(0, dbg_info)

        src_line = nodes.line(text="Src: ")
        dbg_info += src_line
        lb = nodes.literal(text='\n'.join(self.arguments))
        lb["language"] = "text"
        src_line += lb

        if self.decl_names:
            decls = nodes.line(text="Declares: ")
            dbg_info += decls
            decls += [nodes.literal(text=n) for n in self.decl_names]

            scope = self._verilog_scope
            if self.creates_scope and len(self.decl_names) == 1:
                # ignore this directive's scope
                scope = scope[0:-1]
            if len(scope) > 0:
                decls += nodes.Text(" in ")
                decls += nodes.literal(text=".".join(scope))
        if self.placeholders:
            refs = nodes.line(text="Placeholders: ")
            dbg_info += refs
            refs += [nodes.literal(text=n[0]) for n in self.placeholders]

    def before_content(self) -> None:
        if self.creates_scope:
            # Create Verilog scope for declarations inside this node
            if len(self.decl_names) == 1:
                scope = self._verilog_scope
                scope.append(self.decl_names[0])
            else:
                # A class which allows multiple names probably should set self.creates_scope to False
                log.warning(f"{self.name}: {len(self.decl_names)} names declared. Verilog scope is not created.", location=self._loc())


    def after_content(self) -> None:
        if self.creates_scope and len(self.decl_names) == 1:
            # Leave Verilog scope created in before_content()
            scope = self._verilog_scope
            assert(len(scope) > 0)
            assert(scope[-1] == self.decl_names[0])
            del scope[-1]

    def handle_signature(self, sig, signode):
        sig = sig.strip()

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
        except Exception as e:
            log.error(f"{self.name}: {e}", location=self._loc())
        else:
            nodes = self.process_tree(tree)
            self._dbg_print_tree(sig, tree)

        if nodes:
            signode += nodes
        else:
            signode += addnodes.desc_sig_element(text=sig)

        return self.decl_names

    def add_target_and_index(self, names, sig, signode):
        if not names:
            log.warning(f"{self.name}: `{sig}`: no declared names found", location=self._loc())
            return

        domain = self.env.get_domain("verilog")
        parent = domain.data["objects"]
        for ancestor_name in self._verilog_scope:
            parent = parent[ancestor_name]

        for name in names:
            # Create target
            id_parts = ["verilog", self.objtype] + self._verilog_scope + [name]
            node_id = nodes.make_id("-".join(id_parts))
            i = 1
            while node_id in self.state.document.ids:
                node_id = nodes.make_id("-".join(id_parts + [str(i)]))
                i += 1
            signode["ids"].append(node_id)
            self.state.document.note_explicit_target(signode)

            # Register the declaration in domain objects tree
            if name not in parent or parent[name].is_placeholder():
                parent[name] = _DomainObject(node_id=node_id, objtype=self.objtype, docname=self.env.docname, lineno=self.lineno)
            else:
                if "alias" not in self.options:
                    orig = parent[name]
                    log.warning(f"{self.name}: `{name}` (in scope `{parent.qualified_name}`) already declared in line {orig.lineno}.", location=self._loc())

        if not names:
            return

        # Register signature alias if provided
        if "alias" in self.options:
            alias = self.options["alias"].strip()
            if not alias or not _simple_identifier_re.fullmatch(alias):
                log.warning(f"{self.name}: alias `{alias}` is not a valid identifier.", location=self._loc())
            elif alias not in parent:
                parent[alias] = parent[names[0]]
            else:
                orig = parent[alias]
                log.warning(f"{self.name}: `{name}` (in scope `{parent.qualified_name}`) already declared in line {orig.lineno}.", location=self._loc())

        # Register declaration placeholders in domain object tree
        node_id = signode["ids"][0]
        parent = parent[names[0]]
        for name,objtype in self.placeholders:
            parent[name] = _DomainObject(node_id=node_id, objtype=objtype, docname=self.env.docname, lineno=self.lineno)
            if self._debug_enabled("print_add_target"):
                debug("add_target", f"Add placeholder: (\033[1]{parent[name]}\033)")

#-------------------------------------------------------------------------------

class PortDirective(BaseVerilogDirective):
    start_rule = "port"
    creates_scope = False

    def process_token(self, token, rules=[]):
        yield from super().process_token(token, rules)
        if token.type == "ID" and "id_port" in rules:
            self.decl_names.append(_normalize_identifier(token.value))


class ParameterDirective(BaseVerilogDirective):
    start_rule = "parameter"
    creates_scope = False

    def process_token(self, token, rules=[]):
        yield from super().process_token(token, rules)
        if token.type == "ID" and "id_parameter" in rules:
            self.decl_names.append(_normalize_identifier(token.value))


class ModuleDirective(BaseVerilogDirective):
    start_rule = "module"

    def process_token(self, token, rules=[]):
        if token.type == "ID" and "id_port" in rules:
            self.placeholders.append((_normalize_identifier(token.value), "port"))
            ref = addnodes.pending_xref("", refdomain="verilog", reftype="ref", refwarn=False, reftarget=token.value)
            ref["verilog:scope"] = self._verilog_scope + [self.decl_names[0]]
            ref["verilog:ignore_placeholders"] = True
            port_node = addnodes.desc_addname(text=token.value)
            ref += port_node
            yield ref
            return
        else:
            if token.type == "ID" and "id_module" in rules:
                self.decl_names.append(_normalize_identifier(token.value))
            yield from super().process_token(token, rules)


class VerilogXRefRole(XRefRole):
    def process_link(self, env, refnode, has_explicit_title: bool, title: str, target: str):
        env_scope = env.temp_data.get("verilog:scope", [])
        refnode["verilog:scope"] = env_scope[:]
        refnode["verilog:ignore_placeholders"] = False
        return super().process_link(env, refnode, has_explicit_title, title, target)


class _DomainObject:
    def __init__(self, name=None, node_id=None, objtype=None, docname=None, lineno=None, parent=None):
        # Verilog identifier/object tree key
        self._name = name
        # Target ID
        self.node_id = node_id
        # Type ("module", "port", ...)
        self.objtype = objtype
        # Document containing the object
        self.docname = docname
        # Line in .rst file where the object is declared
        self.lineno = lineno

        self._children = {}
        self._parent = None
        if parent is not None:
            assert isinstance(parent, self.__class__)
            assert name, "Objects with a parent must have a name."
            parent.add_children(self)

    @property
    def name(self): return self._name

    @property
    def qualified_name(self):
        return _make_qualified_identifier([a.name for a in reversed([self, *self.iter_ancestors()]) if a.name])

    @property
    def parent(self): return self._parent

    def is_placeholder(self):
        return self.parent is not None and self.parent.node_id == self.node_id

    def iter_ancestors(self):
        ancestor = self.parent
        while ancestor is not None and ancestor.name:
            yield ancestor
            ancestor = ancestor.parent

    def iter_recursive(self):
        """ Depth-first tree iteration. The node itself is not included. """
        for child in self._children.values():
            yield child
            yield from child.iter_recursive()

    def __getitem__(self, key):
        return self._children[key]

    def __setitem__(self, key, obj):
        assert isinstance(obj, self.__class__)
        assert obj != self and obj not in self.iter_ancestors()

        if key in self:
            if self[key] != obj:
                del self[key]
            else:
                return
        if obj.parent == self:
            self._children[key] = obj
            return

        if obj.parent:
            del obj.parent[obj.name]

        self._children[key] = obj
        obj._parent = self
        obj._name = key

    def __delitem__(self, key):
        if self.key_is_alias(key):
            del self._children[key]
        else:
            item = self._children[key]
            item._parent = None
            self._children = {k:v for k,v in self._children.items() if v != item}

    def key_is_alias(self, key):
        assert(key in self._children)
        return key == self._children[key].name

    # FIXME: replace with [] and remove
    def add_children(self, obj):
        assert isinstance(obj, self.__class__)
        assert obj.name
        assert obj.name not in self._children or self._children[obj.name] == obj
        self[obj.name] = obj

    def __contains__(self, key):
        return key in self._children

    def __str__(self):
        return self.qualified_name

    def _attrs_to_string(self, attrs_list=["name", "node_id", "objtype", "docname", "lineno", "parent"], template="{k}={v}"):
        return "(" + ", ".join([template.format(k=a, v=repr(str(getattr(self, a)))) for a in attrs_list if getattr(self, a)]) + ")"

    def __repr__(self):
        return (self.__class__.__name__
            + self._attrs_to_string()
            + (f"[{len(self._children)}]" if len(self._children) > 0 else ""))

    def tree_repr(self):
        result = []
        def add_entry(obj, key=None, indent=""):
            if not key or key == obj.name:
                result.append(indent + "(\033[1]" + obj.name + "\033) " + obj._attrs_to_string(["node_id"], "{v}"))
            else:
                result.append(indent + f"(\033[1;3]{key}\033)  →  (\033[1]{obj.name}\033)")
        def iter_recursive_with_nest_level(obj, indent=""):
            children = list(obj._children.items())
            for key,child in children:
                last = key==children[-1][0]
                cur_indent = ("├─ " if not last else "└─ ")
                add_entry(child, key, indent + cur_indent)
                next_indent = indent + ("│  " if not last else "   ")
                if key == child.name:
                    iter_recursive_with_nest_level(child, next_indent)

        add_entry(self)
        iter_recursive_with_nest_level(self)

        return "\n".join(result)


class VerilogDomain(Domain):
    name = "verilog"
    label = "Verilog domain"
    roles = {
        "ref": VerilogXRefRole()
    }
    directives = {
        "module": ModuleDirective,
        "parameter": ParameterDirective,
        "port": PortDirective,
    }
    initial_data = {
        "objects": _DomainObject(name="$root"),
    }

    def _debug_enabled(self, cat):
        return cat in self.env.app.config.verilog_domain_debug

    def get_objects(self):
        for obj in self.data["objects"].iter_recursive():
            yield obj.qualified_name, obj.qualified_name, obj.objtype, obj.docname, obj.node_id, 1

    def resolve_xref(self, env, fromdocname, builder, typ, target, node, contnode):
        if self._debug_enabled("print_objects_tree") and not hasattr(self, "_dbg_resolve_xref_executed"):
            self._dbg_resolve_xref_executed = True
            debug("objects_tree", self.data["objects"].tree_repr())

        identifiers = [_normalize_identifier(i) for i in _split_qualified_identifier(target)]

        if len(identifiers) == 0 or (len(identifiers) == 1 and identifiers[0] == "$root"):
            return None

        obj = self.data["objects"]

        if identifiers[0] != "$root":
            scope_identifiers = node.attributes.get("verilog:scope", [])
            try:
                for s in scope_identifiers:
                    obj = obj[s]
            except:
                scope = _make_qualified_identifier(scope_identifiers)
                log.warning(f"{target}: reference created in non-existent scope `{scope}`.")
                return None

            # Find first identifier's scope
            while obj and identifiers[0] not in obj:
                obj = obj.parent
            if not obj:
                log.warning(f"{target}: reference not found.")
                return None
            obj = obj[identifiers[0]]

        # Follow remaining identifiers
        try:
            for identifier in identifiers[1:]:
                obj = obj[identifier]
        except:
            log.warning(f"{target}: reference not found.")
            return None

        ignore_placeholders = node.attributes.get("verilog:ignore_placeholders", False)
        if ignore_placeholders and obj.is_placeholder():
            return None

        return make_refnode(builder, fromdocname, obj.docname, obj.node_id, contnode, f"{obj.objtype} {obj.name}")

def setup(app):
    app.add_config_value('verilog_domain_debug', [], '')
    app.add_domain(VerilogDomain)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
