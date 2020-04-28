
# Ontology Graph

A property graph for ontologies based on OBO/OWL ontology structures.



# Ontology

The root of the ontology

**Keys:** *id*

## Properties

<table>
<thead><tr><th>Property</th><th>Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>data-version</td><td>string</td><td>

a version string

</td></tr>
<tr><td>date</td><td>datetime</td><td>

the creation date of the ontology

</td></tr>
<tr><td>default-namespace</td><td>string</td><td>

the default namespace to use for the ontology

</td></tr>
<tr><td>format-version</td><td>string</td><td>

the input format version

</td></tr>
<tr><td>id</td><td>string</td><td>

an identifier for the ontology in the graph

</td></tr>
<tr><td>ontology</td><td>string</td><td>

the identifier for the ontology which may be the same as the id

</td></tr>
<tr><td>remark</td><td>string</td><td>

a comment

</td></tr>
<tr><td>saved-by</td><td>string</td><td>

an identification of the process that generated the format

</td></tr>
</tbody>
</table>

## Relations

<table>
<thead><tr><th>Relation</th><th>Directed</th><th>Target</th></tr></thead>
<tbody>
<tr><td rowspan=2>:subsetdef</td><td>yes</td><td>:Subset</td></tr>
<tr><td colspan=2>


A subset of the ontology. Terms identify themselves as member of a subset.


</td></tr>
<tr><td rowspan=2>:term</td><td>yes</td><td>:Term</td></tr>
<tr><td colspan=2>

a term belonging to the ontology

</td></tr>
<tr><td rowspan=2>:typedef</td><td>yes</td><td>:Typedef</td></tr>
<tr><td colspan=2>

a type definition belonging to the ontology

</td></tr>
</tbody>
</table>

# Term

**Keys:** *id*

## Properties

<table>
<thead><tr><th>Property</th><th>Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>comment</td><td>string</td><td></td></tr>
<tr><td>created_by</td><td>string</td><td></td></tr>
<tr><td>creation_date</td><td>string</td><td></td></tr>
<tr><td>def</td><td>string</td><td></td></tr>
<tr><td>id</td><td>string</td><td>

an identifier for the term in the graph. This is often the same as `name`

</td></tr>
<tr><td>is_obsolete</td><td>string</td><td></td></tr>
<tr><td>name</td><td>string</td><td>

the term identifier in the ontology

</td></tr>
</tbody>
</table>

## Relations

<table>
<thead><tr><th>Relation</th><th>Directed</th><th>Target</th></tr></thead>
<tbody>
<tr><td>:alias</td><td>yes</td><td>:Term</td></tr>
<tr><td>:def</td><td>yes</td><td>:Resource</td></tr>
<tr><td>:subset</td><td>yes</td><td>:Subset</td></tr>
<tr><td>:synonym</td><td>yes</td><td>:XRef</td></tr>
<tr><td>:xref</td><td>yes</td><td>:XRef</td></tr>
<tr><td>:is_a</td><td>yes</td><td>:Term</td></tr>
<tr><td>:disjoint_from</td><td>yes</td><td>:Term</td></tr>
</tbody>
</table>

# Typedef

**Keys:** *id*

## Properties

<table>
<thead><tr><th>Property</th><th>Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>def</td><td>string</td><td></td></tr>
<tr><td>name</td><td>string</td><td></td></tr>
</tbody>
</table>

## Relations

<table>
<thead><tr><th>Relation</th><th>Directed</th><th>Target</th></tr></thead>
<tbody>
<tr><td>:def</td><td>yes</td><td>:Resource</td></tr>
</tbody>
</table>

# Resource

**Keys:** *url*

# Subset

**Keys:** *id*

## Properties

<table>
<thead><tr><th>Property</th><th>Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>description</td><td>string</td><td></td></tr>
</tbody>
</table>

# XRef

**Keys:** *id*

## Properties

<table>
<thead><tr><th>Property</th><th>Type</th><th>Description</th></tr></thead>
<tbody>
<tr><td>related</td><td>string</td><td></td></tr>
<tr><td>relation</td><td>string</td><td></td></tr>
</tbody>
</table>

