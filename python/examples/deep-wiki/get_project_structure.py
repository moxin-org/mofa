import sys
from pathlib import Path
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))  # 添加项目根目录到PATH

try:
    from read_file import FileReader
except ImportError as e:
    print(f"模块导入失败: {str(e)}")
    sys.exit(1)

def main():
    project_root = Path("/Users/chenzi/chenzi/project/zcbc/mofa/python/examples/deep-wiki")
    
    try:
        fr = FileReader(base_path=project_root)
        structure = fr.generate_file_tree(max_depth=3)
        
        if not structure:
            print("无法生成项目结构")
            return
            
        print(yaml.dump(structure, allow_unicode=True))
        
    except Exception as e:
        print(f"结构生成错误: {str(e)}")

if __name__ == "__main__":
    main()
