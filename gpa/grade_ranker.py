from gpa.calculator.preprocess import Preprocessor
from gpa.calculator.loader import Loader
from gpa.calculator.writer import Writer
from gpa.calculator.processor import Processor, Query, Options

path = "./data.xlsx"
output_path = "./ranks.xlsx"

if __name__ == "__main__":
    data = Loader(Preprocessor(path).preprocess()).load()
    # data = Loader("../no-preprocess-path").load()
    queries = [
        Query("大学至今必修限选学分绩", Options(
            course_classes=["必修", "限选"],
            semesters=[],  # all
            only_latest=False,
            only_primary=True
        )),
        Query("大学至今全部成绩学分绩", Options(
            course_classes=[],  # all
            semesters=[],  # all
            only_latest=False,
            only_primary=True
        )),
        Query("大三上必修限选学分绩", Options(
            course_classes=["必修", "限选"],
            semesters=["2020-2021-1"],  # all
            only_latest=False,
            only_primary=True
        )),
        Query("大三上全部成绩学分绩", Options(
            course_classes=[],  # all
            semesters=["2020-2021-1"],  # all
            only_latest=False,
            only_primary=True
        )),
    ]
    # dg = Processor(data).build_df(queries)
    df, dg = Processor(data).build_df(queries, excludes=[2017000001, 2018000002])

    writer = Writer(dg, total=df)
    writer.write_to_excel(output_path)
