import matplotlib.pyplot as plt
import matplotlib as mpl
import excel_open
import numpy as np
# 设定字体
mpl.rcParams['font.sans-serif']=['SimHei']


def get_courses_proportion(excel_file, classroom, name):
    """打印出各班级学生的个人综合实力水平雷达图"""
    df_data = excel_open.excel_input_pd(excel_file, 0)
    # 从dataframe中筛选内容
    classroom_choose = df_data[df_data['班级'] == classroom]
    st_choose = classroom_choose[classroom_choose['姓名'] == name]

    courses = []
    proportion = []
    # 单个学生第三个取起，判断不空在全校排名。
    for col in st_choose.columns[2:-1]:
        # 得到的values是 ndarray object 无法判断是浮点还是空串，所以 转为list
        score_li = st_choose[col].values.tolist()
        score = score_li[0]

        # 不是字符串，应该的到本人在所有人中的排名百分比，并写入到列表
        if not isinstance(score, str):
            # 科目列表， 比例列表
            courses.append(col)
            df_data_copy = df_data.copy()
            df_data_copy_del = df_data_copy[~df_data_copy[col].isin([''])]
            # 取出删除后目前需要比较的成绩，只有一列，不这样会导致其他大面积其他
            course_col = df_data_copy_del[col]
            course_col_rank = course_col.rank()
            # 排名
            rank = course_col_rank.loc[st_choose.index].values
            # 计算排名在总排名的比例从而取得 雷达图中的统一性,越高越好
            proportion.append(int((rank/df_data_copy_del.iloc[:,0].size)*100))

    # 合并 列标题与对于排名百分比为字典
    course_proportion_zip = dict(zip(courses, proportion))
    return course_proportion_zip


def plt_radar(excel_file, classroom, name):
    """利用上面得到的字典来画图"""
    # 通过主模块的调用传入参数给get_courses_proportion得到字典数据
    data_dict = get_courses_proportion(excel_file, classroom, name)
    # 从字典得到列表
    proportion = list(data_dict.values())
    courses = list(data_dict.keys())
    # 画雷达图
    labels = np.array(courses)  # 标签
    data_len = len(courses)  # 数据长度
    data_radar = np.array(proportion)  # 数据

    angles = np.linspace(0, 2 * np.pi, data_len, endpoint=False)  # 分割圆周长
    data_radar = np.concatenate((data_radar, [data_radar[0]]))  # 闭合
    angles = np.concatenate((angles, [angles[0]]))  # 闭合
    plt.polar(angles, data_radar, 'bo-', linewidth=1)  # 做极坐标系
    plt.thetagrids(angles * 180 / np.pi, labels, fontsize=14)  # 做标签
    plt.fill(angles, data_radar, facecolor='r', alpha=0.25)  # 填充
    plt.ylim(0, 100)
    title = str(classroom)+'班【'+name+'】同学战斗力分析图'
    plt.title(title, fontsize=20)
    #plt.style.use('ggplot')

    plt.show()
    # print(proportion)

















