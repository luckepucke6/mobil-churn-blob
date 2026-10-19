import sys
import pandas as pd
import pandera.pandas as pa

schema = pa.DataFrameSchema({
    "kund_id": pa.Column(int, unique=True),
    "alder": pa.Column(int, pa.Check.in_range(16,110)),
    "region": pa.Column(str, pa.Check.isin(["Mitt", "Syd", "Norr", "Stockholm", "Väst"])),
    "abonnemang": pa.Column(str, pa.Check.isin(["Bas", "Standard", "Premium"])),
    "manader_som_kund": pa.Column(int, pa.Check.in_range(0, 1000)),
    "manadskostnad": pa.Column(float, pa.Check.in_range(0, 2000)),
    "data_gb_per_manad": pa.Column(float, pa.Check.in_range(0, 1000)),
    "supportarenden_12m": pa.Column(int,  pa.Check.in_range(0, 365)),
    "avslutat": pa.Column(int, pa.Check.isin([1, 0]))
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