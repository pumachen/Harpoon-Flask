# 快速开始

**1.通过git拉取（推荐）**
```bash
git clone https://github.com/pumachen/Harpoon-Flask.git
```
**2.下载压缩包**

> [https://github.com/pumachen/Harpoon-Flask/archive/refs/heads/main.zip](https://github.com/pumachen/Harpoon-Flask/archive/refs/heads/main.zip)

# 添加资产

## HDALibrary

创建HDALibrary目录，放入HDA文件

# 启动服务

**1. 打开命令行窗口**

> A. 通过Houdini工具栏Window->Shell启动

> B. 将```hython.exe```加入环境变量，通过CMD启动

*hython.exe位于Houdini安装目录/bin/hython.exe*


**2. 运行服务**

```bash
hython harpoon.py -p 端口号
```

可选参数：
* ```-p``` ```--port``` 指定服务器端口
* ```-d``` ```--debug``` 以调试模式启动
* ```-h``` ```--help``` ```-?``` 输出参数说明
