import os
import json

# 获取当前脚本所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 构建源文件路径
local_appdata = os.getenv('LOCALAPPDATA')
source_file = os.path.join(local_appdata, 'Microsoft', 'Edge', 'User Data', 'Local State')

# 构建目标文件路径（保存到当前目录下）
target_file = os.path.join(current_dir, '你的账户解密文件密码在encrypted_key里.json')

try:
    # 打开源文件进行读取
    with open(source_file, 'r', encoding='utf-8') as f_source:
        content = f_source.read()

        # 解析 JSON 数据
        local_state_data = json.loads(content)

        # 获取 encrypted_key 的值
        encrypted_key = local_state_data.get('os_crypt', {}).get('encrypted_key')

        if encrypted_key:
            print(f"成功获取 encrypted_key：{encrypted_key}")
        else:
            print("未找到 encrypted_key")

        # 将数据写入目标文件
        with open(target_file, 'w', encoding='utf-8') as f_target:
            json.dump(local_state_data, f_target, ensure_ascii=False, indent=4)

        print(f"已成功将文件保存到 {target_file}")

except FileNotFoundError:
    print(f"文件 '{source_file}' 未找到")
except IOError as e:
    print(f"读取或写入文件发生错误：{e}")
except json.JSONDecodeError as e:
    print(f"解析 JSON 数据时发生错误：{e}")
