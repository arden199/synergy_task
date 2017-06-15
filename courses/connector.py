from django.db import connection
from .manager import UserManager, CourseManager

User = UserManager('user')
Course = CourseManager('course')
