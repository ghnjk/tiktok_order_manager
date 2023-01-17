# 电商tiktok订单工具

## 功能说明

- 从rar中的pdf面单提取订单信息，转成xls，支持批量倒入到bigseller

## 安装说明

- 安装python3.8+
- 安装依赖包
- window环境需要额外安装rar:
    - 打开libs，点击7z2201.exe进行安装
    - 安装目录选择到./libs/7-Zip

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
- 将面单的PDF压缩包和对应的结算单excel表放到upload目录。
    - rar文件名为： 20xx-xx-xx.rar
    - excel的文件为：20xx-xx-xx.sku.xlsx
- 15秒后upload目录中会自动生成一个同名的excel文件用来导入到ERP
    - 生成的文件名为： 20xx-xx-xx.big_seller.xlsx
- 到big seller系统导入
