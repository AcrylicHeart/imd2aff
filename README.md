# 节奏大师(imd)转Arcaea(aff)

生成的aff适用于arc4.0以后,2024年愚人节之前的版本。
本代码使用4.0以后出现的3号蛇来表示节奏大师中的折线，在节奏大师中，对于时间长度小于33ms的hold，统一转换成了arc的singlearctap。

## 使用方法

在工作目录中创建两个文件夹：`input` 和 `output`。

在`input`中放入要转换的imd，imd的文件名称格式要符合以下习惯：

```
样例
woaini_4k_hd.imd
woaini_5k_ez.imd
woaini_6k_nm.imd
```

运行py代码后会在`output`文件夹中生成对应的aff。
