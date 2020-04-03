import pandas as pd

def test_auto():
    read_csv = pd.read_csv
    import metapandas.auto
    assert id(read_csv) != id(pd.read_csv)
    assert id(read_csv) == id(pd.read_csv_original)
