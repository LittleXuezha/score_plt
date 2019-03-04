import matplotlib.pyplot as plt
import excel_open
import matplotlib as mpl
# 设定字体
mpl.rcParams['font.sans-serif']=['SimHei']


def plt_course(excel_file, classroom, course):
    pf_data = excel_open.excel_input_pd(excel_file, 0)

    # 从dataframe中筛选内容
    classroom_choose = pf_data[pf_data['班级'] == classroom].sort_values(by=course, ascending=False)
    course_choose = classroom_choose[course]
    st_name = classroom_choose['姓名']

    # 设定x的值
    x = range(1, course_choose.size+1)
    y = course_choose

    # 显示柱形图, x轴坐标轴,
    plt.bar(x, y, width=0.35, align='center', color='r', alpha=0.8)
    plt.xticks(x, st_name, rotation=-90, fontsize=10)
    # 标题， x y 标签
    title = str(classroom) + '班' + course + '成绩柱形图'
    plt.title(title)
    plt.ylabel('分数')
    plt.xlabel('姓名')
    # 限制表格显示范围
    course_min = course_choose.min()
    course_max = course_choose.max()
    plt.ylim(course_min-1, course_max+1)
    # 显示标签
    i = 0
    count_sum = 0
    for a, b in zip(x, y):
        p = plt.text(a, b, '%d' % y[i], ha='center', va='bottom', fontsize=10)
        i = i+1
        count_sum += b
    average = count_sum/i
    # 图例 和平均分
    plt.text(course_choose.size-10, course_max+2, '平均分：%.2f' % average)
    plt.legend(labels=course)
    plt.show()



