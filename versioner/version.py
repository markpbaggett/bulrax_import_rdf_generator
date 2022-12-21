import csv
import yaml
from rdflib import Graph, URIRef, Literal
from fastprogress.fastprogress import progress_bar
from tqdm import tqdm
import argparse


class ImportVersioner:
    def __init__(self, import_sheet, output_directory, profile):
        self.sheet = import_sheet
        self.output = output_directory
        self.profile = profile
        self.uri_pattern_for_subjects = "http://utk-metadata-object/"
        self.profile_as_yaml = yaml.safe_load(open(profile))['properties']
        self.lines = self.__get_lines_in_sheet(import_sheet)
        self.__read_sheet(import_sheet)

    @staticmethod
    def __get_lines_in_sheet(sheet):
        lines = 0
        with open(sheet, 'r') as csv_file:
            lines = len(csv_file.readlines()) - 1
        return lines

    def __read_sheet(self, sheet):
        with open(sheet, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in tqdm(reader, total=self.lines):
                if row['model'] != "Attachment" and row['model'] != "Fileset":
                    self.__create_metadata_file(row)

    def __create_metadata_file(self, row):
        g = Graph()
        for k, v in progress_bar(row.items()):
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
    import argparse
    parser = argparse.ArgumentParser(description='Generate RDF about a work from a Bulkrax Import CSV.')
    parser.add_argument("-s", "--sheet", dest="sheet", help="Path to your importer CSV", required=True)
    parser.add_argument("-p", "--profile", dest="profile", help="Path to m3 profile.", required=True)
    parser.add_argument("-o", "--output", dest="output", help="Path to where to save your rdf files.", required=True)
    args = parser.parse_args()
    x = ImportVersioner(
        import_sheet=args.sheet,
        output_directory=args.output,
        profile=args.profile
    )
