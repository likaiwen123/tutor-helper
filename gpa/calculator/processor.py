import pandas as pd


class Options:
    def __init__(self, course_classes, semesters, only_primary=True, only_latest=True):
        self.course_classes = set()
        for cls in course_classes:
            self.course_classes.add(cls)
        self.semesters = set()
        for sem in semesters:
            self.semesters.add(sem)
        self.only_primary = only_primary
        self.only_latest = only_latest


class Query:
    def __init__(self, name, options):
        self.name = name
        self.options = options


class Processor:
    def __init__(self, storage):
        self.storage = storage

    def calc_gpa(self, student_id, options):
        total_credits = 0
        total_marks = 0.0
        course_set = set()
        for grade_idx in self.storage.students[student_id].course_index_list:
            grade = self.storage.grades[grade_idx]
            course_number = grade.course_number
            credit = self.storage.courses[course_number].credit
            if grade.grade < 0:
                continue
            if options.only_primary and grade.course_type != "一学位":
                continue
            if options.only_latest and grade.course_number in course_set:
                # all grades before will be zero.
                total_marks += grade.grade * credit
                continue
            if len(options.course_classes) > 0 and grade.course_class not in options.course_classes:
                continue
            if len(options.semesters) > 0 and grade.course_semester not in options.semesters:
                continue
            total_credits += credit
            total_marks += grade.grade * credit
            course_set.add(course_number)
        if total_credits == 0:
            return 0.0
        return total_marks / total_credits

    def __build_single_df(self, name, options, excludes=None):
        # TODO: avoid duplicate creation of dataframe.
        df = pd.DataFrame()
        df['学号'] = list(self.storage.students.keys())
        df['班级'] = df.apply(func=lambda row: self.storage.students[row['学号']].class_name, axis=1)
        df.drop(df[df['学号'].map(lambda x: x in excludes)].index, inplace=True)

        df[name] = df.apply(func=lambda row: self.calc_gpa(row['学号'], options), axis=1)
        df[name + "排名"] = df[name].rank(method='min', ascending=False).astype(int)
        df[name + "班级排名"] = df.groupby('班级')[name + "排名"].rank(method='min').astype(int)
        return df

    def build_df(self, queries, excludes=None):
        if excludes is None:
            excludes = set()
        else:
            excludes = set(excludes)
        df = pd.DataFrame()
        df['学号'] = list(self.storage.students.keys())
        df['姓名'] = df.apply(func=lambda row: self.storage.students[row['学号']].name, axis=1)
        df['班级'] = df.apply(func=lambda row: self.storage.students[row['学号']].class_name, axis=1)

        for query in queries:
            sdf = self.__build_single_df(query.name, query.options, excludes)
            df = df.merge(sdf)

        return df, df.groupby(by='班级')
