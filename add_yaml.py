import os
import re  # 忘记的模块导入
import datetime

def get_current_time():
    # 获取脚本运行的当前时间
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M')

def replace_front_matter(content, front_matter):
    """
    替换现有的 YAML front matter。如果没有找到现有的 front matter，则直接添加新的。
    """
    # 正则表达式匹配 YAML front matter，要求它以 '---' 开头和结尾
    pattern = r'^---\s*.*?---\s*'  # 匹配 YAML front matter 块
    if re.match(pattern, content, re.DOTALL):
        # 替换现有的 front matter
        content = re.sub(pattern, front_matter, content, count=1, flags=re.DOTALL)
    else:
        # 如果没有找到 YAML front matter，则直接在开头插入
        content = front_matter + content
    return content

def add_or_replace_front_matter(directory):
    for root, _, files in os.walk(directory):
        print(f"Scanning directory: {root}")
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                print(f"Found markdown file: {file_path}")

                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()

                    # 获取文件名和当前时间
                    title = os.path.splitext(file)[0]
                    date = get_current_time()  # 使用脚本运行时的当前时间
                    tags = os.path.basename(root)

                    # 获取相对路径并去除 '_posts'
                    relative_path = os.path.relpath(root, directory)
                    categories = relative_path.split(os.sep)
                    if '_posts' in categories:
                        categories.remove('_posts')  # 移除 `_posts` 目录

                    # 生成新的 front matter
                    front_matter = f'''---
title: {title}
date: {date}
tags: 
  - {tags}
categories:
  - [{', '.join(categories)}]
---

'''

                    # 替换文件中的 front matter
                    new_content = replace_front_matter(content, front_matter)

                    # 将替换后的内容写回文件
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)

                    print(f"Updated: {file_path}")
                except Exception as e:
                    print(f"Error updating {file_path}: {e}")

if __name__ == "__main__":
    # 自动获取当前脚本所在的目录
    directory = os.path.dirname(os.path.abspath(__file__))
    print(f"Starting to update markdown files in: {directory}")
    add_or_replace_front_matter(directory)
    print("Finished updating markdown files.")
