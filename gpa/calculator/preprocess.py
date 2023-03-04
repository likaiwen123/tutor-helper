import pandas as pd
import os
import glob
import logging

class Preprocessor:
    def __init__(self, paths, output_path=None):
        self.data_files = []
        self.output_paths = []

        if type(paths) is not list:
            paths = [paths]

        for path in paths:
            if os.path.isdir(path):
                data_files = glob.glob(os.path.join(path, '*'))
                filtered_files = [f for f in data_files if f[-4:] == ".xls"]
                self.data_files.extend(filtered_files)
                self.output_paths.extend([path] * len(filtered_files))
            elif os.path.isfile(path) and path[-4:] == ".xls":
                self.data_files.extend([path])
                self.output_paths.extend(os.path.dirname(path))
            else:
                logging.error("Path {} to be preprocessed should be a valid xls file or directory, xlsx file may not need to be preprocessed.".format(path))

        if output_path is not None:
            self.output_paths = [output_path] * len(self.data_files)

        assert(len(self.output_paths) == len(self.data_files))

    def preprocess(self):
        outputs = []
        for idx, fname in enumerate(self.data_files):
            df = pd.read_excel(fname)
            if df["特殊课程标记"].isnull().any():
                if "特殊课程标记.1" in df:
                    df["特殊课程标记"] = df["特殊课程标记.1"]
                    df.drop(columns=["特殊课程标记.1"])
            elif "特殊课程标记.1" in df and df["特殊课程标记.1"].isnull().any():
                df.drop(columns=["特殊课程标记.1"])
            output_fname = os.path.join(self.output_paths[idx], fname[:-4] + ".xlsx")
            df.to_excel(output_fname, index=None)
            outputs.append(output_fname)
        return outputs
