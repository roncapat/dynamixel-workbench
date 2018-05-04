#!/usr/bin/env python
# coding: UTF-8


class ControlTableItem:
    def __init__(self, address, item_name, data_length):
        self.address = address
        self.item_name = item_name
        self.data_length = data_length
