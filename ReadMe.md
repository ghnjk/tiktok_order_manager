# 电商tiktok订单工具

## 功能说明

- 从rar中的pdf面单提取订单信息，转成xls，支持批量倒入到bigseller

## 安装说明

- 安装python3.8+
- 安装依赖包

```angular2html
pip3 install -r requirements.txt
```

## 启动程序

- windows:

```
./restart.bat
```

- mac/linux

```
./restart.sh
```

## 批量导入TIKTOK订单，使用说明

- 打开upload目录
- 将rar包放到upload目录，例如xxx.rar
- 15秒后upload目录中会自动生成一个同名的excel文件xxx.xlsx
- 到big seller系统导入

## 商品和big seller的SKU转换， 使用说明

- ./data/sku_map.txt文件打开，直接编辑
- 参考如下格式编辑

```
<tiktok 面单中显示的商品> = <big seller 录入的sku名>
New combination = CW-2-Set (new type)
```