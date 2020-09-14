from sphinx.application import Sphinx
from .verilogdomain import VerilogDomain

def setup(app: Sphinx):
    app.add_config_value('verilog_domain_debug', [], '')
    app.add_domain(VerilogDomain)

    return {
        "version": "0.0.2",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
