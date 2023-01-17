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
from tiktok_order import TikTokOrder, append_orders_to_xls, SkuMapper, save_order_to_db
from utils import parse_pdf, extract_file

__current_pdf_file_path = None
__current_pdf_lines = []
__current_order = None


def parse_and_convert_tiktok_orders(rar_file: str, xls_file: str, sku_order_xls: str):
    global __current_pdf_file_path
    global __current_pdf_lines
    global __current_order
    sku_mapper = SkuMapper()
    sku_mapper.load_sku_map(sku_order_xls)
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
            __current_pdf_file_path = abs_path
            order = TikTokOrder()
            pdf_lines = parse_pdf(abs_path)
            __current_pdf_lines = pdf_lines
            order.parse(pdf_lines, sku_mapper)
            __current_order = order
            valid, cause = order.is_valid_order()
            if valid:
                logging.debug(f"add order {order.tiktok_order_id}")
                logging.debug(order)
                order_list.append(order)
                save_order_to_db(abs_path, order)
            else:
                logging.error(f"parse file {file} invalid order {cause}")
                logging.error(order)
                raise Exception(f"parse file {file} invalid order.")
    append_orders_to_xls(order_list, xls_file)
    logging.info(f"process file {rar_file} order count {len(order_list)}")
    print(f"process file {rar_file} order count {len(order_list)}")


def output_error_file(abs_file_path, e, err_file):
    with open(err_file, "w") as fp:
        fp.write(f"file: {abs_file_path}\n")
        fp.write("-------------\n")
        fp.write(f"exception: {str(e)}\n")
        fp.write("-------------\n")
        fp.write(f"pdf_path: {__current_pdf_file_path}\n")
        fp.write("-------------\n")
        for i in range(len(__current_pdf_lines)):
            fp.write(f">>> line[{i} {__current_pdf_lines[i]}\n")
        fp.write("-------------\n")
        fp.write(f"order: {str(__current_order)}\n")


def main():
    upload_dir = "./upload"
    while True:
        # read_sku_map()
        for file in os.listdir(upload_dir):
            if not file.endswith(".rar"):
                continue
            abs_file_path = os.path.join(upload_dir, file)
            # sku_order_xls
            sku_order_xls = file[: -4] + ".sku.xlsx"
            sku_order_xls = os.path.join(upload_dir, sku_order_xls)
            if not os.path.isfile(sku_order_xls):
                logging.info(f"sku_order_xls file {sku_order_xls} not exist.")
                continue
            # output xls file
            xls_file = file[: -4] + ".big_seller.xlsx"
            xls_file = os.path.join(upload_dir, xls_file)
            if os.path.isfile(xls_file):
                continue
            # output error file
            err_file = file[: -4] + ".error.txt"
            err_file = os.path.join(upload_dir, err_file)
            if os.path.isfile(err_file):
                continue
            logging.info(f"start parsing file {file}...")
            try:
                parse_and_convert_tiktok_orders(abs_file_path, xls_file, sku_order_xls)
            except Exception as e:
                logging.error(f"process file {file} failed", e)
                output_error_file(abs_file_path, e, err_file)
        time.sleep(10)


if __name__ == '__main__':
    log_config.fileConfig('./conf/logging.conf')
    main()
