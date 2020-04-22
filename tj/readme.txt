python 数据区间统计

函数接口
#data 数组
# total_sec_num 欲分几段
#v_step  切分单位，越小越精细。
#主要算法。通过一个个v_step长度的个数统计，汇总到total_sec_num段（total_sec_num总数占比是100，一般）
def get_section(data,total_sec_num, v_step = 0.005):
