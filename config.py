import configparser


def read_config(config_file):
    """从INI配置文件中读取配置"""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config
