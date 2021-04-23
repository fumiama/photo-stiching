# 照片拼接

## 官方版
`opencv`现在具有官方拼接工具，效果很好，可以直接调用本仓库封装好的`stitch_official.py`进行拼接。命令格式如下

```bash
Usage: <match_ext_name> <input_dir> <output_file>
```

其中，`match_ext_name`是`input_dir`下搜寻的图片文件的扩展名，如`jpg`、`png`等，图片数量任意。

## 学习研究版

本仓库还有一个基于`SIFT`写的图片拼接工具`stitch_mimicry.py`，该工具效果不如官方，且仅能拼接两张图片，但是可以完成基本功能。在图片相似度（亮度、对比度）较高时可以使用。

如果想要调节两个图片拼接的亮度，可以更改`imgstitch/brightness.py`的`adjust_v`函数的`increase_brightness(img, int(0 * (my_mean - average_v_mean)))`中的`0`为任意比例值，可正可负。