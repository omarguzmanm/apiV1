from surprise import Dataset, Reader, SVD
from surprise.model_selection import train_test_split
import pandas as pd
from db.db import data  

# Configura Surprise
reader = Reader(rating_scale=(0, 5))

# Crea un DataFrame de pandas con los datos
df = pd.DataFrame(data, columns=['user_id', 'tag_id', 'rating'])

# Carga datos en Surprise
data = Dataset.load_from_df(df[['user_id', 'tag_id', 'rating']], reader)
trainset, _ = train_test_split(data, test_size=0.2)
model = SVD()
model.fit(trainset)
