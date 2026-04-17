import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, MinMaxScaler, StandardScaler

# -----------------------------
# 1. Crear el dataset
# -----------------------------
data = {
    'ID': [1, 2, 3, 4],
    'Edad': [25, 45, 30, 40],
    'Ciudad': ['Madrid', 'Sevilla', 'Madrid', 'Barcelona'],
    'Ingresos': [30000, 50000, np.nan, 40000]
}

df = pd.DataFrame(data)

print("Dataset original:\n", df)

# -----------------------------
# 2. Imputar valores nulos (media)
# -----------------------------
imputer = SimpleImputer(strategy='mean')
df['Ingresos'] = imputer.fit_transform(df[['Ingresos']])

# -----------------------------
# 3. Label Encoding
# -----------------------------
le = LabelEncoder()
df['Ciudad_Label'] = le.fit_transform(df['Ciudad'])

# -----------------------------
# 4. One Hot Encoding
# -----------------------------
df_onehot = pd.get_dummies(df, columns=['Ciudad'])

# -----------------------------
# 5. Variables Dummy (es lo mismo que OneHot)
# -----------------------------
df_dummy = pd.get_dummies(df['Ciudad'], prefix='Ciudad')

# -----------------------------
# 6. Escalamiento
# -----------------------------

# Min-Max
scaler_minmax = MinMaxScaler()
df_onehot[['Edad_MinMax', 'Ingresos_MinMax']] = scaler_minmax.fit_transform(
    df_onehot[['Edad', 'Ingresos']]
)

# Z-Score
scaler_std = StandardScaler()
df_onehot[['Edad_Z', 'Ingresos_Z']] = scaler_std.fit_transform(
    df_onehot[['Edad', 'Ingresos']]
)

print("\nDataset final:\n", df_onehot)

# Guardar archivo
df_onehot.to_csv("datos_procesados.csv", index=False)