import plt_courses
import plt_radar
import plt_rank
import excel_open
import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFileDialog
from inputUI import Ui_Form
import numpy as np
# 主文件，启动文件
# 获取地址 打开文件 读取数据画图

# 通过界面获取班级， 科目， 类型，通过类型调取不同的函数，班级科目作为参数完成绘图
# plt_courses.plt_course(excel_file, 9, '语文')
# plt_radar.plt_radar(excel_file, 9, '潘柯轩')
# plt_rank.plt_rank(excel_file, 9, '技赋', '技赋')


class MyForm(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.c_class = 1
        # 这个要在构造函数里说明，虽然赋值在函数里在使用之前，还是有错,因为建立监听时用到了这个变量，虽然当时不需要具体值
        self.e_file = None
        self.setupUi(self)
        self.btn_input.clicked.connect(self.input_file)
        self.btn_plot.clicked.connect(self.plt_class)
        self.btn_p_plot.clicked.connect(self.plt_person)

    def input_file(self):
        """input btn window"""
        excel_path, file_type= QFileDialog.getOpenFileName(self,'选择文件', './','excel(*.xlsx);;excel(*.xls)')
        excel_file = excel_open.excel_open(excel_path)
        self.e_file = excel_file
        # self.excel_file = excel_file
        # 当的到excel文件的时候，再获得班级
        self.get_classes(self.e_file)
        # 获得学科
        self.get_courses(self.e_file)
        # 获得姓名
        self.cb_class.currentIndexChanged.connect(self.get_names)
        # plt_radar.plt_radar(excel_file,1, '潘忠禹')
        # plt_rank.plt_rank(self.e_file, self.c_class, '语文', '语文')

    def get_classes(self, file):
        """get per class"""
        df_data = excel_open.excel_input_pd(file, 0)
        df_classes = df_data['班级']
        np_classes = np.unique(df_classes.values)
        # np.unique返回列表的班级去重，排序， 返回列表
        li_classes = list(np_classes)
        self.cb_class.addItems([str(int(item)) for item in li_classes])
        self.lineEdit_input.setStyleSheet('color:green')
        self.lineEdit_input.setText('导入成功：请选择班级')

    def get_names(self):
        """get one class st name"""
        df_data = excel_open.excel_input_pd(self.e_file, 0)
        self.c_class = int(self.cb_class.currentText())

        df_class = df_data[df_data['班级'] == int(self.c_class)]
        df_name = df_class['姓名']
        li_name = df_name.values.tolist()
        self.cb_name.clear()
        self.cb_name.addItems(li_name)
        # class_choose0 = course_choose_all0[course_choose_all0['班级'] == classroom]

    def get_courses(self, file):
        """get all courses"""
        df_data = excel_open.excel_input_pd(file, 0)
        cols_name = df_data.columns.values.tolist()[2:]
        self.cb_course.addItems(cols_name)

    def plt_class(self):
        """用来作为槽函数，画出班级相关图"""
        if self.rb_score.isChecked():
            plt_courses.plt_course(self.e_file, self.c_class, self.cb_course.currentText())
        else:
            # plt_rank.plt_rank(excel_file, 9, '技赋', '技赋')
            plt_rank.plt_rank(self.e_file, self.c_class, self.cb_course.currentText(), self.cb_course.currentText())
            # print(self.cb_course.currentText())

    def plt_person(self):
        """个人情况按钮槽函数， 打印图片"""
        plt_radar.plt_radar(self.e_file, self.c_class, self.cb_name.currentText())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myform = MyForm()
    myform.show()
    sys.exit(app.exec_())

