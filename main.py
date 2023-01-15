#!/usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@file: utils
@author: jkguo
@create: 2023/1/15
"""
import logging
import logging.config as log_config
import os
import shutil
import time

from tiktok_order import TikTokOrder, append_orders_to_xls, read_sku_map
from utils import parse_pdf, extract_file


def parse_and_convert_tiktok_orders(rar_file: str, xls_file: str):
    order_list = []
    rar_base_name = os.path.basename(rar_file)[: -4]
    tmp_dir = f"./tmp/{rar_base_name}"
    if os.path.isdir(tmp_dir):
        shutil.rmtree(tmp_dir)
    os.mkdir(tmp_dir)
    extract_file(rar_file, tmp_dir)
    for file in os.listdir(tmp_dir):
        abs_path = os.path.join(tmp_dir, file)
        if not file.endswith(".pdf"):
            continue
        if os.path.isfile(abs_path):
            order = TikTokOrder()
            order.parse(parse_pdf(abs_path))
            if order.is_valid_order():
                logging.info(f"add order {order.tiktok_order_id}")
                logging.debug(order)
                order_list.append(order)
            else:
                logging.error(f"parse file {file} failed.")
                logging.error(order)
    append_orders_to_xls(order_list, xls_file)


def main():
    upload_dir = "./upload"
    while True:
        read_sku_map()
        for file in os.listdir(upload_dir):
            if not file.endswith(".rar"):
                continue
            xls_file = file[: -4] + ".xlsx"
            xls_file = os.path.join(upload_dir, xls_file)
            if os.path.isfile(xls_file):
                continue
            logging.info(f"start parsing file {file}...")
            try:
                parse_and_convert_tiktok_orders(os.path.join(upload_dir, file), xls_file)
            except Exception as e:
                logging.error(f"process file {file} failed", e)
        time.sleep(10)


def test_parsing():
    test_file = "./data/pdf/dvQxLioSMlIduvQkmshwSU5nUASEhStf_1673657890533.pdf"
    i = 0
    for line in parse_pdf(test_file):
        print(f"=====  {i} ====")
        print(line)
        i += 1
    o = TikTokOrder()
    o.parse(parse_pdf(test_file))
    print(o)


if __name__ == '__main__':
    log_config.fileConfig('./conf/logging.conf')
    main()
