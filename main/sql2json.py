import base64
import sqlite3
import shutil
import json
import os
import binascii


# 获取当前脚本所在目录的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 获取当前用户的 LOCALAPPDATA 路径
local_appdata = os.getenv('LOCALAPPDATA')

# 定义源复制的文件路径
source_file = os.path.join(local_appdata, 'Microsoft', 'Edge', 'User Data', 'Default', 'Login Data')

# 定义目标文件路径，防止别的程序占用
target_file = os.path.join(current_dir, 'copyed.db')

try:
    shutil.copyfile(source_file, target_file)
    print(f"已成功复制文件到 {target_file}")
except IOError as e:
    print(f"复制文件时发生错误：{e}")

# 定义 SQLite 数据库文件路径变量
db_file = os.path.join(current_dir, 'copyed.db')


print(f"数据库文件路径：{db_file}")
def convert_to_json():
    try:
        # 连接到 SQLite 数据库
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # 执行查询语句（假设表名为 logins）
        cursor.execute('SELECT * FROM logins')

        # 获取所有行数据
        rows = cursor.fetchall()


        # 构建 JSON 数据
        json_data = []
        for row in rows:
            # 使用 base64 编码将字节数据转换为字符串
            data = row[5]
            hex_data = binascii.hexlify(data).decode('utf-8')
            print(hex_data)

            password_value = base64.b64encode(row[5],).decode('utf-8') if isinstance(row[5], bytes) else str(row[5])
            from_data = base64.b64encode(row[13]).decode('utf-8') if isinstance(row[13], bytes) else str(row[13])
            possible_username_pairs = base64.b64encode(row[19]).decode('utf-8') if isinstance(row[19], bytes) else str(row[19])
            moving_blocked_for = base64.b64encode(row[22]).decode('utf-8') if isinstance(row[22], bytes) else str(row[22])
            sender_profile_image_url =base64.b64encode(row[28]).decode('utf-8') if isinstance(row[28], bytes) else str(row[28])
            #这几行必须转base64 不然无法正常输出
            password_bytes = row[5]
            password_hex = binascii.hexlify(password_bytes).decode('utf-8')
            #将密码转换成hex加以验证

            #验证过程
            # 将 Hex 格式的密码转换为 bytes
            password_bytes_1 = binascii.unhexlify(password_hex)
            # 将 bytes 数据转换为 Base64 编码的字符串
            password_base64 = base64.b64encode(password_bytes_1).decode('utf-8')
            # 比较 Base64 编码后的结果
            if password_base64 == password_value:
                result = "相同"
            else:
                result = "不相同"

            json_item = {
                'origin_url': row[0],
                'action_url': row[1],
                'username_element': row[2],
                'username_value': row[3],
                'password_element': row[4],
                'password_value = password_base64 ': password_value,
                'submit_element': row[6],
                'signon_realm': row[7],
                'date_created': row[8],
                'blacklisted_by_user': row[9],
                'scheme': row[10],
                'password_type': row[11],
                'times_used': row[12],
                'from_data': from_data,
                'display_name': row[14],
                'icon_url': row[15],
                'federation_url': row[16],
                'skip_zero_click': row[17],
                'generation_upload_status': row[18],
                'possible_username_pairs': possible_username_pairs,
                'id': row[20],
                'date_last_used': row[21],
                'moving_blocked_for': moving_blocked_for,
                'date_password_modified': row[23],
                'sender_email': row[24],
                'date_received': row[25],
                'sharing_notification_displayed': row[26],
                'keychain_identifier': row[27],
                'sender_profile_image_url': sender_profile_image_url,
                'password_hex': password_hex,
                '密码比较': result
            }
            json_data.append(json_item)

        # JSON 文件路径（保存到当前目录的 output.json 文件）
        json_file_path = os.path.join(current_dir, '你的账户数据库.json')

        # 将数据写入 JSON 文件
        with open(json_file_path, 'w', encoding='utf-8') as f:
            json.dump(json_data, f, ensure_ascii=False, indent=4)

        print(f"数据成功转换为 JSON 格式并保存到 {json_file_path} 文件")

    except sqlite3.Error as e:
        print(f"SQLite 错误：{e}")

    finally:
        # 关闭数据库连接
        if conn:
            conn.close()

# 调用函数执行转换操作
convert_to_json()
