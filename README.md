# RDF Work Generator

Generate RDF about a Work described in a Bulkrax sheet so it can be versioned in 
Github, Fedora, or elsewhere.

```shell

python versioner/version.py -s sheets/kintner_with_collections.csv -o output -p utk.yml -r turtle

```

## Flags

* **-s**: your import sheet
* **-o**: where to save your rdf
* **-p**: path to your m3 profile
* **-r**: specify your rdf serialization.  Must be one of: turtle, rdf-xml, json-ld, n3.