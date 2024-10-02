import os
import re
import datetime
from collections import defaultdict

def get_current_time():
    now = datetime.datetime.now()
    return now.strftime('%Y-%m-%d %H:%M')

def replace_front_matter(content, front_matter, date):
    pattern = r'^---\s*.*?---\s*'
    if re.match(pattern, content, re.DOTALL):
        existing_date = re.search(r'date:\s*([^\n]+)', content)
        if existing_date:
            date = existing_date.group(1).strip()
            front_matter = front_matter.replace('<DATE_PLACEHOLDER>', date)
        content = re.sub(pattern, front_matter, content, count=1, flags=re.DOTALL)
    else:
        front_matter = front_matter.replace('<DATE_PLACEHOLDER>', date)
        content = front_matter + content
    return content

def add_or_replace_front_matter(directory, tags_data, categories_data):
    modified_files = []  # 新增：用于保存修改过的文件
    for root, _, files in os.walk(directory):
        if '_posts' in root:  # 只处理 _posts 目录下的文件
            for file in files:
                if file.endswith('.md'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()

                        title = os.path.splitext(file)[0]
                        current_time = get_current_time()
                        tags = os.path.basename(root)
                        relative_path = os.path.relpath(root, directory)
                        categories = relative_path.split(os.sep)
                        if '_posts' in categories:
                            categories.remove('_posts')

                        front_matter = f'''---
title: {title}
date: <DATE_PLACEHOLDER>
tags: 
  - {tags}
categories:
  - [{', '.join(categories)}]
---

'''
                        # 更新 tags 和 categories 数据
                        tags_data[tags].append(title)
                        categories_data[categories[0]].append(title)

                        new_content = replace_front_matter(content, front_matter, current_time)

                        if new_content != content:
                            modified_files.append(file_path)  # 如果文件被修改，添加到列表

                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(new_content)

                    except Exception as e:
                        print(f"Error updating {file_path}: {e}")
    
    return modified_files  # 返回修改过的文件列表

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    tags_data = defaultdict(list)
    categories_data = defaultdict(list)

    # 更新 front matter 并收集 tags 和 categories 信息
    modified_files = add_or_replace_front_matter(directory, tags_data, categories_data)

    if modified_files:
        print("Modified files:")
        for file in modified_files:
            print(file)
    else:
        print("No files were modified.")

    print("Finished updating markdown files")
