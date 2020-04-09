from lark import Lark
import re
from datetime import datetime


grammar = r"""
?ontology: header (term | typedef)+
header: property+
term: _term_start property+
typedef: _typedef_start property+
property: NAME ":" _WS_INLINE VALUE _NEWLINE
_term_start: _TERM _WS_INLINE? _NEWLINE
_typedef_start: _TYPEDEF _WS_INLINE? _NEWLINE

_TERM: "[Term]"
_TYPEDEF: "[Typedef]"
VALUE: /[^\n\r]+/
NAME: LETTER ("_"|"-"|LETTER|DIGIT)*
_WS_INLINE: WS_INLINE
_NEWLINE: NEWLINE

%import common.NEWLINE
%import common.WS_INLINE
%import common.LETTER
%import common.DIGIT

"""

property_value_grammar = r"""
property_value: (CURIE | URI | NAME ) (ESCAPED_STRING | CURIE | URI ) (CURIE | URI) ? ("{" (URI ("," URI)*)? "}")?

URI.3: ("a".."z"|"A".."Z"|"0".."9"|"."|"-"|"_")+ (":" /([^ \t,\]\\}#]|\\[^\\]|\\\\)+/)? ("#xref=" ESCAPED_STRING)?
CURIE.2: ("a".."z"|"A".."Z"|"0".."9"|"."|"-"|"_")+ ":" ("a".."z"|"A".."Z"|"0".."9"|"."|"-"|"_")+
NAME: ("a".."z"|"A".."Z"|"0".."9"|"."|"-"|"_")+
%import common.ESCAPED_STRING
%import common.WS
%ignore WS
"""

is_a_value_grammar = r"""
is_a: CURIE ("{" _URI "}")? ("!" VALUE)?
CURIE: ("a".."z"|"A".."Z"|"0".."9"|"."|"-"|"_")+ (":" ("a".."z"|"A".."Z"|"0".."9"|"."|"-"|"_")+)?
VALUE: /[^\n\r]+/
_URI: ("a".."z"|"A".."Z")+ ":" /([^ \t,\]\\}]|\\[^\\]|\\\\)+/

%import common.WS
%ignore WS
"""

def_value_grammar = r"""
def: ESCAPED_STRING "[" (URI ( "," URI)*)? "]" _COMMENT?

URI: ("a".."z"|"A".."Z")+ ":" /([^ \t,\]\\]|\\[^\\]|\\\\)+/
_COMMENT: "{" /[^}]+/ "}"
%import common.ESCAPED_STRING
%import common.WS
%ignore WS
"""

synonym_value_grammar = r"""
synonym: ESCAPED_STRING RELATION "[" (CURIE ("," CURIE)*)? "]"

RELATION: ("a".."z"|"A".."Z"|"0".."9"|"."|"-"|"_")+
CURIE: ("a".."z"|"A".."Z"|"0".."9"|"."|"-"|"_")+ ":" ("a".."z"|"A".."Z"|"0".."9"|"."|"-"|"_")+
%import common.ESCAPED_STRING
%import common.WS
%ignore WS
"""

class Ontology:
   def __init__(self):
      self.metadata = {}
      self.metadata['subsetdef'] = {}
      self.metadata['property_value'] = {}
      self.terms = {}
      self.typedefs = {}

def unescape_literal(value):
   if value[0]=='"' and value[-1]=='"':
      value = value[1:-1].replace(r'\"','"')
   return value

class OBOParser:

   def __init__(self):
      self.parser = Lark(grammar,parser='lalr',start='ontology')
      self.property_value_parser = Lark(property_value_grammar,parser='lalr',start='property_value')
      self.is_a_value_parser = Lark(is_a_value_grammar,parser='lalr',start='is_a')
      self.def_value_parser = Lark(def_value_grammar,parser='lalr',start='def')
      self.synonym_value_parser = Lark(synonym_value_grammar,parser='lalr',start='synonym')
      self.obo_datetime = re.compile('(\d\d):(\d\d):(\d\d\d\d) (\d\d):(\d\d)')

   def parse(self,source):
      ontology = Ontology()

      if type(source)!=str:
         source = source.read()

      ontology_tree = self.parser.parse(source)

      header_tree = ontology_tree.children[0]
      for property in header_tree.children:
         name = property.children[0].value
         value = property.children[1].value
         if name not in ['subsetdef','property_value']:
            ontology.metadata[name] = self._parse_value(name,value)
         elif name=='subsetdef':
            value = value.strip()
            space = value.find(' ')
            id = value[0:space]
            description = unescape_literal(value[space:].strip())
            ontology.metadata.get(name)[id] = description
         elif name=='property_value':
            property_value_tree = self.property_value_parser.parse(value)
            id, *value = list(map(lambda token: unescape_literal(token.value), property_value_tree.children))
            value = tuple(value)
            if len(value)==1:
               value = value[0]
            properties = ontology.metadata.get(name)
            if id not in properties:
               properties[id] = []
            properties[id].append(value)
      for item in ontology_tree.children[1:]:
         if item.data=='term':
            id, data = self._multidict(item)
            if id is not None:
               ontology.terms[id] = data
         else:
            id, data = self._multidict(item)
            if id is not None:
               ontology.typedefs[id] = data

      return ontology

   def _parse_value(self,name,value):
      if name=='is_a' or name=='disjoint_from':
         tree = self.is_a_value_parser.parse(value)
         value = tree.children[0].value
      elif name=='is_obsolete':
         if value=='true':
            value = True
         elif value=='false':
            value = False
      elif name=='def':
         tree = self.def_value_parser.parse(value)
         value = tuple(map(lambda token: unescape_literal(token.value),tree.children))
      elif name=='date':
         m = self.obo_datetime.match(value)
         if m is not None:
            dtinfo = list(map(int,m.groups()))
            value = datetime(dtinfo[2],dtinfo[1],dtinfo[0],dtinfo[3],dtinfo[4]).isoformat()
      elif name=='synonym':
         tree = self.synonym_value_parser.parse(value)
         description, relation, *curies = list(map(lambda token: unescape_literal(token.value),tree.children))
         value = (description, relation, curies)
      elif name=='property_value':
         property_value_tree = self.property_value_parser.parse(value)
         id, *value = list(map(lambda token: unescape_literal(token.value), property_value_tree.children))
         value = tuple(value)
         if len(value)==1:
            value = value[0]
         value = (id, value)
      return value

   def _multidict(self,item):
      id = None
      data = {}
      for property in item.children:
         name = property.children[0].value
         value = property.children[1].value
         if name=='id':
            id = value
         # TODO: specific parsers
         pvalue = self._parse_value(name,value)
         if name=='property_value' and pvalue[0]=='http://purl.obolibrary.org/obo/def':
            name = 'def'
            pvalue = tuple([pvalue[1][0]] + list(pvalue[1][2:]))
         if name not in data:
            data[name] = []
         data[name].append(pvalue)
      return (id,data)

if __name__ == '__main__':
   import sys, pprint
   pp = pprint.PrettyPrinter(indent=2)
   for file in sys.argv[1:]:
      parser = OBOParser()
      with open(file,'r') as input:
         ontology = parser.parse(input)
         #pp.pprint(ontology.metadata)
         pp.pprint(ontology.terms)
         #pp.pprint(ontology.typedefs)
