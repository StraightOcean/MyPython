import pickle
data = ["夏正洋", "吴伟", "吴雨珊", "刘雨桐", "黄至浩",
        "管运涵", "秦长榕", "王欣琳", "谭尧", "赵子杰",
        "赵文杰", "高阳", "高树旋", "俞旭东", "尚梓墨",
        "彭博", "戎梓坤", "徐瑞岩", "许瑞扬", "许亦凡",
        "阚远", "黄天乐", "黄茂哲", "黄浩洋", "周智宸",
        "胡文萱", "张童子昊", "孙瑞", "王欣妍", "金魏澜",
        "周颜", "汤彩云", "雷子墨", "丁瑞舟", "曹怀媛",
        "袁子凌", "王晨蹊", "王昊然", "张田羽"]
with open('../点名/bin/pkl/data.pkl', 'wb') as file:
   pickle.dump(data, file)
# 从文件读取列表
with open('../点名/bin/pkl/data.pkl', 'rb') as file:
   loaded_data = pickle.load(file)
print(loaded_data) # 输出: [1, 2, 3, 4, 5]
#
# import json
# # 定义列表
# data = [1, 2, 3, 4, 5]
# # 保存列表到文件
# with open('data.json', 'w') as file:
#    json.dump(data, file)
# # 从文件读取列表
# with open('data.json', 'r') as file:
#    loaded_data = json.load(file)
# print(loaded_data) # 输出: [1, 2, 3, 4, 5]

