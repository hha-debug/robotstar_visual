import os

# 检查目录内容
directory = 'E:/vscode/opencv/'
if os.path.exists(directory):
    print("目录中的文件:")
    for file in os.listdir(directory):
        if file.endswith(('.jpg', '.jpeg', '.png', '.bmp')):
            print(f"  - {file}")
else:
    print("目录不存在")