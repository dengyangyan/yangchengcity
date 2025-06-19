import os
import shutil
from pathlib import Path

def copy_images_from_txt(txt_file_path, source_folder, destination_folder):
    """
    从txt文件中读取图像名称，并将对应的图像从源文件夹复制到目标文件夹
    
    Args:
        txt_file_path (str): 包含图像名称的txt文件路径
        source_folder (str): 源图像文件夹路径
        destination_folder (str): 目标文件夹路径
    """
    
    # 创建目标文件夹（如果不存在）
    Path(destination_folder).mkdir(parents=True, exist_ok=True)
    
    # 支持的图像格式
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif']
    
    copied_count = 0
    not_found_count = 0
    not_found_files = []
    
    try:
        # 读取txt文件
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                # 去除行首行尾的空白字符
                image_name = line.strip()
                
                # 跳过空行
                if not image_name:
                    continue
                
                # 查找图像文件
                found = False
                
                # 如果文件名没有扩展名，尝试所有支持的格式
                if not any(image_name.lower().endswith(ext) for ext in image_extensions):
                    for ext in image_extensions:
                        source_path = os.path.join(source_folder, image_name + ext)
                        if os.path.exists(source_path):
                            destination_path = os.path.join(destination_folder, image_name + ext)
                            shutil.copy2(source_path, destination_path)
                            print(f"已复制: {image_name + ext}")
                            copied_count += 1
                            found = True
                            break
                else:
                    # 文件名已包含扩展名
                    source_path = os.path.join(source_folder, image_name)
                    if os.path.exists(source_path):
                        destination_path = os.path.join(destination_folder, image_name)
                        shutil.copy2(source_path, destination_path)
                        print(f"已复制: {image_name}")
                        copied_count += 1
                        found = True
                
                if not found:
                    print(f"未找到图像: {image_name} (第{line_num}行)")
                    not_found_count += 1
                    not_found_files.append(image_name)
    
    except FileNotFoundError:
        print(f"错误: 找不到txt文件 '{txt_file_path}'")
        return
    except Exception as e:
        print(f"错误: {str(e)}")
        return
    
    # 输出统计信息
    print(f"\n复制完成!")
    print(f"成功复制: {copied_count} 个文件")
    print(f"未找到: {not_found_count} 个文件")
    
    if not_found_files:
        print(f"\n未找到的文件列表:")
        for file in not_found_files:
            print(f"  - {file}")

def main():
    """
    主函数 - 使用示例
    """
    # 请根据您的实际路径修改以下参数
    txt_file_path = "/mnt/data/yangchengcity/diffusion_reflection/kunshanzhongxue/partition/partitions-dim_3_3_visibility_0.05/000_000.txt"  # txt文件路径
    source_folder = "source_images"   # 源图像文件夹路径
    destination_folder = "selected_images"  # 目标文件夹路径
    
    print("图像复制工具")
    print("=" * 50)
    
    # 检查txt文件是否存在
    if not os.path.exists(txt_file_path):
        print(f"错误: txt文件 '{txt_file_path}' 不存在")
        print("请确保txt文件路径正确")
        return
    
    # 检查源文件夹是否存在
    if not os.path.exists(source_folder):
        print(f"错误: 源文件夹 '{source_folder}' 不存在")
        print("请确保源文件夹路径正确")
        return
    
    print(f"txt文件: {txt_file_path}")
    print(f"源文件夹: {source_folder}")
    print(f"目标文件夹: {destination_folder}")
    print("-" * 50)
    
    # 执行复制操作
    copy_images_from_txt(txt_file_path, source_folder, destination_folder)

if __name__ == "__main__":
    main()
