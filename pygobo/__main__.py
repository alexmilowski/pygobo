import argparse
import sys
import pprint

from pygodo import OBOParser, query_generate

if __name__ == '__main__':

   argparser = argparse.ArgumentParser(description='Article importer')
   argparser.add_argument('--host',help='Redis host',default='0.0.0.0')
   argparser.add_argument('--port',help='Redis port',type=int,default=6379)
   argparser.add_argument('--password',help='Redis password')
   argparser.add_argument('--show-query',help='Show the cypher queries before they are run.',action='store_true',default=False)
   argparser.add_argument('--graph',help='The graph name',default='obo')
   argparser.add_argument('--scope',help='The scope of the operation',choices=['all','ontology','term','xref','typedef'],action='append')
   argparser.add_argument('--option',help='An option to the operation',choices=['show-xrefs'],action='append')
   argparser.add_argument('operation',help='The operation to perform',choices=['parse','cypher','load','structure'])
   argparser.add_argument('files',nargs='*',help='The files to process.')

   args = argparser.parse_args()

   pp = pprint.PrettyPrinter(indent=2)
   if len(args.files)==0:
      sources = [sys.stdin]
   else:
      sources = args.files
   for source in sources:
      parser = OBOParser()
      with open(source,'r') if type(source)==str else source as input:
         ontology = parser.parse(input)

         if args.operation=='parse':
            if args.scope is None or 'all' in args.scope:
               args.scope = ['ontology','term','typedef']

            if 'ontology' in args.scope:
               print('Ontology:')
               pp.pprint(ontology.metadata)
            if 'term' in args.scope:
               print('Terms:')
               pp.pprint(ontology.terms)
            if 'typedef' in args.scope:
               print('Typedefs:')
               pp.pprint(ontology.typedefs)

         elif args.operation=='cypher':
            if args.scope is None or 'all' in args.scope:
               args.scope = ['ontology','term','xref','typedef']

            for query in query_generate(ontology,scope=args.scope):
               print(query)
               print(';')

         elif args.operation=='load':
            import redis
            from redisgraph import Graph
            r = redis.Redis(host=args.host,port=args.port,password=args.password)
            graph = Graph(args.graph,r)

            if args.scope is None or 'all' in args.scope:
               args.scope = ['ontology','term','xref','typedef']

            for query in query_generate(ontology,scope=args.scope):
               if args.show_query:
                  print(query)
                  print(';')
               graph.query(query)

         elif args.operation=='structure':
            if args.scope is None or 'all' in args.scope:
               args.scope = ['ontology','term','typedef']

            if 'ontology' in args.scope:
               print('Ontology:')
               for name in sorted(ontology.metadata.keys()):
                  print('  '+name)
                  if name=='property_value':
                     for property in ontology.metadata['property_value'].keys():
                        print('    '+property)
                  elif name=='subsetdef':
                     for property in ontology.metadata['subsetdef'].keys():
                        print('    '+property)
            if 'term' in args.scope:
               print('Term:')
               structure = {}
               xrefs = {}
               properties = {}
               do_xrefs = ('show-xrefs' in args.option) if args.option is not None else False
               for typedef in ontology.terms.keys():
                  term = ontology.terms[typedef]
                  if do_xrefs:
                     for name in term.get('xref',[]):
                        xrefs[name] = True
                  for name,value in term.get('property_value',[]):
                     properties[name] = True
                  for name in term.keys():
                     structure[name] = True
               for name in sorted(structure.keys()):
                  print('  '+name)
                  if do_xrefs and name=='xref':
                     for xref in sorted(xrefs.keys()):
                        print('    '+xref)
                  if name=='property_value':
                     for property in sorted(properties.keys()):
                        print('    '+property)
            if 'typedef' in args.scope:
               print('Typedef:')
               structure = {}
               for typedef in ontology.typedefs.keys():
                  for name in ontology.typedefs[typedef].keys():
                     structure[name] = True
               for name in sorted(structure.keys()):
                  print('  '+name)
