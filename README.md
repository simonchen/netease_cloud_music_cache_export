# netease_cloud_music_cache_export
This util tool helps to export the cached music files from Netease Cloud Music
Those exported music files will be renamed automaically as original song name.

## Program languages
The source codes is writted by [Python](http://python.org), idealy, it can be running on any platform that you installed Python.
Especially, I've packaged a windows executalbe file in dist folder, therfore, you can directly peform the exe file without installing Python.

## Comiple executable file on Windows
Type below command line in console (before you should make sure that you installed [Py2exe](https://pypi.python.org/pypi/py2exe) module for the specific version of Python)

*Python setup.py py2exe*

## Running command line

- Python script

*python netease_cloud_music_cache_export.py [cache folder] [output_folder]

**[cache_folder]**
It's the source folder where Netease Cloud Music store cahced music files, usually, it's the folder at 
*C:\Users\{user name}\AppData\Local\Netease\CloudMusic\Cache\Cache*

**[output_folder]**
The destination folder where you want to export music files.

- Executeable file

*cd dist
*netease_cloud_music_cache_export.exe [cache folder] [output_folder]*

<hr/>

这个实用工具可以帮助你轻松转出缓存的网易云音乐文件，转出的网易云音乐文件名将被自动重命名为原歌曲名.mp3
可执行文件被打包在dist文件夹中，简单执行命令行转出缓存的MP3音乐文件:

- Python 脚本

*python netease_cloud_music_cache_export.py [cache folder] [output_folder]*

**[cache_folder]**
网易云音乐会存储缓冲的MP3音乐文件在这个目录里：
*C:\Users\{user name}\AppData\Local\Netease\CloudMusic\Cache\Cache*

**[output_folder]**
目标转出文件夹

- 可执行文件

*cd dist
*netease_cloud_music_cache_export.exe [cache folder] [output_folder]*
