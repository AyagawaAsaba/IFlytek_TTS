import requests


def download_audio(url, local_filename):
    """
    下载音频文件并保存到本地
    :param url: 音频文件的网址
    :param local_filename: 自定义的本地保存文件名（包括路径和扩展名）
    :return: 本地文件路径
    """
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return local_filename


# # 音频文件的URL，请替换为你想要下载的音频链接
# audio_url = 'http://example.com/path/to/audio.mp3'
# # 自定义保存的文件名，包括路径和扩展名
# custom_filename = 'my_custom_audio.mp3'  # 你想保存的文件名
# # 调用函数下载音频文件并指定文件名
# file_path = download_audio(audio_url, custom_filename)
# print(f"音频文件已下载至: {file_path}")
