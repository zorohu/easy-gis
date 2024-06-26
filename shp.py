# import fiona
import geopandas as gpd
from geopandas.io.file import fiona
from pyproj import Transformer
from shapely import Point
from shapely.ops import transform

from transform import Transform


def geojson_to_shp(geojson_file, shp_file):
    """
    将GeoJSON文件转换为SHP文件

    参数:
        geojson_file (str): GeoJSON文件路径
        shp_file (str): 输出的SHP文件路径
    """
    # 读取GeoJSON文件为GeoDataFrame对象
    gdf = gpd.read_file(geojson_file)
    # 将GeoDataFrame对象保存为SHP文件
    gdf.to_file(shp_file)
    print("转换完成！")


def filter_shp_by_attribute(input_shp, output_shp, attribute_name, attribute_value):
    """
    根据SHP文件的属性进行过滤，生成新的SHP文件

    参数:
        input_shp (str): 输入的SHP文件路径
        output_shp (str): 输出的SHP文件路径
        attribute_name (str): 属性字段名称
        attribute_value: 过滤条件的属性值
    """
    # 读取SHP文件为GeoDataFrame对象
    gdf = gpd.read_file(input_shp)
    # 根据属性过滤数据
    filtered_gdf = gdf[gdf[attribute_name] == attribute_value]
    # 将过滤后的数据保存为新的SHP文件
    filtered_gdf.to_file(output_shp)

    print("生成新的SHP文件完成！")


def filter_shp_by_query(input_shp, output_shp, query):
    """
    根据查询语句过滤SHP文件的属性，生成新的SHP文件

    参数:
        input_shp (str): 输入的SHP文件路径
        output_shp (str): 输出的SHP文件路径
        query (str): 查询语句，类似SQL的语法
    """
    # 读取SHP文件为GeoDataFrame对象
    gdf = gpd.read_file(input_shp)
    # 使用查询语句过滤数据
    filtered_gdf = gdf.query(query)
    # 将过滤后的数据保存为新的SHP文件
    filtered_gdf.to_file(output_shp)

    print("生成新的SHP文件完成！")


def find_polygon_for_point(point, shp_file, query):
    """
    查询一个坐标点在SHP文件中符合条件的多边形中

    参数:
        point (tuple): 要查询的点的坐标，格式为 (经度, 纬度)
        shp_file (str): SHP文件的路径
        query (str): 查询条件，类似SQL的语法
    返回:
        str: 符合条件的多边形的属性值，如果没有符合条件的多边形，则返回None
    """
    # 创建点对象
    point_geom = Point(point)
    # 读取SHP文件为GeoDataFrame对象
    gdf = gpd.read_file(shp_file)
    # 判断点是否在SHP文件的范围内
    filtered_gdf = gdf
    if query is not None:
        # 使用查询条件筛选多边形
        filtered_gdf = gdf.query(query)
    # 遍历筛选后的多边形，查找包含点的多边形
    for index, row in filtered_gdf.iterrows():
        if row.geometry.contains(point_geom):
            print(f"index: {index}, geometry: {row.geometry}")
            return row  # 替换为实际的属性字段名

    return None


def project_coordinates(input_file, output_file, input_crs, output_crs):
    """
    将坐标投影转换为指定的坐标系

    参数:
        input_file (str): 输入文件的路径（支持常见的地理数据格式，如SHP、GeoJSON等）
        output_file (str): 输出文件的路径（生成的投影转换后的地理数据）
        input_crs (str): 输入坐标系的EPSG代码或proj4字符串
        output_crs (str): 输出坐标系的EPSG代码或proj4字符串
    """
    # 读取输入文件为GeoDataFrame对象
    gdf = gpd.read_file(input_file)

    # 创建坐标转换器
    transformer = Transformer.from_crs(input_crs, output_crs, always_xy=True)

    # 进行坐标转换
    gdf['geometry'] = gdf['geometry'].apply(lambda geom: transform(transformer.transform, geom))

    # 将转换后的结果保存为新文件
    gdf.to_file(output_file, driver='ESRI Shapefile')


def recur_map(f, data):
    """递归处理所有坐标

    Arguments:
        f {function} -- [apply function]
        data {collection} -- [fiona collection]
    """

    return [not type(x) is list and f(x) or recur_map(f, x) for x in data]


def project_convertor(src_path, dst_path, convert_type):
    """convert input china coordinate to another.

\b
    Arguments:
        convert_type {string} -- [coordinate convert type, e.g. wgs2bd]
\b
            wgs2gcj : convert WGS-84 to GCJ-02
            wgs2bd  : convert WGS-84 to DB-09
            gcj2wgs : convert GCJ-02 to WGS-84
            gcj2bd  : convert GCJ-02 to BD-09
            bd2wgs  : convert BD-09 to WGS-84
            bd2gcj  : convert BD-09 to GCJ-02

        src_path {string} -- [source file path]
        dst_path {string} -- [destination file path]


    Example:

\b
        coord_covert wgs2gcj ./test/data/line/multi-polygon.shp ~/temp/qqqq.shp
    """

    with fiona.open(src_path, 'r', encoding='utf-8') as source:
        source_schema = source.schema.copy()
        with fiona.open(dst_path, 'w', encoding='utf-8', **source.meta) as out:
            transform = Transform()
            f = lambda x: getattr(transform, convert_type)(x[0], x[1])  #dynamic call convert func

            for fea in source:
                collections = fea['geometry']['coordinates']
                if type(collections) is tuple:
                    fea['geometry']['coordinates'] = f(collections)
                elif type(collections) is list:
                    fea['geometry']['coordinates'] = recur_map(f, collections)
                else:
                    raise TypeError("collection must be list or tuple")
                out.write(fea)


def delete_attributes(input_file, output_file, attributes):
    """
    从Shapefile中删除指定的属性列

    参数:
        input_file (str): 输入Shapefile文件的路径
        output_file (str): 输出Shapefile文件的路径
        attributes (list): 要删除的属性列的名称列表
    """
    # 读取输入Shapefile文件为GeoDataFrame对象
    gdf = gpd.read_file(input_file)

    # 删除指定的属性列
    gdf.drop(columns=attributes, inplace=True)

    # 保存删除属性后的结果为新Shapefile文件
    gdf.to_file(output_file)


if __name__ == '__main__':
    # 调用方法进行转换
    # geojson_file = "data/data.geojson"
    # shp_file = "data/output.shp"
    # geojson_to_shp(geojson_file, shp_file)

    # 调用方法进行过滤和生成新的SHP文件
    # input_shp = "data/output.shp"
    # output_shp = "data/test.shp"
    # query = "cun == '056'"
    # filter_shp_by_query(input_shp, output_shp, query)

    # 调用方法进行查询 注意x,y顺序
    # point = (37.375671, 121.717757)
    # point = (37.381003, 121.722481)
    # point = (121.706408, 37.375153)
    # point = (121.706046, 37.374998)
    # point = (121.710019, 37.377302)
    # point = (121.709216, 37.373135)
    # shp_file = "test.shp"
    # # query = "属性字段 = '条件值'"  # 替换为实际的查询条件
    # result = find_polygon_for_point(point, shp_file, None)
    # print(result)

    # 指定输入文件、输出文件、输入坐标系和输出坐标系
    # input_file = "data/test.shp"
    # output_file = "output.shp"
    # # input_crs = "EPSG:4490"  # WGS84 经纬度坐标系
    # output_crs = "EPSG:3857"  # Web Mercator 投影坐标系
    # # 执行投影转换
    # project_convertor(input_file, output_file, "wgs2gcj")

    # 示例用法
    input_file = 'data/test.shp'
    output_file = 'output.shp'
    attributes_to_delete = ['bhnd']  # 要删除的属性列的名称列表

    delete_attributes(input_file, output_file, attributes_to_delete)
