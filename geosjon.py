import json
import os

import geopandas as gpd
import pandas as pd


def delete_geojson_properties(input_file, output_file, columns_to_delete):
    """
    删除 geojson的属性
    # 示例用法
    input_file = '/Users/author/Documents/test.geojson'
    output_file = '/Users/author/Documents/test2.geojson'
    columns_to_delete = ['path']  # 要删除的属性列名

    # 调用方法删除属性
    delete_geojson_properties(input_file, output_file, columns_to_delete)
    """
    # 读取 GeoJSON 文件
    gdf = gpd.read_file(input_file)
    print(gdf.columns)
    # 删除属性列
    gdf = gdf.drop(columns=columns_to_delete)

    # 保存修改后的 GeoJSON
    gdf.to_file(output_file, driver='GeoJSON')


def merge_geojson_files(file1, file2, output_file):
    # 读取第一个GeoJSON文件
    gdf1 = gpd.read_file(file1)
    # 读取第二个GeoJSON文件
    gdf2 = gpd.read_file(file2)
    # 合并两个GeoDataFrame
    merged_gdf = gpd.GeoDataFrame(pd.concat([gdf1, gdf2], ignore_index=True))
    # 保存合并后的GeoJSON文件
    merged_gdf.to_file(output_file, driver='GeoJSON')
    # 压缩生成的GeoJSON文件
    compress_json(output_file)


def compress_json(input_file):
    # 读取输入文件
    with open(input_file, 'r') as f_in:
        data = json.load(f_in)
    # 构建输出文件路径
    _output_file = os.path.splitext(input_file)[0] + '_compress' + os.path.splitext(input_file)[1]
    # 写入压缩后的输出文件
    with open(_output_file, 'w') as f_out:
        json.dump(data, f_out, separators=(',', ':'))


if __name__ == '__main__':
    # 示例用法
    file1 = '1_80e5d9341fcf4c0984eb990b96855117.geojson'
    file2 = '1_beb1286cf51d42c39d8ba6bf6cdf3a7c.geojson'
    output_file = 'merged2.geojson'

    # 调用方法合并GeoJSON文件
    merge_geojson_files(file1, file2, output_file)
