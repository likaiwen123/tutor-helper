import datetime

basic_template_plain = "<name>同学：\n\n" + \
                 "    你好，下面是你至今的成绩情况，学分绩和排名为辅导员计算结果，仅供参考。参与排名的班级人数为<class number>人，年级人数为<grade number>人。\n\n" + \
                 "<GPA table>\n\n" + \
                 "<sender name>\n" + \
                 datetime.datetime.now().strftime('%Y.%m.%d')

basic_template = basic_template_plain.replace("\n", "<br />")
