import csv
import yaml
from rdflib import Graph, URIRef, Literal


class ImportVersioner:
    def __init__(self, import_sheet, output_directory, profile):
        self.sheet = import_sheet
        self.output = output_directory
        self.profile = profile
        self.uri_pattern_for_subjects = "http://utk-metadata-object/"
        self.profile_as_yaml = yaml.safe_load(open(profile))['properties']
        self.__read_sheet(import_sheet)

    def __read_sheet(self, sheet):
        with open(sheet, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['model'] != "Attachment" and row['model'] != "Fileset":
                    self.__create_metadata_file(row)

    def __create_metadata_file(self, row):
        g = Graph()
        for k, v in row.items():
            for key, value in self.profile_as_yaml.items():
                if k == key:
                    if v != "":
                        values_to_mint = v.split(' | ')
                        for new_value in values_to_mint:
                            if new_value.startswith('http'):
                                minted_object = URIRef(new_value)
                            else:
                                minted_object = Literal(new_value)
                            g.add(
                                (
                                    URIRef(f"{self.uri_pattern_for_subjects}{row['source_identifier']}"),
                                    URIRef(value['property_uri']),
                                    minted_object
                                )
                            )
                with open(f"{self.output}/{row['source_identifier']}.ttl", 'wb') as rdf:
                    rdf.write(
                        g.serialize(format='turtle', indent=4).encode("utf-8")
                    )
        return


if __name__ == "__main__":
    my_yaml = "utk.yml"
    output = "output"
    sheet = "sheets/kintner_with_collections.csv"
    x = ImportVersioner(sheet, output, my_yaml)

