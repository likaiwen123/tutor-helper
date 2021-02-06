import pandas as pd
import os


class Writer:
    def __init__(self, data_group, total=None):
        self.data_group = data_group
        self.total = total

    def write_to_excel(self, name, total_name="全部"):
        if self.total is not None:
            if not os.path.isfile(name):
                self.total.reset_index(drop=True).to_excel(name, sheet_name=total_name)
        for df in self.data_group:
            if not os.path.isfile(name):
                df[1].reset_index(drop=True).to_excel(name, sheet_name=df[0])
                continue
            with pd.ExcelWriter(name, engine='openpyxl', mode='a') as writer:
                df[1].reset_index(drop=True).to_excel(writer, sheet_name=df[0])
