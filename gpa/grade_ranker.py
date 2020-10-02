from calculator.loader import Loader
from calculator.writer import Writer
from calculator.processor import Processor, Query, Options

path = "./data.xlsx"
output_path = "./ranks.xlsx"

if __name__ == "__main__":
    data = Loader(path).load()
    queries = [
        Query("两年必修限选学分绩", Options(
            course_classes=["必修", "限选"],
            semesters=[],  # all
            only_latest=True,
            only_primary=True
        )),
        Query("两年全部成绩学分绩", Options(
            course_classes=[],  # all
            semesters=[],  # all
            only_latest=True,
            only_primary=True
        )),
        Query("大二学年必修限选学分绩", Options(
            course_classes=["必修", "限选"],
            semesters=["2019-2020-1", "2019-2020-2", "2019-2020-3"],  # all
            only_latest=True,
            only_primary=True
        )),
        Query("大二学年全部成绩学分绩", Options(
            course_classes=[],  # all
            semesters=["2019-2020-1", "2019-2020-2", "2019-2020-3"],  # all
            only_latest=True,
            only_primary=True
        )),
    ]
    dg = Processor(data).build_df(queries)
    # dg = Processor(data).build_df(queries, excludes=[2017000001, 2018000002])

    writer = Writer(dg)
    writer.write_to_excel(output_path)
