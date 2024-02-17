import os
import re

# 进入input文件夹，如果不存在则新建一个
input_folder = 'input'
if not os.path.exists(input_folder):
    os.makedirs(input_folder)
os.chdir(input_folder)

# 获取当前目录下的所有文件
files = os.listdir()

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'output')
print(f'output_dir: {output_dir}')

# 筛选出所有的markdown文件
markdown_files = [file for file in files if file.endswith('.md')]

# 对每个markdown文件进行处理
for file in markdown_files:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 使用正则表达式按照“---”进行切片
    slices = re.split(r'---', content)
    
    # 创建一个与markdown文件同名的文件夹
    file_name = file.rsplit('.', 1)[0]
    if not os.path.exists(os.path.join(output_dir, file_name)):
        os.makedirs(os.path.join(output_dir, file_name))
    
    # 对每个切片进行处理，保留所有的上级标题
    title = []
    for i, slice in enumerate(slices):
        lines = slice.split('\n')
        content = []
        if len(lines) == 0 or (len(lines) == 1 and lines[0].lstrip(' ') == ''):
            continue
        for line in lines:
            if line == '':
                continue
            if line[0] == '#':
                # 认为是标题
                line = re.sub(r'\d+\.', '', line)
                line = re.sub(r'[一二三四五六七八九十]+、', '', line)
                title_level = len(line) - len(line.lstrip('#'))
                while len(title) > 0 and title[-1]['level'] >= title_level:
                    title.pop()
                title.append({
                    'level': title_level,
                    'name': line.lstrip('#').strip()
                })
            else:
                content.append(line)
        
        # 将title和content的内容存入新创建的文件夹中
        file_to_save = os.path.join(output_dir, file_name, f"{file_name}_{i}.md")
        with open(file_to_save, 'w', encoding="utf-8") as f:
            for t in title:
                f.write("#" * t['level'] + f" {t['name']}\n")
            for c in content:
                f.write(f"{c}\n")