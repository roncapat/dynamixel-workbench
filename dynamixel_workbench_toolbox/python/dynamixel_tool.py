#!/usr/bin/env python
#coding: UTF-8

import dynamixel_item as dyn_item
import control_table_item as ct_item

ITEM_ARRAY_SIZE = 60

class DXLInfo:
	def __init__(self, model_name, model_num, id):
		self._model_name = model_name
		self._model_num = int(model_num)
		self._id = int(id)

class DynamixelTool:
	def __init__(self):
		self._dxl_info_cnt = 0
		self._dxl_info = []

	
	def addTool(self, model, id):
		for i in range(0, len(self._dxl_info)):
			if(self._dxl_info[i] == id):
				return
		if type(model) == str:
			self._dxl_info.append(DXLInfo(model, self.setModelNum(model), id))
		elif type(model) == int:
			self._dxl_info.append(DXLInfo(self.setModelName(model), model, id))
		self.setControlTable(model)
		self._dxl_info_cnt = self._dxl_info_cnt + 1
	
	def addDXL(self, model, id):
		for i in range(0, len(self._dxl_info)):
			if(self._dxl_info[i]._id == id):
				return
		if type(model) == str:
			self._dxl_info.append(DXLInfo(model, self.setModelNum(model), id))
		elif type(model) == int:
			self._dxl_info.append(DXLInfo(self.setModelName(model), model, id))
		self.setControlTable(model)
		self._dxl_info_cnt = self._dxl_info_cnt + 1
	
	def setControlTable(self, model):
		if type(model) == str:
			name = str(model)
			self._model_info = dyn_item.ModelInfo()
			if (name == "AX-12A"):
				self._model_info.setAXItem()
				self._model_info.setAXInfo()
			elif (name == "AX-12W"):
				self._model_info.setAXItem()
				self._model_info.setAXInfo()
			elif (name == "AX-18A"):
				self._model_info.setAXItem()
				self._model_info.setAXInfo()
			elif (name == "RX-24F"):
				self._model_info.setRXItem()
				self._model_info.setRXInfo()
			elif (name == "RX-28"):
				self._model_info.setRXItem()
				self._model_info.setRXInfo()
			elif (name == "RX-64"):
				self._model_info.setRXItem()
				self._model_info.setRXInfo()
			elif (name == "EX-106"):
				self._model_info.setEXItem()
				self._model_info.setEXInfo()

			elif (name == "MX-12W"):
				self._model_info.setMXItem()
				self._model_info.setMXInfo()
			elif (name == "MX-28"):
				self._model_info.setMXItem()
				self._model_info.setMXInfo()
			elif (name == "MX-28-2"):
				self._model_info.setMX2Item()
				self._model_info.setMX2Info()
			elif (name == "MX-64"):
				self._model_info.setExtMXItem()
				self._model_info.setExtMXInfo()
			elif (name == "MX-64-2"):
				self._model_info.setExtMX2Info()
				self._model_info.setExtMX2Info()
			elif (name == "MX-106"):
				self._model_info.setExtMXItem()
				self._model_info.setExtMXInfo()
			elif (name == "MX-106-2"):
				self._model_info.setExtMX2Info()
				self._model_info.setExtMX2Info()
		elif type(model) == int:
			num = int(model)
			self._model_info = dyn_item.ModelInfo()
			self._model_info.getConrolTableItem(num)
			self._model_info.getModelInfo(num)

	def setModelNum(self, model):
		if type(model) != str:
			return
		name = str(model)
		if (name == "AX-12A"):
			return dyn_item.AX_12A
		elif (name == "AX-12W"):
			return dyn_item.AX_12W
		elif (name == "AX-18A"):
			return dyn_item.AX_18A
		elif (name == "RX-10"):
			return dyn_item.RX_10
		elif (name == "RX-24F"):
			return dyn_item.RX_24F
		elif (name == "RX-28"):
			return dyn_item.RX_28
		elif (name == "RX-64"):
			return dyn_item.RX_64
		elif (name == "EX-106"):
			return dyn_item.EX_106
		elif (name == "MX-12W"):
			return dyn_item.MX_12W
		elif (name == "MX-28"):
			return dyn_item.MX_28
		elif (name == "MX-28-2"):
			return dyn_item.MX_28_2
		elif (name == "MX-64"):
			return dyn_item.MX_64
		elif (name == "MX-64-2"):
			return dyn_item.MX_64_2
		elif (name == "MX-106"):
			return dyn_item.MX_106
		elif (name == "MX-106-2"):
			return dyn_item.MX_106_2

	def setModelName(self, model):
		if type(model) != int:
			return
		num = int(model)
		if (num == dyn_item.AX_12A):
    			return "AX-12A"
		elif (num == dyn_item.AX_12W):
			return "AX-12W"
		elif (num == dyn_item.AX_18A):
			return "AX-18A"
		elif (num == dyn_item.RX_10):
			return "RX-10"
		elif (num == dyn_item.RX_24F):
			return "RX-24F"
		elif (num == dyn_item.RX_28):
			return "RX-28"
		elif (num == dyn_item.RX_64):
			return "RX-64"
		elif (num == dyn_item.EX_106):
			return "EX-106"
		elif (num == dyn_item.MX_12W):
			return "MX-12W"
		elif (num == dyn_item.MX_28):
			return "MX-28"
		elif (num == dyn_item.MX_28_2):
			return "MX-28-2"
		elif (num == dyn_item.MX_64):
			return "MX-64"
		elif (num == dyn_item.MX_64_2):
			return "MX-64-2"
		elif (num == dyn_item.MX_106):
			return "MX-106"
		elif (num == dyn_item.MX_106_2):
			return "MX-106-2"

	def getVelocityToValueRatio(self):
		return self._model_info._velocity_to_value_ratio;

	def getTorqueToCurrentValueRatio(self):
		return self._model_info._torque_to_current_value_ratio;

	def getValueOfMinRadianPosition(self):
		return self._model_info._value_of_min_radian_position;

	def getValueOfMaxRadianPosition(self):
		return self._model_info._value_of_max_radian_position;

	def getValueOfZeroRadianPosition(self):
		return self._model_info._value_of_0_radian_position;

	def getMinRadian(self):
		return self._model_info._min_radian;

	def getMaxRadian(self):
		return self._model_info._max_radian;

	def getTheNumberOfItem(self):
		return self._model_info._the_number_of_item;

	def getControlItem(self, item_name):
		for i in range(0, self.getTheNumberOfItem()):
			if item_name == self._model_info._item[i]._item_name:
				return self._model_info._item[i]

	def getModelInfo(self):
		return self._model_info





