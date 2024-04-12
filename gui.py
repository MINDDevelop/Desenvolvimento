import Functions as tt
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    r'C:\Users\vgonçalves\Downloads\IBOVDia_03-04-24.csv',
    encoding='latin1',
    sep=';',
    header=None
)
Ibov=df[0].unique().tolist()
df2= tt.DR_acoes()
df2=df2.query(f"symbol in{Ibov}")
Altas=df2.head(5)
Baixas=df2.tail(5)
print(Altas)
print(Baixas)
