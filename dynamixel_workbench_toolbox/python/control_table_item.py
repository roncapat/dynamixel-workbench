#!/usr/bin/env python
#coding: UTF-8

class ControlTableItem:
	def __init__(self, address, item_name, data_length):
		self._address = int(address)
		self._item_name = item_name
		self._data_length = int(data_length)

