

class Course:
    def __init__(self, number, name, credit):
        """
        number: the unique number of the course.
        name: the name of the course.
        credit: the credit of the course.
        semester:
        """
        self.number = number
        self.name = name
        self.credit = credit


class Student:
    def __init__(self, id, name, class_name):
        """
        id: the student ID
        name: the name of the student
        class_name: the class name.
        """
        self.id = id
        self.name = name
        self.class_name = class_name

        # temporary member
        self.course_index_list = []


class Grade:
    def __init__(self, student_id, course_number, grade, grade_mark, semester, course_class, course_type="ordinary", re_enter=False):
        self.student_id = student_id
        self.course_number = course_number
        self.course_class = course_class
        self.course_type = course_type
        self.course_semester = semester
        self.re_enter = re_enter
        self.grade = grade
        self.grade_mark = grade_mark
