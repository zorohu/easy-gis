import configparser


def read_config(config_file):
    """从INI配置文件中读取配置"""
    config = configparser.ConfigParser()
    config.read(config_file)
    return config


if __name__ == '__main__':
    config = read_config('config.ini')
    sections = config.sections()
    for section in sections:
        print(f'Section: {section}')
        paths_str = config.get(section, 'geo_src_path')
        paths_str = paths_str.replace('\n', '').replace('\\', '').replace(' ', '')
        paths = [path.strip() for path in paths_str.split(',')]
        xb = config.get(section, 'XB_NUM')
        xb = xb.replace('\n', '').replace('\\', '').replace(' ', '')
        xbs = [path.strip() for path in xb.split(',')]

        print(paths)
        print(xbs)
