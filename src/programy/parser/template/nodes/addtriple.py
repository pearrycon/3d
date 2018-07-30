"""
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.utils.logging.ylogger import YLogger

from programy.parser.template.nodes.triple import TemplateTripleNode
from programy.parser.exceptions import ParserException


class TemplateAddTripleNode(TemplateTripleNode):

    def __init__(self, subj=None, pred=None, obj=None):
        TemplateTripleNode.__init__(self, node_name="addtriple", subj=subj, pred=pred, obj=obj)

    def resolve_to_string(self, client_context):
        rdf_subject = self._subj.resolve(client_context)
        rdf_predicate = self._pred.resolve(client_context)
        rdf_object = self._obj.resolve(client_context)

        client_context.brain.rdf.add_entity(rdf_subject, rdf_predicate, rdf_object, "USERDEFINED")
        resolved = ""
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def resolve(self, client_context):
        try:
            return self.resolve_to_string(client_context)
        except Exception as excep:
            YLogger.exception(client_context, "Failed to resolve", excep)
            return ""

    def to_string(self):
        return "ADDTRIPLE"

    def to_xml(self, client_context):
        xml = "<addtriple>"
        xml += self.children_to_xml(client_context)
        xml += "</addtriple>"
        return xml

    #######################################################################################################
    # ADDTRIPLE_EXPRESSION ::== <addtriple>TEMPLATE_EXPRESSION</addtriple>

    def parse_expression(self, graph, expression):
        super(TemplateAddTripleNode, self).parse_expression(graph, expression)

        if self._subj is None:
            raise ParserException("<%s> node missing subject attribue/element"%self.node_name)

        if  self._pred is None:
            raise ParserException("<%s> node missing predicate attribue/element"%self.node_name)

        if self._obj is None:
            raise ParserException("<%s> node missing object attribue/element"%self.node_name)
