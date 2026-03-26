# TravelPugliaKG

Tabular data https://dati.puglia.it/ckan/dataset/luoghi-di-interesse-turistico-culturale-naturalistico-progressivo#

OntoPiA ontologies: https://github.com/italia/dati-semantic-assets

[Download KG](10.6084/m9.figshare.30168661)

Matey: https://rml.io/yarrrml/matey/#

RML mapper: https://github.com/RMLio/rmlmapper-java

Function ontology: https://fno.io/

Function specifications: 
- https://users.ugent.be/~bjdmeest/function/grel.ttl
- https://w3id.org/imec/idlab/function

Other YARRRML examples are in the test folder of https://github.com/RMLio/yarrrml-parser. It includes also examples using functions, but, as far as we can tell, no examples with string_replace and string_substring.


# Use Case: Select tourist destinations based on user preferences

## Description
The application selects tourist destinations for tourists based on their preferences collected through a preference elicitation form.

## Actors
- Tourist  
- Application querying the Knowledge Graph (KG)

## Triggers
- The user logs in  
- The user starts the registration procedure  

## Flows

### Flow 1 — Registration and recommendation
1. The user starts the registration.  
2. A preference elicitation form requests:
   - a score (1–5 Likert scale) for each of ten tourist interests  
   - a date range  
   - a location  
3. The registration procedure succeeds.  
4. The application shows tourist destinations selected based on the user preferences.  

### Flow 2 — Login and recommendation
1. The user logs into the application.  
2. The application shows tourist destinations selected based on the preferences specified during registration.  