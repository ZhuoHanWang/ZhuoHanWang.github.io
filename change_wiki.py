import os
import re

def convert_wiki_image_links(file_path):
    """
    读取 Markdown 文件，找到 Obsidian 图片链接 ![[...]] 并将其转换为标准 Markdown 图片格式。
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # 匹配 Obsidian 图片链接，保持图片的扩展名，如 .png, .jpg, .jpeg, .gif
    image_pattern = r'!\[\[(.*?\.(png|jpg|jpeg|gif))\]\]'
    new_content = re.sub(image_pattern, r'![\1](\1)', content)

    # 如果内容有变化，则写回文件
    if new_content != content:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Converted image links in: {file_path}")
    else:
        print(f"No image links found in: {file_path}")

def scan_directory_for_md_files(directory):
    """
    扫描给定目录下的所有 .md 文件，并转换其中的图片链接。
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                convert_wiki_image_links(file_path)

if __name__ == "__main__":
    # 当前目录为脚本所在目录
    root_directory = os.getcwd()  # 获取当前工作目录

    # 扫描根目录并转换图片链接为标准 Markdown 格式
    scan_directory_for_md_files(root_directory)
