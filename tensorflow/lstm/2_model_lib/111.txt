一、目标意义
本案例测试lstm 股票分类问题
预测股票5天后 上涨情况，具体根据上涨幅度划分为5个区间，从而构成lstm分类问题

为避免样本不均衡，首先用get_hihg_low_section.py统计
get_hihg_low_section.py 函数统计出股票的上涨分布空间，注意该算法是均匀的。避免样本分布不均衡导致训练失败


最终结果，基本是20%-50%，没有实际买卖价值，但说明是随机的。模型虽然预测不准，但该lstm结构用来学习或者其他项目参照很好


二、总体过程
1、首先对原有csv数据做转换
  原有数据，close是有前复权的。所有根据他计算其他所有前复权 。同时计算bias atr  60（20）日K线 斜率和方差
  用n_conver.py脚本

2、 统计股票label分布特征
    避免样本分布不均衡导致训练失败 。本测试用5个区间，对应5个分类。
    用 get_hihg_low_section.py 对样本数据统计，能很好的确定5个空间每个的起始、结束位置
    产出文件high_low_section.json
    
3、    组织数据
tf_data_factroy2.py   组织数据，用get_hihg_low_section获得的high_low_section.json 找到上涨所在的区间，从而确定分类。比如[1,0,0,0,0] 表示在第一个区间

一次喂batch_size个，然后参数每次更新一遍
此部分未来可考虑用 tf.data.Dataset 来组织。参考sin2.py

split.py分割训练和测试集合



输入特征：
open	high	low	close	change	volume	money	turnover	linear_k60	linear_k60_loss	linear_k20	linear_k20_loss	bias	atr

label 
label_1	label_2 具体需要转换tf_data_factroy2.py转换

