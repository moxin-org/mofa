import os
from pathlib import Path

# 获取当前文件（即 __init__.py）的绝对路径
package_root = os.path.abspath(os.path.dirname(__file__))
mae_path = os.path.join(package_root,  )
examples_dir_path = Path(str(mae_path)).parent / 'examples'