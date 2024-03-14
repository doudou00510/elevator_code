# -*- codings:utf-8 -*-

notes="""

以下命令是查看 student_data.db 中的 所有表的名字

Python 3.9.12 (main, Apr  5 2022, 06:56:58) 
[GCC 7.5.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import sqlite3
>>> import sqlite3 as sql3
>>> conn=sql3.connect("student_data.db")
>>> cur=conn.cursor()
>>> cur.execute(f"select name from sqlite_master where type='table'")
<sqlite3.Cursor object at 0x7f89dbeadf80>
>>> tables=cur.fetchall()
>>> for table in tables:print(table[0])
... 
_stu_info_old_20221108
sqlite_sequence
course_info
course_teacher
teacher_info
class_info
_stu_info_old_20221108_1
_score_info_old_20221108
score_info
_stu_info_old_20221109
stu_info


======================>
>>> cur.execute("PRAGMA table_info(score_info);")
<sqlite3.Cursor object at 0x7f89dbeadf80>
>>> columns=cur.fetchall()
>>> for column in columns:print(column)
... 
(0, 'sc_id', 'INTEGER', 0, None, 1)
(1, 'score', 'INT', 0, '0', 0)
(2, 'create_time', 'TEXT', 0, None, 0)
(3, 'take_second', 'INT', 0, None, 0)
(4, 'stu_id', 'INTEGER', 1, None, 0)
(5, 'course_id', 'INTEGER', 0, None, 0)
(6, 'question_num', 'INTEGER', 0, None, 0)


>>> cur.execute("select * from score_info ")
<sqlite3.Cursor object at 0x7f89dbeadf80>
>>> data=cur.fetchall()
>>> for line in data:
...     print(line)
...
(1, 10, '2022/11/08 23:08:05', 10, 287, 1, 10)
(2, 15, '2022/11/08 23:08:05', 7, 288, 1, 20)
(3, 35, '2022/11/08 23:08:05', 12, 289, 1, 100)
(6, 20, '2022/11/08 22:23:10', 85, 287, 1, 20)
(7, 10, '2022/11/08 23:08:05', 53, 287, 1, 10)
(8, 10, '2022/11/09 03:38:11', 75, 287, 1, 10)
(9, 1, '2022/11/09 03:39:34', 5, 287, 1, 1)
(10, 0, '2022/11/09 03:39:58', 5, 287, 1, 1)
(11, 5, '2022/11/09 03:42:29', 59, 287, 1, 5)
(12, 5, '2022/11/09 03:49:13', 29, 287, 1, 5)
(13, 5, '2022/11/09 03:50:45', 13, 287, 1, 5)
(14, 5, '2022/11/09 03:51:29', 15, 287, 1, 5)
(15, 5, '2022/11/09 03:52:17', 13, 287, 1, 5)
(16, 5, '2022/11/09 03:53:05', 16, 287, 1, 5)
>>> cur.execute("ALTER TABLE score_info ADD COLUMN index_list TEXT";)
  File "<stdin>", line 1
    cur.execute("ALTER TABLE score_info ADD COLUMN index_list TEXT";)
                                                                   ^
SyntaxError: invalid syntax
>>> cur.execute("ALTER TABLE score_info ADD COLUMN index_list TEXT;")
<sqlite3.Cursor object at 0x7f89dbeadf80>
>>> cur.execute(f"UPDATE score_info set index_list={[*range(100)]}")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
sqlite3.OperationalError: no such column: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99
>>> cur.commit()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'sqlite3.Cursor' object has no attribute 'commit'
>>> sql.commit()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'sql' is not defined
>>> sql3.commit()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: module 'sqlite3' has no attribute 'commit'
>>> conn.commit()
>>> cur.execute(f"UPDATE score_info set index_list={[*range(100)]}")
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
sqlite3.OperationalError: no such column: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99
>>> cur.execute(f"UPDATE score_info set index_list='{[*range(100)]}'")
<sqlite3.Cursor object at 0x7f89dbeadf80>
>>> conn.commit()
>>> cur.close()
>>> conn.close()

"""
