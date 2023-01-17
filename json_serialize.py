#!/usr/bin/env python3
# -*- coding:utf-8 _*-
"""
@file: json_object
@author: jkguo
@create: 2022/4/4
"""
import copy
import json


class JsonSerializable(object):
    """
    可序列化对象
    """

    def to_dict(self) -> dict:
        d = copy.deepcopy(self.__dict__)
        for k in d.keys():
            if hasattr(d[k], "to_dict"):
                d[k] = d[k].to_dict()
            elif isinstance(d[k], list):
                arr = []
                for item in d[k]:
                    if hasattr(item, "to_dict"):
                        arr.append(item.to_dict())
                    else:
                        arr.append(item)
                d[k] = arr
            elif isinstance(d[k], tuple):
                arr = []
                for item in d[k]:
                    if hasattr(item, "to_dict"):
                        arr.append(item.to_dict())
                    else:
                        arr.append(item)
                d[k] = arr
            elif isinstance(d[k], dict):
                id = {}
                for ik in d[k].keys():
                    item = d[k][ik]
                    if hasattr(item, "to_dict"):
                        id[ik] = item.to_dict()
                    else:
                        id[ik] = item
                d[k] = id
        return d

    def to_json(self) -> str:
        return json.dumps(self.to_dict())

    def __repr__(self) -> str:
        return self.to_json()

    def from_dict(self, doc: dict):
        for k in self.__dict__.keys():
            if doc.get(k, None) is None:
                self.__dict__[k] = None
            elif hasattr(self.__dict__[k], "from_dict"):
                self.__dict__[k].from_dict(doc[k])
            else:
                self.__dict__[k] = doc[k]

    def from_json(self, json_str: str):
        self.from_dict(json.loads(json_str))
