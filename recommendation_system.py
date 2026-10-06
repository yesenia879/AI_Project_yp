"""Carga y preprocesamiento básico de un catálogo de productos."""

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer


# Cargar products.csv desde el directorio de trabajo. El archivo debe incluir
# las columnas product_id, name, category y description.
DATA_PATH = "products.csv"
products = pd.read_csv(DATA_PATH)

# Validar la estructura y limpiar los datos usados para recomendar productos.
required_columns = ["product_id", "name", "category", "description"]
missing_columns = [column for column in required_columns if column not in products.columns]
if missing_columns:
	raise ValueError(f"Faltan columnas requeridas: {', '.join(missing_columns)}")

products = products.drop_duplicates(subset="product_id").copy()
for column in ("name", "category", "description"):
	products[column] = products[column].fillna("").astype(str).str.strip()

# Unir los campos de texto y convertirlos en vectores TF-IDF para su uso
# posterior en un sistema de recomendación basado en contenido.
products["features"] = (
	products["name"] + " " + products["category"] + " " + products["description"]
).str.lower()
vectorizer = TfidfVectorizer()
product_vectors = vectorizer.fit_transform(products["features"])
