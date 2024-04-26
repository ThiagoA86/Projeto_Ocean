import json
import pandas as pd # para concatenação de arquivos csv
import os

class Data:
    # Concatena dois arquivos no formato csv e salva o arquivo concatenado 
    def concatenate(file1, file2, path):
        df_1 = pd.read_csv(file1)
        df_2 = pd.read_csv(file2)

        # Concatena os dois arquivos csv
        df_final = pd.concat([df_1, df_2])

        # Salva o arquivo concatenado na pasta files
        df_final.to_csv(os.path.join(path, file1.filename), index=False)
    