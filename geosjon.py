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


def merge_geojson_list(file_list, output_file):
    merged_gdf = None  # 用于存储合并后的GeoDataFrame

    for file in file_list:
        # 读取当前文件的GeoDataFrame
        gdf = gpd.read_file(file)

        if merged_gdf is None:
            merged_gdf = gdf
        else:
            # 合并当前文件的GeoDataFrame到已合并的GeoDataFrame
            merged_gdf = pd.concat([merged_gdf, gdf], ignore_index=True)
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


def shp_to_geojson(shp_file, geojson_file):
    """
    将SHP文件转换为GeoJSON文件，并保留属性值

    参数:
        shp_file (str): SHP文件路径
        geojson_file (str): 输出的GeoJSON文件路径
    """
    # 读取SHP文件
    gdf = gpd.read_file(shp_file)
    # 将GeoDataFrame转换为GeoJSON
    gdf.to_file(geojson_file, driver='GeoJSON')
    # 压缩生成的GeoJSON文件
    compress_json(geojson_file)
    print("转换完成！")


if __name__ == '__main__':
    # 示例用法
    # file1 = '1_80e5d9341fcf4c0984eb990b96855117.geojson'
    # file2 = '1_beb1286cf51d42c39d8ba6bf6cdf3a7c.geojson'
    # output_file = 'merged2.geojson'

    # 调用方法合并GeoJSON文件
    # merge_geojson_files(file1, file2, output_file)
    shp_to_geojson("/Users/author/Desktop/37shandong370602/370602out-filter.shp",
                   "/Users/author/Desktop/37shandong370602/370602out-filter.geojson")
    # 示例用法
    # file_list = [
    #     '/Users/author/Desktop/37shandong370602/370602/1ae33b5393094129b403bd97b8b9d9ea.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/30af738770744c399dbf9c8e58ddf089.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/51652d23526844fb9e779e07895fafaf.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/6d43b8c5a08941fcbe12818375624e03.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/75430b139ed4494db404b0cc2d876116.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/819aff30646b4d08bf5af17b106af1b7.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/8f470c0f46854c33bd788177b40c94b1.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/9218db3073494e9bbfe74706e47fd99f.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/95c5dc84e2ed40fd93b53c42aa1a9f5b.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/af0d96d1094245f68b7219846b690fd1.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/d447491157bb40468aac55f9d40e9f3e.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/d762f9494de44e5aab4b67027c78929c.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/da5f817d96d94d86a5328455e3bdf24d.geojson',
    #     '/Users/author/Desktop/37shandong370602/370602/ea6a3d2cd1b74bf1b1260f8a254e421a.geojson',
    #     # 添加其他文件...
    # ]
    # basePath = '/Users/author/Desktop/37shandong370602/370602'
    # output_file = '/Users/author/Desktop/37shandong370602/370602out.geojson'
    # merge_geojson_list(file_list, output_file)
    # compress_json('/Users/author/Documents/test.geojson')
