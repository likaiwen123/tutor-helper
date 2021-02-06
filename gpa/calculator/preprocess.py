import pandas as pd
import os
import glob

class Preprocessor:
    def __init__(self, path, output_path=None):
        if os.path.isdir(path):
            data_files = glob.glob(os.path.join(path, '*'))
            self.data_files = [f for f in data_files if f[-4:] == ".xls"]
        elif os.path.isfile(path) and path[-4:] == ".xls":
            self.data_files = [path]
        else:
            raise TypeError("Path {} should be a valid xls file or directory.".format(path))

        if output_path is None:
            if os.path.isfile(path):
                self.output_path = os.path.dirname(path)
            else:
                self.output_path = path
        else:
            self.output_path = output_path

    def preprocess(self):
        for fname in self.data_files:
            df = pd.read_excel(fname)
            if df["特殊课程标记"].isnull().any():
                df["特殊课程标记"] = df["特殊课程标记.1"]
                df.drop(columns=["特殊课程标记.1"])
            elif "特殊课程标记.1" in df and df["特殊课程标记.1"].isnull().any():
                df.drop(columns=["特殊课程标记.1"])
            output_fname = os.path.join(self.output_path, fname[:-4] + ".xlsx")
            df.to_excel(output_fname, index=None)
        return self.output_path
