import xlrd
import pandas as pd


def excel_open(excel_path):
    """获取相对文件夹下的表格，并打印"""
    excel_file = xlrd.open_workbook(excel_path)
    return excel_file


def excel_input_pd(excel_file, sheet_num):
    """提取数据 返回df类型"""
    sheet = excel_file.sheet_by_index(sheet_num)
    # 提取数据 到字典 构建dataFrame
    col0 = sheet.col_values(0)[1:]
    sheet1_dict = {}
    for i in range(1, sheet.ncols):
        col_label = sheet.row_values(0)[i]
        col = sheet.col_values(i)[1:]
        # 字典{考号：Series数组}
        sheet1_dict.update({col_label: col})

    pf_data = pd.DataFrame(sheet1_dict, index=col0)
    return pf_data

