import geopandas as gpd


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


if __name__ == '__main__':
    # 调用方法进行转换
    # geojson_file = "data/data.geojson"
    # shp_file = "data/output.shp"
    # geojson_to_shp(geojson_file, shp_file)
    # 调用方法进行过滤和生成新的SHP文件
    input_shp = "data/output.shp"
    output_shp = "data/test.shp"
    query = "cun == '056'"
    filter_shp_by_query(input_shp, output_shp, query)
