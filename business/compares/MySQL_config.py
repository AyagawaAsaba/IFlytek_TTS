# import DormitoryManager.views
# import DormitoryManager.__init__
import pymysql

# 配置MySQL数据库连接
app_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Zywz5201314',
    'db': 'xf_Project',
}

mysql = pymysql.connect(**app_config)  # type: ignore
