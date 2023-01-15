#!/usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@file: tiktok_order
@author: jkguo
@create: 2023/1/15
"""
import typing

from openpyxl import load_workbook

SKU_MAP: typing.Dict[str, typing.List[str]] = {
}


def read_sku_map():
    SKU_MAP.clear()
    with open("./data/sku_map.txt", "r", encoding="utf-8") as fp:
        for line in fp:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.find("=") < 0:
                continue
            if line.startswith("<"):
                continue
            if line.startswith("#"):
                continue
            fields = line.split("=")
            if len(fields) != 2:
                continue
            key = fields[0]
            value = fields[1]
            key = key.strip()
            value = value.strip()
            if key not in SKU_MAP:
                SKU_MAP[key] = []
            SKU_MAP[key].append(value)
    import logging
    logging.info(f"loading sku map {SKU_MAP}")


class TikTokOrder(object):

    def __init__(self):
        self.track_order: str = ""
        self.sender_addr: str = ""
        self.receiver_addr: str = ""
        self.weight: str = ""
        self.goods: str = ""
        self.sku_list: typing.List[str] = []
        self.payment: str = "COD"
        self.tiktok_order_id: str = ""
        self.cod: str = ""
        self.sender_name: str = ""

    def __str__(self):
        return f"TT Order ID: {self.tiktok_order_id}\n" \
               f"Track Order: {self.track_order}\n" \
               f"SKU: {self.goods}\n" \
               f"Weight: {self.weight}\n" \
               f"Payment: {self.payment}\n" \
               f"Price: {self.cod}\n" \
               f"---------\n" \
               f"{self.sender_addr}\n" \
               f"---------\n" \
               f"{self.receiver_addr}"

    def parse(self, text_list: typing.List[str]):
        # for line in text_list:
        #     print("======")
        #     print(line)
        offset = 0
        for i in range(len(text_list)):
            if i - offset == 1:
                self.track_order = text_list[i]
            elif i - offset == 3:
                self.sender_name = text_list[i]
            elif i - offset == 4:
                self.sender_addr = text_list[i]
            elif i - offset == 6:
                self.receiver_addr = text_list[i]
            elif i - offset == 7:
                if text_list[i].startswith("Weigh"):
                    self.weight = text_list[i]
                else:
                    offset += 1
                    self.receiver_addr += " phone: " + text_list[i]
            elif i - offset == 8:
                self.goods = text_list[i].split("\n")[0][7:]
                # self.payment = text_list[i].split("\n")[1]
            elif i - offset in [9, 10]:
                if len(text_list[i]) > 6:
                    self.cod = text_list[i].replace("\n", " ")[5:].replace("PHP", "").strip()
            elif i - offset in [11, 12, 13, 14, 15]:
                if text_list[i].isdigit():
                    self.tiktok_order_id = text_list[i]
        self.sku_list = SKU_MAP.get(self.goods, [self.goods])
        self.tiktok_order_id = self.tiktok_order_id[:-3] + "111"

    def to_xls_row(self) -> typing.List[typing.List[str]]:
        rows = []
        for sku in self.sku_list:
            rows.append(
                [
                    self.tiktok_order_id,
                    self.track_order,
                    sku,
                    "1",
                    self.cod,
                    "",
                    self.get_receiver_name(),
                    self.get_receiver_phone(),
                    self.receiver_addr,
                    "",
                    "",
                    self.payment,
                    "",
                    "",
                    "J&T EXPRESS",
                    "",
                    "",
                    self.sender_name,
                    "",
                    self.sender_addr,
                    "",
                    ""
                ]
            )
        return rows

    def get_receiver_name(self):
        s = self.receiver_addr[10:].split("\n")[0]
        return s

    def get_receiver_phone(self):
        s = self.receiver_addr
        idx = s.find("(+63)")
        if idx >= 0:
            idx += 5
            s = s[idx:].strip()
            for idx in range(min(20, len(s))):
                if not s[idx].isdigit():
                    break
            return s[: idx]
        return ""

    def is_valid_order(self):
        if len(self.tiktok_order_id) == 0:
            return False
        if len(self.track_order) == 0:
            return False
        return True


def append_orders_to_xls(order_list: typing.List[TikTokOrder], xls_file_path: str,
                         template_xls_file_path: str = "./data/import_hand_order_template_cn.xlsx"):
    wb = load_workbook(filename=template_xls_file_path)
    # 打开第一个sheet
    ws = wb[wb.sheetnames[0]]
    # row_idx = 0
    # while True:
    #     row_idx += 1
    #     v = ws.cell(row=row_idx, column=1).value
    #     if v is None:
    #         break
    #     print(v)
    for order in order_list:
        for r in order.to_xls_row():
            ws.append(r)
        print(f"add {order.tiktok_order_id}")
    wb.save(xls_file_path)
    wb.close()
