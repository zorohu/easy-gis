import json
import os

import shp
import geosjon
import utils
import config
import pgsql_util
from geoalchemy2 import Geometry, WKTElement

if __name__ == '__main__':
    with open('/Users/author/Desktop/8a181c813bf0493592a86f400811d0e7.geojson', 'r') as f:
        geojson_data = json.load(f)

    for feature in geojson_data['features']:
        properties = feature['properties']
        geometry = feature['geometry']

        insert_query = """
        INSERT INTO your_table_name (
            id, ban_resource_year, city, county, di_lei, di_mao, is_pine, lat, ld_cd, ld_kd, lin_ban, lin_chang,
            lin_ye_ju, lng, location, mian_ji, ping_jun_xj, po_du, po_wei, po_xiang, province, status, town,
            tu_ceng_hd, village, xb_num, xiao_ban, you_shi_sz_code, yu_bi_du
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        values = (
            properties['id'],
            properties['ban_resource_year'],
            properties['city'],
            properties['county'],
            properties['di_lei'],
            properties['di_mao'],
            properties['is_pine'],
            properties['lat'],
            properties['ld_cd'],
            properties['ld_kd'],
            properties['lin_ban'],
            properties['lin_chang'],
            properties['lin_ye_ju'],
            properties['lng'],
            WKTElement(json.dumps(geometry), srid=4490),
            properties['mian_ji'],
            properties['ping_jun_xj'],
            properties['po_du'],
            properties['po_wei'],
            properties['po_xiang'],
            properties['province'],
            properties['status'],
            properties['town'],
            properties['tu_ceng_hd'],
            properties['village'],
            properties['xb_num'],
            properties['xiao_ban'],
            properties['you_shi_sz_code'],
            properties['yu_bi_du']
        )

    config = config.read_config('config.ini')
    sections = config.sections()
    for section in sections:
        print(f'Section: {section}')
        # paths_str = config.get(section, 'geo_src_path')
        # paths_str = paths_str.replace('\n', '').replace('\\', '').replace(' ', '')
        # paths = [path.strip() for path in paths_str.split(',')]
        xb = config.get(section, 'XB_NUM')
        xb = xb.replace('\n', '').replace('\\', '').replace(' ', '')
        xbs = [path.strip() for path in xb.split(',')]
        #
        # xian = "371003"
        xian = section
        basePath = "/Users/author/Desktop/gis/37shandong{}".format(xian)
        geoPath = "{}/{}/".format(basePath, xian)
        # os.makedirs(geoPath, exist_ok=True)
        #
        # if os.path.exists(geoPath):
        #     print("Directory created:", geoPath)
        # else:
        #     print("Failed to create directory:", geoPath)
        # # 1 下载文件
        # urls = paths
        # base_url = 'http://192.168.80.153:9000/geo'
        # file_list = []
        # for url in urls:
        #     # 构建完整的URL
        #     full_url = base_url + url
        #
        #     # 构建输出文件路径
        #     filename = url.split('/')[-1]
        #     output_path = geoPath + filename
        #
        #     # 下载文件
        #     utils.download_file(full_url, output_path)
        #     file_list.append(output_path)
        #
        # # 2 合并文件
        # # output_file = '/Users/author/Desktop/37shandong370602/370602out.geojson'
        # output_file = "{}/{}out.geojson".format(basePath, xian)
        # geosjon.merge_geojson_list(file_list, output_file)
        #
        # # 3 转换shp
        # geojson_file = "{}/{}out_compress.geojson".format(basePath, xian)
        # # shp_file = "/Users/author/Desktop/37shandong370602/370602out.shp"
        shp_file = "{}/{}out.shp".format(basePath, xian)
        # shp.geojson_to_shp(geojson_file, shp_file)

        # 4 开始过滤
        output_shp = "{}/{}out-filter.shp".format(basePath, xian)
        values = xbs
        query = f"xb_num in {tuple(values)}"
        shp.filter_shp_by_query(shp_file, output_shp, query)

        # 5生成json文件
        geosjon.shp_to_geojson("{}/{}out-filter.shp".format(basePath, xian),
                               "{}/{}out-filter.geojson".format(basePath, xian))
