import matplotlib.pyplot as plt
import excel_open
import matplotlib as mpl
import numpy as np
# 设定字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 这个比较困难，涉及到多次考试，留在最后
# 以第一次为基准，得考虑第二次找不到的情况，会出现错误


def get_dict(excel_file, classroom, course0, course1):
    """制图：学生进步情况,course1, course2 由界面勾选，目前由程序直接输入"""
    # 完整表
    df_data0 = excel_open.excel_input_pd(excel_file, 0)
    df_data1 = excel_open.excel_input_pd(excel_file, 1)

    # 筛选第一次 科目年级完整总表，第二次科目完整总表
    course_choose_all0 = df_data0[~df_data0[course0].isin([''])]
    course_choose_all1 = df_data1[~df_data1[course1].isin([''])]
    # 筛选出仅仅单个科目表
    course_choose0 = course_choose_all0[course0]
    course_choose1 = course_choose_all1[course1]
    # 对这一列进行全年级排名
    course_choose_rank0 = course_choose0.rank()
    course_choose_rank1 = course_choose1.rank()
    # 筛选出某个班级，循环结构获得本班的各个同学的索引
    class_choose0 = course_choose_all0[course_choose_all0['班级'] == classroom]
    class_choose1 = course_choose_all1[course_choose_all1['班级'] == classroom]
    # 循环结构选出各个索引
    rank_dict = {}
    for index in class_choose0.index:
        name = df_data0.loc[index, '姓名']
        # 以防某同学上一次成绩是空的，索引不到
        rank0 = course_choose_rank0.loc[index]
        if index in course_choose_rank1.index:
            rank1 = course_choose_rank1.loc[index]
            rank_dict.update({name: rank0 - rank1})
        else:
            rank_dict.update({name: 10000})  # 代表缺失
        # 将的到的两次名词 结合姓名 包装为dict，不用zip 因为不是两个list了

    # 返回字典
    return rank_dict


def plt_rank(excel_file, classroom, course0, course1):
    """通过得到的字典来画图, 字典中的到名字和排名进步情况"""
    data_dict = get_dict(excel_file, classroom, course0, course1)
    # 按照降序排序
    data_dict_sort = dict(sorted(data_dict.items(), key=lambda data_dict: data_dict[1], reverse=True))
    #print(data_dict_sort)
    # sorted_x = sorted(x.iteritems(), key=lambda x: x[1], reverse=True)
    li_names = list(data_dict_sort.keys())
    li_ranks = list(data_dict_sort.values())

    # 设定x y的值
    x = np.arange(1, len(li_names)+1)
    y = np.array(li_ranks)
    text = '上次缺考人：\n'
    # 画图
    count = 0  # 记录rank为10000的人数。
    # 统计进步总数求和 ,求人数
    sum_good = 0
    count_good = 0
    sum_bad = 0
    count_bad = 0
    # 得先画，初始化，可能执行不到bad
    good = plt.bar(0, 0, color='g')
    bad = plt.bar(0, 0, color='r')
    for a, b in zip(x, y):
        if b == 10000:
            text += li_names[a-1]+'\n'
            count += 1
        elif (b >= 0) and (b < 10000):
            good = plt.bar(a-count, b, width=0.35, align='center', color='g', alpha=0.8)
            sum_good += b  # 求和
            count_good += 1
        else:
            bad = plt.bar(a-count, b, width=0.35, align='center', color='r', alpha=0.8)
            sum_bad += b
            count_bad += 1
    if count == 0:
        plt.xticks(x, li_names[count:], rotation=-90, fontsize=10)
        # print(x[:-count], li_names[count:]) 当count = 0 时 -0为空
    else:
        plt.xticks(x[:-count], li_names[count:], rotation=-90, fontsize=10)

    # 标题， x y 标签
    plt.xlabel('姓名')
    plt.ylabel('进步情况')
    title = str(classroom) + '班'+course0+'学科进步一览表'
    plt.title(title)
    # 坐标系的x, y轴范围,存在最大值10000，不能单纯是y最大值
    for each in li_ranks:
        if each != 10000:
            rank_max = each
            break
    rank_min = min(li_ranks)
    plt.ylim(rank_min-5, rank_max+5)
    # 显示数据标签
    i = 0
    for a, b in zip(x, y):
        if (b > 0) and (b < 10000):
            plt.text(a-count, b, '%d' % y[i], ha='center', va='bottom', fontsize=10, color='black')
        else:
            plt.text(a-count, b, '%d' % y[i], ha='center', va='top', fontsize=10, color='black')
        i = i + 1
    # 显示缺考人
    if text != '上次缺考人：\n':
        plt.text(1, rank_min, text, alpha=0.6)
    # 显示图例
    if count_good == 0:
        count_good = 1
    if count_bad == 0:
        count_bad = 1
    average_good = int(sum_good/count_good)
    average_bad = int(sum_bad/count_bad)
    plt.legend((good, bad), ("平均进步名次：" + str(average_good), "平均退步名次："+str(average_bad)))
    plt.hlines(0, 1, count_bad+count_good, colors="black", linestyles="-", linewidth=0.5)
    plt.show()


# print(get_dict(excel_file, 14,'语文','语文'))
# plt_rank(excel_file, 14, '语文', '语文')




