import os
import shutil

def copy_images_from_txt(txt_file_path, source_folder, destination_folder):
    """
    从txt文件中读取图像名称，并将对应的图像从源文件夹复制到目标文件夹
    
    Args:
        txt_file_path (str): 包含图像名称的txt文件路径
        source_folder (str): 源图像文件夹路径
        destination_folder (str): 目标文件夹路径
    """
    
    # 创建目标文件夹（如果不存在）
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print("创建目标文件夹: {}".format(destination_folder))
    
    # 支持的图像格式
    image_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.JPG', '.JPEG', '.PNG', '.BMP']
    
    copied_count = 0
    not_found_count = 0
    not_found_files = []
    
    # 检查txt文件是否存在
    if not os.path.exists(txt_file_path):
        print("错误: txt文件 '{}' 不存在".format(txt_file_path))
        return
    
    # 检查源文件夹是否存在
    if not os.path.exists(source_folder):
        print("错误: 源文件夹 '{}' 不存在".format(source_folder))
        return
    
    try:
        # 读取txt文件
        with open(txt_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            total_lines = len(lines)
            print("txt文件中共有 {} 行".format(total_lines))
            
            for line_num, line in enumerate(lines, 1):
                # 去除行首行尾的空白字符
                image_name = line.strip()
                
                # 跳过空行和注释行
                if not image_name or image_name.startswith('#'):
                    continue
                
                print("处理第 {}/{} 行: {}".format(line_num, total_lines, image_name))
                
                # 查找图像文件
                found = False
                
                # 检查文件名是否已包含扩展名
                has_extension = False
                for ext in image_extensions:
                    if image_name.lower().endswith(ext.lower()):
                        has_extension = True
                        break
                
                if not has_extension:
                    # 如果文件名没有扩展名，尝试所有支持的格式
                    for ext in image_extensions:
                        source_path = os.path.join(source_folder, image_name + ext)
                        if os.path.exists(source_path):
                            destination_path = os.path.join(destination_folder, image_name + ext)
                            try:
                                shutil.copy2(source_path, destination_path)
                                print("  ✓ 已复制: {}".format(image_name + ext))
                                copied_count += 1
                                found = True
                                break
                            except Exception as e:
                                print("  ✗ 复制失败: {} - {}".format(image_name + ext, str(e)))
                else:
                    # 文件名已包含扩展名
                    source_path = os.path.join(source_folder, image_name)
                    if os.path.exists(source_path):
                        destination_path = os.path.join(destination_folder, image_name)
                        try:
                            shutil.copy2(source_path, destination_path)
                            print("  ✓ 已复制: {}".format(image_name))
                            copied_count += 1
                            found = True
                        except Exception as e:
                            print("  ✗ 复制失败: {} - {}".format(image_name, str(e)))
                
                if not found:
                    print("  ✗ 未找到图像: {}".format(image_name))
                    not_found_count += 1
                    not_found_files.append(image_name)
    
    except Exception as e:
        print("读取文件时发生错误: {}".format(str(e)))
        return
    
    # 输出统计信息
    print("\n" + "="*50)
    print("复制完成!")
    print("成功复制: {} 个文件".format(copied_count))
    print("未找到: {} 个文件".format(not_found_count))
    print("成功率: {:.1f}%".format(copied_count * 100.0 / (copied_count + not_found_count) if (copied_count + not_found_count) > 0 else 0))
    
    if not_found_files:
        print("\n未找到的文件列表:")
        for i, file in enumerate(not_found_files, 1):
            print("  {}: {}".format(i, file))

def main():
    """
    主函数
    """
    print("图像复制工具 v2.0")
    print("="*50)
    
    # 获取用户输入
    txt_file_path = input("请输入txt文件路径 (例: image_list.txt): ").strip()
    if not txt_file_path:
        txt_file_path = "image_list.txt"
    
    source_folder = input("请输入源图像文件夹路径 (例: ./images): ").strip()
    if not source_folder:
        source_folder = "./images"
    
    destination_folder = input("请输入目标文件夹路径 (例: ./selected_images): ").strip()
    if not destination_folder:
        destination_folder = "./selected_images"
    
    print("\n配置信息:")
    print("txt文件: {}".format(txt_file_path))
    print("源文件夹: {}".format(source_folder))
    print("目标文件夹: {}".format(destination_folder))
    
    # 确认执行
    confirm = input("\n确认执行? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes', '是']:
        print("操作已取消")
        return
    
    print("\n开始复制...")
    print("-"*50)
    
    # 执行复制操作
    copy_images_from_txt(txt_file_path, source_folder, destination_folder)

if __name__ == "__main__":
    main()