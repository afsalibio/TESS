class Student:
    """docstring for Student"""
    def __init__(self):
        super().__init__()

        self.firstname = ""
        self.lastname = ""
        self.school = ""
        self.instructor = ""
        self.instructorID = ""
        self.result = []

    def set_student_info(self, f, l, s, i, id):

        self.firstname = f.title()
        self.lastname = l.title()
        self.school = s.title()
        self.instructor = i.title()
        self.instructorID = id.title()

        return

    def set_result(self, res):
        self.result = res
        return

    def get_firstname(self):
        return self.firstname

    def get_lastname(self):
        return self.lastname

    def get_school(self):
        return self.school

    def get_result(self):
        return self.result 
    
    def get_instructor(self):
        return self.instructor 
    
    def get_instructorID(self):
        return self.instructorID 