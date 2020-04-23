from io import StringIO

def cypher_literal(value):
   return value.replace('\n',r'\n').replace("'",r"\'")

def query_create_ontology(ontology,**options):
   q = StringIO()
   merge = options.get('merge',True)
   id = options.get('id',ontology.metadata.get('ontology'))
   if merge:
      q.write("MERGE (o:Ontology {{id: '{id}'}}) ON CREATE\n".format(id=id))
   else:
      q.write("CREATE (o:Ontology {{id: '{id}'}})\n".format(id=id))
   first = True
   for name in ['data-version','date','default-namespace','format-version','ontology','remark','saved-by']:
      value = ontology.metadata.get(name)
      if value is None:
         continue
      if first:
         q.write('SET ')
         first = False
      else:
         q.write(',\n    ')
      q.write("o.`{name}` = '{value}'".format(name=name,value=cypher_literal(value)))
   properties = ontology.metadata.get('property_value')
   for property in properties.keys() if properties is not None else []:
      value = ','.join(map(lambda value: value[0] if type(value)==tuple else value,properties[property]))
      q.write(',\n    ')
      q.write("o.`{name}` = '{value}'".format(name=property,value=cypher_literal(value)))
   q.write('\n')
   subsetdefs = ontology.metadata.get('subsetdef')
   for name in subsetdefs.keys() if subsetdefs is not None else []:
      description = subsetdefs.get(name)
      q.write("MERGE (o)-[:subsetdef]->(:Subset {{id: '{id}', description:'{description}'}})\n".format(id=cypher_literal(name),description=cypher_literal(description)))
   return q.getvalue()

def query_create_term(ontology,term,**options):
   q = StringIO()
   merge = options.get('merge',True)
   ontology_id = options.get('id',ontology.metadata.get('ontology'))
   id = term.get('id')[0]
   q.write("MATCH (o:Ontology {{id: '{id}'}})\n".format(id=ontology_id))
   for index, subset in enumerate(term.get('subset',[])):
      q.write("MATCH (subset{index}:Subset {{id: '{id}'}})\n".format(index=index,id=subset))
   if merge:
      q.write("MERGE (t:Term {{id: '{id}'}}) ON CREATE\n".format(id=id))
   else:
      q.write("CREATE (t:Term {{id: '{id}'}})\n".format(id=id))
   first = True
   for name in ['comment','created_by','creation_date','def','is_obsolete','name']:
      value = term.get(name)
      if value is None:
         continue
      # All these values are singletons
      value = value[0]
      if type(value)==tuple:
         value = value[0]
      if first:
         q.write('SET ')
         first = False
      else:
         q.write(',\n    ')
      if type(value)==bool:
         q.write("t.`{name}` = {value}".format(name=name,value='true' if value else 'false'))
      else:
         q.write("t.`{name}` = '{value}'".format(name=name,value=cypher_literal(value)))
   for property, value in term.get('property_value',[]):
      if type(value)==tuple:
         value = value[0]
      q.write(',\n    ')
      q.write("t.`{name}` = '{value}'".format(name=property,value=cypher_literal(value)))
   q.write('\n')

   q.write('MERGE (o)-[:term]->(t)\n')

   for index, alt_id in enumerate(term.get('alt_id',[])):
      q.write("MERGE (alt_id{index}:Term {{id: '{id}', alias: true}})\n".format(index=index,id=alt_id))
      q.write("MERGE (alt_id{index})-[:alias]->(t)\n".format(index=index))
   if 'def' in term:
      definition = term['def'][0]
      if type(definition)==tuple:
         for url in list(definition)[1:]:
            q.write("MERGE (t)-[:def]->(:Resource {{url: '{url}'}})\n".format(url=cypher_literal(url)))
   for index, subset in enumerate(term.get('subset',[])):
      q.write("MERGE (t)-[:subset]->(subset{index})\n".format(index=index))
   for index, synonym in enumerate(term.get('synonym',[])):
      q.write("CREATE (synonym{index}:XRef {{name: '{id}', relation: '{relation}', related: '{targets}'}})\n".format(index=index,id=cypher_literal(synonym[0]),relation=synonym[1],targets=','.join(synonym[2])))
      q.write("CREATE (t)-[:synonym]->(synonym{index})\n".format(index=index))
   for index, xref in enumerate(term.get('xref',[])):
      q.write("CREATE (xref{index}:XRef {{id: '{id}'}})\n".format(index=index,id=xref))
      q.write("CREATE (t)-[:xref]->(xref{index})\n".format(index=index))
   return q.getvalue()

def query_cross_reference_term(ontology,term,**options):
   if 'is_a' not in term or 'disjoint_from' not in term:
      return None
   q = StringIO()
   id = term.get('id')[0]
   q.write("MATCH (t:Term {{id: '{id}'}})\n".format(id=id))
   for index, xref in enumerate(term.get('is_a',[])):
      q.write("MATCH (is_a{index}:Term {{id: '{id}'}})\n".format(index=index,id=xref))
   for index, xref in enumerate(term.get('disjoint_from',[])):
      q.write("MATCH (disjoint_from{index}:Term {{id: '{id}'}})\n".format(index=index,id=xref))
   for index, xref in enumerate(term.get('is_a',[])):
      q.write("MERGE (t)-[:is_a]->(is_a{index})\n".format(index=index))
   for index, xref in enumerate(term.get('disjoint_from',[])):
      q.write("MERGE (t)-[:disjoint_from]->(disjoint_from{index})\n".format(index=index))
   return q.getvalue()

def query_create_typedef(ontology,typedef,**options):
   q = StringIO()
   merge = options.get('merge',True)
   ontology_id = options.get('id',ontology.metadata.get('ontology'))
   id = typedef.get('id')[0]
   q.write("MATCH (o:Ontology {{id: '{id}'}})\n".format(id=ontology_id))
   if merge:
      q.write("MERGE (t:Typedef {{id: '{id}'}}) ON CREATE\n".format(id=id))
   else:
      q.write("CREATE (t:Typedef {{id: '{id}'}})\n".format(id=id))
   first = True
   for name in ['def','name']:
      value = typedef.get(name)
      if value is None:
         continue
      # All these values are singletons
      value = value[0]
      if type(value)==tuple:
         value = value[0]
      if first:
         q.write('SET ')
         first = False
      else:
         q.write(',\n    ')
      if type(value)==bool:
         q.write("t.`{name}` = {value}".format(name=name,value='true' if value else 'false'))
      else:
         q.write("t.`{name}` = '{value}'".format(name=name,value=cypher_literal(value)))
   q.write('\n')
   q.write('MERGE (o)-[:typedef]->(t)\n')
   if 'def' in typedef:
      definition = typedef['def'][0]
      if type(definition)==tuple:
         for url in list(definition)[1:]:
            q.write("MERGE (t)-[:def]->(:Resource {{url: '{url}'}})\n".format(url=cypher_literal(url)))
   return q.getvalue()

def query_generate(ontology,**options):

   scope = options.get('scope',['ontology','term','xref','typedef'])

   if 'ontology' in scope:
      yield query_create_ontology(ontology,**options)

   if 'term' in scope:
      for id in ontology.terms.keys():
         term = ontology.terms[id]
         yield query_create_term(ontology,term,**options)

   if 'xref' in scope:
      for id in ontology.terms.keys():
         term = ontology.terms[id]
         q = query_cross_reference_term(ontology,term,**options)
         if q is not None:
            yield q

   if 'typedef' in scope:
      for id in ontology.typedefs.keys():
         typedef = ontology.typedefs[id]
         yield query_create_typedef(ontology,typedef,**options)
