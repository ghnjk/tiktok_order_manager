#!/usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@file: utils
@author: jkguo
@create: 2023/1/15
"""
import logging
import os
import subprocess
import typing

from pdfminer.converter import PDFPageAggregator
from pdfminer.layout import *
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def execute_command(cmdline, work_dir=None, std_input_data=None, encoding="UTF-8"):
    """
    调用命令行指令，获取返回参数
    """
    if work_dir is not None:
        if os.name == "nt":
            child_proc = subprocess.Popen(
                args=cmdline,
                shell=True,
                cwd=work_dir,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:
            child_proc = subprocess.Popen(
                args=cmdline,
                shell=True,
                cwd=work_dir,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True,
            )
    else:
        if os.name == "nt":
            child_proc = subprocess.Popen(
                args=cmdline,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        else:
            child_proc = subprocess.Popen(
                args=cmdline,
                shell=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                close_fds=True,
            )
    stdout, stderr = child_proc.communicate(input=std_input_data)
    return_code = child_proc.wait()
    if os.name == 'nt':
        return return_code, stdout.decode("gbk"), stderr.decode("gbk")
    else:
        return return_code, stdout, stderr
    

def parse_pdf_fd(fp, password="") -> typing.List[str]:
    text_list = []
    parser = PDFParser(fp)
    # 创建pdf文档对象，存储文档结构
    document = PDFDocument(parser, password)

    # 创建一个pdf资源管理对象，存储共享资源
    res_mgr = PDFResourceManager()
    la_params = LAParams()

    # 创建一个device对象
    device = PDFPageAggregator(res_mgr, laparams=la_params)

    # 创建一个解释对象
    interpreter = PDFPageInterpreter(res_mgr, device)

    # 处理包含在文档中的每一页
    for page in PDFPage.create_pages(document):
        interpreter.process_page(page)
        layout = device.get_result()
        for x in layout:
            # 获取文本对象
            if isinstance(x, LTTextBox):
                text_list.append(x.get_text().strip())
    device.close()
    parser.close()
    return text_list


def parse_pdf(file_path: str) -> typing.List[str]:
    # 打开pdf文件
    with open(file_path, 'rb') as fp:
        return parse_pdf_fd(fp)


def extract_file(rar_file, tmp_dir):
    if os.name == 'nt':
        tmp_dir = tmp_dir.replace("./", "")
        cmd = f".\\libs\\7-Zip\\7z.exe e -o{tmp_dir} {rar_file}"
        # os.system(cmd)
    else:
        cmd = f"./libs/7zz e -o{tmp_dir} {rar_file}"
    ret, out, err = execute_command(
        cmd
    )
    logging.debug(f"extract_file {cmd} ret {ret} out {out} {err}")
    if ret != 0:
        raise Exception("extract_file failed.")
    else:
        logging.info(f"success extract_file {rar_file} to {tmp_dir}")
