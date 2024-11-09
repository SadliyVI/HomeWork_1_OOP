# Homework OOPs


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        return (f'Имя: {self.name}\nФамилия: {self.surname}\n'
                f'Средняя оценка за домашнее задание: '
                f'{self.get_average_hw_grade()}\n'
                f'Курсы в процессе изучения: {self.get_courses_in_progress()}\n'
                f'Завершенные курсы: {self.get_finished_courses()}')

    def __eq__(self, other):
        return self.get_average_hw_grade() == other.get_average_hw_grade()

    def get_finished_courses(self):
        courses_list = ''
        for course in self.finished_courses:
            courses_list += course + ', '
        return courses_list

    def get_courses_in_progress(self):
        courses_list = ''
        for course in self.courses_in_progress:
            courses_list += course + ', '
        return courses_list

    def get_average_hw_grade(self):
        average_grade = 0
        course_av_grade = 0
        counter = 0
        if self.grades:
            for grades in self.grades.values():
                course_av_grade += sum(grades) / len(grades)
                counter +=1
            average_grade = course_av_grade / counter
        return round(average_grade, 1)

    def let_grade_lecturer(self, lecturer, course, grade):
        if (isinstance(lecturer, Lecturer) and course in self.finished_courses
                and course in lecturer.courses_attached):
            if course in lecturer.grades_from_students:
                lecturer.grades_from_students[course] += [grade]
            else:
                lecturer.grades_from_students[course] = [grade]
        else:
            return 'Ошибка! Проверьте данные!'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []
        self.grades_from_students = {}

    def get_average_grade(self):
        if self.grades_from_students:
            average_grade = 0
            course_av_grade = 0
            counter = 0
            if self.grades_from_students:
                for grades in self.grades_from_students.values():
                    course_av_grade += sum(grades) / len(grades)
                    counter += 1
                average_grade = course_av_grade / counter
            return round(average_grade, 1)

    def __str__(self):
        return (f'Имя: {self.name}\nФамилия: {self.surname}\n'
                f'Средняя оценка за лекции: {self.get_average_grade()}')

    def __eq__(self, other):
        if self.get_average_grade() > other.get_average_grade():
            return 'Лучше'
        elif self.get_average_grade() < other.get_average_grade():
            return 'Хуже'
        else:
            return 'Равны'


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = []

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'

    def rate_hw(self, student, course, grade):
        if (isinstance(student, Student) and course in self.courses_attached
                and course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

# Example usage

# Work with Class Student

student_1 = Student('Иван', 'Иванов', 'мужской')
student_2 = Student( 'Елена', 'Петрова', 'женский')
student_1.courses_in_progress += ['Python']
student_2.courses_in_progress += ['Git']
student_1.finished_courses += ['Java', 'CSS']
student_2.finished_courses += ['C++', 'C#']

student_1.grades = {'Java': [10, 8, 9], 'CSS': [8,8,8]}
student_2.grades = {'C++': [10, 10, 9], 'C#': [9,8,10]}

print(student_1, '\n')
print(student_2, '\n')
print(f'Студенты равны? {student_1 == student_2}\n')

# Work with Class Lecturer

lecturer_1 = Lecturer('Андрей', 'Петров')
lecturer_2 = Lecturer('Евгений', 'Смирнов')
lecturer_1.courses_attached += ['Python','C++', 'Java']
lecturer_2.courses_attached += ['Git', 'C#', 'CSS']
lecturer_1.grades_from_students = {'Python': [10, 9, 8, 10, 10],
                                   'C++': [9, 8, 9, 10, 10],
                                   'Java': [8, 10, 9, 8, 9]}
lecturer_2.grades_from_students = {'Git': [10, 10, 9, 10, 9],
                                   'C#': [10, 8, 10, 10, 10],
                                   'CSS': [10, 8, 8, 10, 10]}

student_1.let_grade_lecturer(lecturer_1, 'Python', 9)
# поставить оценку нельзя так как курс еще не закончился
student_1.let_grade_lecturer(lecturer_1,'Java', 10)
# поставить оценку нельзя так как курс еще не закончился
student_1.let_grade_lecturer(lecturer_2, 'Git', 9)
student_2.let_grade_lecturer(lecturer_2, 'C#', 10)

print(lecturer_1, '\n')
print(lecturer_2, '\n')
print(f'По мнению студентов преподаватель {lecturer_1.name[0]}'
      f'.{lecturer_1.surname} лучше преподавателя {lecturer_2.name[0]}'
      f'.{lecturer_2.surname}? {lecturer_1.__eq__(lecturer_2)}\n')

# Work with class Reviewer

student_list = [student_1, student_2]

reviewer_1 = Reviewer('Петр', 'Сидоров')
reviewer_2 = Reviewer('Екатерина', 'Безымянная')
reviewer_1.courses_attached = ['Java','CSS', 'Git']
reviewer_2.courses_attached = ['C++','C#', 'Python']

print(reviewer_1, '\n')
print(reviewer_2, '\n')

reviewer_2.rate_hw(student_1,'Python', 8)
reviewer_1.rate_hw(student_2, 'Git', 8)
reviewer_2.rate_hw(student_1,'Python', 10)
reviewer_1.rate_hw(student_2,'Git', 7 )

print(student_1, '\n')
print(student_2, '\n')
print(f'Студенты равны? {student_1 == student_2}\n')

def get_best_student_on_course(student_list):
    best_student_list = []
    i = 0
    max_grade =  max(student_list, key=lambda x: x.get_average_hw_grade())
    for student in student_list:
        if student.get_average_hw_grade() == max_grade.get_average_hw_grade():
            best_student_list.append(i)
        i += 1
    if len(best_student_list) == 1:
        student = student_list[best_student_list[0]]
        return f'Лучший студент: {student.name} {student.surname}'
    elif len(best_student_list) > 1:
        student_list_str = ', '.join(f'{student_list[i].name} '
                                     f'{student_list[i].surname}'
                                     for i in best_student_list)
        return f'Лучшие студенты: {student_list_str}'

print(get_best_student_on_course(student_list))

student_3 = Student('Николай', 'Семенов', 'мужской')
student_4 = Student( 'Полина', 'Гагарина', 'женский')
student_3.courses_in_progress.append('Python')
student_4.courses_in_progress.append('Python')
student_3.grades = {'Python': [10, 8, 9, 8, 10]}
student_4.grades = {'Python': [9, 8, 9, 10, 10]}


def get_average_all_grades(students_list, course):
    if students_list:
        consolidated_list = []
        counter = 0
        for student in students_list:
            for key, value in student.grades.items():
                if key == course:
                    consolidated_list.extend(value)
                    counter += 1
        if counter != 0:
            return (f'Средняя оценка студентов за курс {course}: '
                    f'{round(sum(consolidated_list) / 
                             len(consolidated_list), 1)}')
        else:
            return 'Курс не преподается!'
    else:
        return 'На этом курсе нет студентов или курс не преподается!'

students_list = [student_1, student_2, student_3, student_4]
print(get_average_all_grades(students_list, 'Python'))
print(get_average_all_grades(students_list, 'Java'))
print(get_average_all_grades(students_list, 'JavaScript'))
students_list = []
print(get_average_all_grades(students_list, 'Python'))

def get_average_lecturer_rating(lecturers_list, course):
    if lecturers_list:
        consolidated_grade = 0
        counter = 0
        for lecturer in lecturers_list:
            for key, value in lecturer.grades_from_students.items():
                if key == course:
                    consolidated_grade += sum(value) / len(value)
                    counter += 1
        if counter != 0:
            return (f'Средняя оценка преподавания курса {course}: '
                    f'{round((consolidated_grade / counter), 1)}')
        else:
            return 'Этот курс никем не преподается!'
    else:
        return 'Нет данных!'


lecturers_list = [lecturer_1, lecturer_2]
print('\n')
print(get_average_lecturer_rating(lecturers_list, 'Python'))
print(get_average_lecturer_rating(lecturers_list, 'Java'))
print(get_average_lecturer_rating(lecturers_list, 'CSS'))
print(get_average_lecturer_rating(lecturers_list, 'JavaScript'))
print('\n')
lecturers_list = []
print(get_average_lecturer_rating(lecturers_list, 'Python'))
