from django.db import connection
from django.http import Http404


class UserManager:

    def __init__(self, table_name):
        with connection.cursor() as cursor:
            self.table_name = table_name
            cursor.execute("Describe {}".format(self.table_name))
            self.fields = tuple(column[0] for column in cursor.fetchall())

    def all(self):
        with connection.cursor() as cursor:
            cursor.execute('CALL userGetAllRecords()')
            elements = self._to_dict(cursor.fetchall())
        return elements

    def get(self, field, value):
        with connection.cursor() as cursor:
            if field == 'id':
                cursor.execute('CALL userGetRecordById({})'.format(value))
            elif field == 'email':
                cursor.execute('CALL userGetRecordByEmail(\"{}\")'.format(value))
            else:
                raise Http404('No such field')
            element = cursor.fetchone()
            if element is None:
                return element
            element = dict(zip(self.fields, element))
        return element

    def filter(self, search):
        with connection.cursor() as cursor:
            search = "'" + search + "%'"
            cursor.execute('CALL userFilterRecord({})'.format(search))
            elements = cursor.fetchall()
            elements = self._to_dict(elements)
        return elements

    def create(self, **kwargs):
        for key in kwargs.keys():
            if kwargs[key] is None:
                kwargs[key] = ''
        with connection.cursor() as cursor:
            field_set = set(self.fields)
            create_fields = self.fields[1:]
            keys = set(kwargs.keys())
            if not keys.issubset(field_set):
                return
            values = ["'" + str(kwargs.get(field, '')) + "'" for field in create_fields]
            values = ','.join(values)
            cursor.execute('CALL userCreateRecord ({})'.format(values))

    def update(self, **kwargs):
        for key in kwargs.keys():
            if kwargs[key] is None:
                kwargs[key] = ''
        with connection.cursor() as cursor:
            field_set = set(self.fields)
            keys = set(kwargs.keys())
            if not keys.issubset(field_set):
                return
            values = ["'" + str(kwargs.get(field, '')) + "'" for field in self.fields ]
            values = ','.join(values)
            cursor.execute('CALL userUpdateRecord ({})'.format(values))

    def delete(self, pk):
        with connection.cursor() as cursor:
            cursor.execute('CALL userDeleteRecordById({})'.format(pk))

    def add_courses(self, user_id, courses_codes):
        with connection.cursor() as cursor:
            cursor.execute('CALL userGetCourses({})'.format(user_id))
            user_courses_codes = set(course[0] for course in cursor.fetchall())
            add_courses_codes = set(courses_codes)
            to_add = add_courses_codes - user_courses_codes
            to_remove = user_courses_codes - add_courses_codes
            self._remove_courses(user_id, to_remove)
            for course_code in to_add:
                course_code = "'" + course_code + "'"
                cursor.execute(
                    "CALL createHasCourseRecord({0}, {1})".format(user_id, course_code))

    def _remove_courses(self, user_id, courses_codes):
        with connection.cursor() as cursor:
            for course_code in courses_codes:
                course_code = "'" + course_code + "'"
                cursor.execute('CALL deleteHasCourseRecord({0}, {1})'.format(user_id, course_code))

    def _to_dict(self, records):
        record_list = []
        if records:
            for record in records:
                record_dict = dict(zip(self.fields, record))
                record_list.append(record_dict)
        return record_list


class CourseManager:

    def __init__(self, table_name):
        with connection.cursor() as cursor:
            self.table_name = table_name
            cursor.execute("Describe {}".format(self.table_name))
            self.fields = tuple(column[0] for column in cursor.fetchall())

    def all(self):
        with connection.cursor() as cursor:
            cursor.execute('CALL coursesGetRecords()')
            elements = self._to_dict(cursor.fetchall())
        return elements

    def user_courses(self, user_id):
        with connection.cursor() as cursor:
            cursor.execute('CALL userGetCourses({})'.format(user_id))
            elements = self._to_dict(cursor.fetchall())
        return elements

    def free_courses(self, user_id):
        with connection.cursor() as cursor:
            cursor.execute('CALL userGetCourses({})'.format(user_id))
            user_courses = set(cursor.fetchall())
            cursor.execute('CALL coursesGetRecords()')
            all_courses = set(cursor.fetchall())
            free_courses = all_courses - user_courses
            free_courses = self._to_dict(free_courses)
        return free_courses

    def _to_dict(self, records):
        record_list = []
        if records:
            for record in records:
                record_dict = dict(zip(self.fields, record))
                record_list.append(record_dict)
        return record_list
