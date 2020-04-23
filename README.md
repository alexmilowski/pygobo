# Property Graphs for Open Biological Ontologies
Property Graphs library for Open Biological and Biomedical Ontologies (OBO) in
Python. This library supports reading OBO formatted ontologies into python
data structures. It also supports generation of cypher statements to load
the ontology into a property graph database like RedisGraph.

## Using the command-line interface

The module can be invoked directly and provides a set of basic commands that
allow parsing, inspection, cypher statement generation, and loading ontologies.

The invocation is:

```sh
python -m pygobo {operation} {file ...}?
```

where `operation` is one of:

   * `parse` - parse the ontology syntax
   * `cypher` - generate cypher create/merge statements
   * `load` - load the ontology into a property graph database
   * `structure` - output the general structure of the ontology

The operations can be scoped via the `--scope` option that takes the values:

   * `all` - all the components
   * `ontology` - only the top-level ontology metadata
   * `term` - only the ontology terms
   * `xref` - only the cross references
   * `typedef` - only the type definitions.

The scope option can be used multiple times to display different items.

If the file is omitted, the command will read from stdin. Otherwise, each
file specified will be read and operated on in the order they are specified.

## Loading ontology property graphs

The module currently supports loading ontologies directly into [RedisGraph](https://github.com/RedisGraph/RedisGraph).

The following options can be specified for connecting to the database:

 * `--host {name}|{ip}` - the host of the database, defaults to 0.0.0.0
 * `--port {port}` - the port, defaults to 6379
 * `--password {password}` - the database password, default is no password
 * `--graph {key}` - the graph key, defaults to "obo"

Adding the `--show-query` option will allow you to see the Cypher statements as
they are executed.

The `--scope` option will limit the loading to a specific aspect of the
ontology but the order is presumed to be: ontology, term, xref, typedef. If you
violate this ordering, the cypher statements may fail.

## API

### OBOParser

An ontology can be easily loaded from a stream source:

```python
from pygobo import OBOParser
parser = OBOParser()
with open('ontology.obo','r') as input:
   ontology = parser.parse(input)
```

### Ontology

An ontology is a simple class with the following fields:

 * `metadata` - a dictionary of ontology metadata
 * `terms` - a dictionary of ontology terms
 * `typedefs` - a dictionary of ontology type definitions

Some property values are structured dictionaries, some are tuples, and some
are simple values.

### Generating Cypher

Once an ontology is loaded, the `query_generate` function can be used
to generate cypher load statements. The usage is:

```python
for query in query_generate(ontology,scope=['ontology']):
   print(query)
   print(';')
```

The `scope` keyword argument is a list of scope values. The values are the
same as the command-line interface (see above).
