from io import BytesIO
import pandas as pd
import numpy as np


def export_excel(file_name, sheet_name, json_file):
    byte_buffer = BytesIO()
    df = pd.read_json(json_file)
    writer = pd.ExcelWriter(byte_buffer, engine='xlsxwriter')
    df.index = np.arange(1, len(df) + 1)
    df.to_excel(writer, sheet_name=sheet_name, index=True)
    writer.close()
    return byte_buffer, file_name
