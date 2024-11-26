import re

# 打开并读取 JSON 文件内容
with open('Task2TrainingSet.json', 'r', encoding='utf-8') as file:
    content = file.read()

# 替换 '约:'、'大约：' 和 '的：' 为 ':'
content = re.sub(r'约：', ':', content)
content = re.sub(r'大约：', ':', content)
content = re.sub(r'的:', ':', content)
content = re.sub(r'大：', ':', content)
content = re.sub(r'约:', ':', content)
content = re.sub(r'大约:', ':', content)
content = re.sub(r'的:', ':', content)
content = re.sub(r'大:', ':', content)
content = re.sub(r'约量', '约', content)
content = re.sub(r'约大约', '大约', content)
content = re.sub(r'约为量', '约', content)

# 将修改后的内容写回 JSON 文件
with open('Task2TrainingSet.json', 'w', encoding='utf-8') as file:
    file.write(content)

print("替换完成！")