# unicontainer

拆分容器镜像，并根据unikernel的思想将其制作成基于虚拟化技术隔离的容器，使其在保证性能的前提下获得额外的安全性提升。

## 镜像切片

解析strace输出文件。

## 定制unikernel



## 跨虚拟机的容器通信

### 对unikraft的修改

添加库“unicontainer-exec_hook”，将“syscall-shim”中exec系统调用的控制流转移到“unicontainer-exec_hook”中来。将exec的参数用vmcall传递给kvm。

### 对kvm的修改

接收vmcall传来的参数，用它们到虚拟机的内存中去读取具体的参数，然后新建一个unikraft来运行它。

## 运行

### 目录结构

```
➜  ZZC tree -L 2             
.
├── unicontainer
│   ├── example
│   ├── image_splitting
│   └── README.md
└── unikraft
    ├── dynamic-apps
    └── elfloader
```

