import concurrent.futures

import requests


def download_file(url, output_path):
    """
    从给定的URL下载文件到指定的输出路径

    参数:
        url (str): 文件的URL
        output_path (str): 输出路径，包括文件名和扩展名
    """
    response = requests.get(url)
    with open(output_path, 'wb') as f:
        f.write(response.content)


def download_all_files(urls, output_folder):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # 提交下载任务给线程池
        download_futures = []
        for url in urls:
            # 构建完整的URL
            full_url = base_url + url

            # 构建输出文件路径
            filename = url.split('/')[-1]
            output_path = output_folder + filename

            # 提交下载任务
            future = executor.submit(download_file, full_url, output_path)
            download_futures.append(future)

        # 等待所有下载任务完成
        concurrent.futures.wait(download_futures)


if __name__ == '__main__':
    # 示例用法
    # 示例用法
    urls = [
        '/geojson/37/af0d96d1094245f68b7219846b690fd1.geojson',
        '/geojson/37/6d43b8c5a08941fcbe12818375624e03.geojson',
        '/geojson/37/1ae33b5393094129b403bd97b8b9d9ea.geojson',
        '/geojson/37/d447491157bb40468aac55f9d40e9f3e.geojson',
        '/geojson/37/da5f817d96d94d86a5328455e3bdf24d.geojson',
        '/geojson/37/d762f9494de44e5aab4b67027c78929c.geojson',
        '/geojson/37/9218db3073494e9bbfe74706e47fd99f.geojson',
        '/geojson/37/8f470c0f46854c33bd788177b40c94b1.geojson',
        '/geojson/37/30af738770744c399dbf9c8e58ddf089.geojson',
        '/geojson/37/51652d23526844fb9e779e07895fafaf.geojson',
        '/geojson/37/75430b139ed4494db404b0cc2d876116.geojson',
        '/geojson/37/ea6a3d2cd1b74bf1b1260f8a254e421a.geojson',
        '/geojson/37/819aff30646b4d08bf5af17b106af1b7.geojson',
        '/geojson/37/95c5dc84e2ed40fd93b53c42aa1a9f5b.geojson',
        # 添加其他URL...
    ]
    output_folder = '/Users/author/Desktop/37shandong370602/370602/'
    base_url = 'http://192.168.80.153:9000/geo'
    # prefixed_array = [base_url + element for element in urls]
    # print(prefixed_array)
    # # 执行多线程下载
    # download_all_files(urls, output_folder)

    for url in urls:
        # 构建完整的URL
        full_url = base_url + url

        # 构建输出文件路径
        filename = url.split('/')[-1]
        output_path = output_folder + filename

        # 下载文件
        download_file(full_url, output_path)
