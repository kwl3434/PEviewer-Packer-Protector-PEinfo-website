from docutils.parsers.rst.directives import register_directive
from .directives import CodeBlock, Define, Undefine, IfDef, IfNDef, StyleSheet, Script, Template


def register_directives():
    register_directive('code-block', CodeBlock)
    register_directive('code', CodeBlock)
    register_directive('sourcecode', CodeBlock)
    register_directive('define', Define)
    register_directive('undef', Undefine)
    register_directive('undefine', Undefine)
    register_directive('ifdef', IfDef)
    register_directive('ifndef', IfNDef)
    register_directive('stylesheet', StyleSheet)
    register_directive('script', Script)
    register_directive('template', Template)
