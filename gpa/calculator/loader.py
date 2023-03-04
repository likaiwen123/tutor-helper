import os
import glob
import math
from openpyxl import load_workbook
import pandas as pd
from gpa.calculator.models import Student, Course, Grade
from gpa.calculator.storage import Storage

import logging


class Loader:
    def __init__(self, paths):
        if type(paths) is not list:
            paths = [paths]
        for path in paths:
            if os.path.isdir(path):
                data_files = glob.glob(os.path.join(path, '*'))
                self.data_files = [f for f in data_files if f[-5:] == ".xlsx"]
            elif os.path.isfile(path) and path[-5:] == ".xlsx":
                self.data_files = [path]
            else:
                logging.error("Path {} should be a valid file or directory, ignored.".format(path))

        if len(self.data_files) == 0:
            logging.fatal("Path {} does not specify any valid data source file.".format(paths))
            exit(1)

        self.meta = {
            "student_id": "学号",
            "student_name": "姓名",
            "class_name": "教学班级",
            "course_number": "课程号",
            "course_name": "课程名",
            "course_grade": "绩点成绩",
            "course_grade_mark": "成绩",
            "semester": "学年学期",
            "course_credit": "学分",
            "course_class": "课程属性",
            "course_type": "特殊课程标记",
            "re-enter": "重修补考标志"
        }
        self.course_class_meta = {
            "必修": "必修",
            "限选": "限选",
            "任选": "任选",
        }
        self.course_type_meta = {
            "第一学位课程": "一学位",
            "第二学位课程": "二学位",
            "辅修专业课程": "辅修",
            "交换生课程": "交换生课程", # 成绩为EX，绩点为N/A或空，不计入成绩计算
        }
        self.re_enter_mark = "重修"

    def load(self):
        storage = Storage()
        for f in self.data_files:
            wb = load_workbook(f)
            ws_name = wb.active.title
            wb.close()
            frame = pd.read_excel(f, sheet_name=ws_name)
            for idx in range(len(frame)):
                data = frame.iloc[idx]

                student_id = data[self.meta["student_id"]]
                student_name = data[self.meta["student_name"]]
                class_name = data[self.meta["class_name"]]

                if student_id not in storage.students:
                    storage.students[student_id] = Student(student_id, student_name, class_name)

                course_number = data[self.meta["course_number"]]
                course_name = data[self.meta["course_name"]]
                course_credit = data[self.meta["course_credit"]]

                if course_number not in storage.courses:
                    storage.courses[course_number] = Course(course_number, course_name, course_credit)
                elif storage.courses[course_number].credit != course_credit:
                    raise ValueError("Different credits found for Course ID {}".format(course_number))

                course_grade_val = data[self.meta["course_grade"]]
                if course_grade_val == '*':
                    # grade has not been provided.
                    continue
                course_grade = float(course_grade_val)
                if math.isnan(course_grade):
                    course_grade = -1
                course_grade_mark = data[self.meta["course_grade_mark"]]
                semester = data[self.meta["semester"]]
                course_class = self.course_class_meta[data[self.meta["course_class"]]]
                if type(data[self.meta["course_type"]]) is str:
                    course_type = self.course_type_meta[data[self.meta["course_type"]]]
                elif math.isnan(data[self.meta["course_type"]]):
                    course_type = self.course_type_meta["第一学位课程"]
                else:
                    logging.fatal(f"特殊课程标记 \"{data[self.meta['course_type']]}\"无法识别")
                re_enter = data[self.meta["re-enter"]] == self.re_enter_mark

                grade = Grade(student_id, course_number, course_grade, course_grade_mark, semester, course_class,
                              course_type, re_enter)
                storage.students[student_id].course_index_list.append(len(storage.grades))
                storage.grades.append(grade)
        logging.info("Totally {} students found.".format(len(storage.students)))
        return storage
