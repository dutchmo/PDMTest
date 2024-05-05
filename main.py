import json
from typing import Dict, Any

from glom import glom, Iter, T, Merge, Coalesce, assign

from gui import StopwatchApp

def print_hi(name: str) -> None:
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

def load_and_convert_json() -> Dict[str, Any]:
    # load file dataset.json
    with open('dataset.json', 'r') as file:
        json_document = json.load(file)
    return json_document

def default_factory(stuff) -> Dict[str, Any]:
    print(stuff)
    return "Couldnt find"

planets = {
   "pluto": {"moons": 6, "population": None},
   "venus": {"population": {"aliens": 5}},
   "earth": {"moons": 1, "population": {"humans": 7700000000, "aliens": 1}},
}

if __name__ == '__main__':
    print_hi('PyCharm')
    app = StopwatchApp()
    json_document = load_and_convert_json()
    spec = ('DataSet.PhysicalTableMap', T.items()['Name'])
    spec = ('DataSet.PhysicalTableMap', Iter().first())
    dset_id  = glom(json_document, spec)
    spec2 = (f'DataSet.PhysicalTableMap.{dset_id}', Coalesce('Other', 'RelationalTable', default_factory), )
    #spec2 = (f'DataSet.PhysicalTableMap.{dset_id}', ('Other', 'RkelationalTable', default_factory), )

    result = glom(json_document, spec2, )

    _ = assign(result, 'Name', 'updated dataset name')
    _ = assign(json_document, f'DataSet.PhysicalTableMap.{dset_id}', result)
    print(json.dumps(json_document, indent=4))

    result = glom(json_document, "**.InputColumns", )
    print("Result: " + json.dumps(result))

    spec = {
        "moons": (
            T.items(),
        Iter({T[0]: (T[1])}),
            Merge()

        )
    }


    result = glom(planets, spec)
    print(result)

    spec = "**.humans"

    result = glom(planets, spec)
    print(result)

    # app.run()