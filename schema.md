
# Ontology Graph

A property graph for ontologies based on OBO/OWL ontology structures.



# Ontology

The root of the ontology

Keys: id

## Properties

|Property|Type|Description|
|--------|----|-----------|
|data-version|string|a version string|
|date|datetime|the creation date of the ontology|
|default-namespace|string|the default namespace to use for the ontology|
|format-version|string|the input format version|
|ontology|string|the identifier for the ontology which may be the same as the id|
|remark|string|a comment|
|saved-by|string|an identification of the process that generated the format|

## Relations

|Relation|Directed|Target|
|--------|--------|------|
|:subsetdef|yes|:Subset|
|:term|yes|:Term|
|:typedef|yes|:Typedef|

# Term

Keys: id

## Properties

|Property|Type|Description|
|--------|----|-----------|
|comment|string||
|created_by|string||
|creation_date|string||
|def|string||
|is_obsolete|string||
|name|string||

## Relations

|Relation|Directed|Target|
|--------|--------|------|
|:alias|yes|:Term|
|:def|yes|:Resource|
|:subset|yes|:Subset|
|:synonym|yes|:XRef|
|:xref|yes|:XRef|
|:is_a|yes|:Term|
|:disjoint_from|yes|:Term|

# Typedef

Keys: id

## Properties

|Property|Type|Description|
|--------|----|-----------|
|def|string||
|name|string||

## Relations

|Relation|Directed|Target|
|--------|--------|------|
|:def|yes|:Resource|

# Resource

Keys: url

# Subset

Keys: id

## Properties

|Property|Type|Description|
|--------|----|-----------|
|description|string||

# XRef

Keys: id

## Properties

|Property|Type|Description|
|--------|----|-----------|
|related|string||
|relation|string||

