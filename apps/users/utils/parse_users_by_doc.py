import pandas as pd
import json


class UsersParser:
    def __init__(self, doc_file):
        self.doc_file = doc_file
        self.doc_format = doc_file.name.split('.')[1]

    def operation(self):
        if self.doc_format == 'xlsx':
            df = pd.read_excel(self.doc_file)
        elif self.doc_format == 'csv':
            df = pd.read_csv(self.doc_file)
        else:
            raise ValueError('Invalid doc format')
        users_parsed = json.loads(df.to_json(orient='records'))
        users_json = json.dumps(users_parsed, indent=4)
        return users_parsed


