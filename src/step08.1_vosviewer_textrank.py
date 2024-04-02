import json
import pathlib
from co_occurrence_calculation import CoCalculator


ROOT = pathlib.Path(__file__).resolve().parent.parent

if __name__ == "__main__":
    c = CoCalculator()
    with open(ROOT / "output" / "dataset.json" ) as json_file:
        data = json.load(json_file)
    c.set_data(data)
    c.calculate_all()
    c.export_vos_viewer_topics_co_occurring("vos_textrank.json",
                                            degree_limit= 0,
                                            link_weight_limit=7)
 