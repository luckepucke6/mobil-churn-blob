import sys
import pandas as pd
import pandera.pandas as pa

schema = pa.DataFrameSchema({
    "kund_id": pa.Column(int, unique=True),
    "alder": pa.Column(int, pa.Check.in_range(16,110)),
    "region": pa.Column(str),
    "abonnemang": pa.Column(str),
    "manader_som_kund": pa.Column(int),
    "manadskostnad": pa.Column(float),
    "data_gb_per_manad": pa.Column(float),
    "supportarenden_12m": pa.Column(int),
    "avslutat": pa.Column(int)
}, strict=True)

if __name__ == "__main__":
    fil = sys.argv[1]
    df = pd.read_csv(fil)
    try:
        schema.validate(df, lazy=True)
    except pa.errors.SchemaErrors as fel:
        print(fel.failure_cases)
        sys.exit(1)
    print("OK")