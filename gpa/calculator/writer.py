import pandas as pd
import os
import openpyxl

class Writer:
    def __init__(self, data_group, total=None):
        self.data_group = data_group
        self.total = total

    def write_to_excel(self, name, total_name="全部"):
        
        i = 0
        # None == ALL
        if self.total is not None:
            if not os.path.isfile(name):
                print("save in all")
                self.total.reset_index(drop=True).to_excel(name, sheet_name=total_name)
        else:
            print("save by class")
            if not os.path.isfile(name):  
                workbook = openpyxl.Workbook()
                workbook.save(name)   
            # excel exists 
            with pd.ExcelWriter(name, engine='openpyxl', mode='a') as writer:      
                for df in self.data_group:
                    df[1].reset_index(drop=True).to_excel(writer, sheet_name=df[0])
