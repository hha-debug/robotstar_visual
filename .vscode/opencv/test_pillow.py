from PIL import Image
import os

print("✅ PIL导入成功！")

# 测试基本功能
try:
    # 创建一个测试图片
    img = Image.new('RGB', (100, 100), color='red')
    img.save('test_image.png')
    print("✅ 图片创建和保存成功！")
    
    # 读取图片
    img2 = Image.open('test_image.png')
    print(f"✅ 图片读取成功！尺寸: {img2.size}")
    
    # 清理测试文件
    if os.path.exists('test_image.png'):
        os.remove('test_image.png')
        print("✅ 测试文件清理完成")
        
except Exception as e:
    print(f"❌ 错误: {e}")