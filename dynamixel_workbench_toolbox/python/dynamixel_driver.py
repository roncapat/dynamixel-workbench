#!/usr/bin/env python
#coding: UTF-8

import sys, time
import control_table_item as ct_item
import dynamixel_item as dyn_item
import dynamixel_tool as dyn_tool
import dynamixel_classes as dynSDK
import dynamixel_functions as df

MAX_DXL_SERIES_NUM = 3
MAX_HANDLER_NUM = 5

BYTE = 1
WORD = 2
DWORD = 4

#ct_item.ControlTableItem _cti; dynSDK.GroupSyncWrite _groupSyncWrite;
class SyncWriteHandler:
	def setCTI(self, cti):
		self._cti = cti
	def setGroupSyncWrite(self, gsw):
		self._groupSyncWrite = gsw

#ct_item.ControlTableItem _cti; dynSDK.GroupSyncRead _groupSyncRead;
class SyncReadHandler:
	def setCTI(self, cti):
		self._cti = cti
	def setGroupSyncRead(self, gsr):
		self._groupSyncWrite = gsr

class DynamixelDriver:
	def __init__(self):
		self._tools_cnt = 0
		self._sync_write_handler_cnt = 0
		self._sync_read_handler_cnt = 0
		self._tools = []
		self._syncWriteHandler = []
		self._syncReadHandler = []

	def __del__(self):
		for i in range(0, self._tools_cnt):
			for j in range(0, self._tools[i]._dxl_info_cnt):
				self.writeRegister(self._tools[i]._dxl_info[j]._id, "Torque_Enable", False)
		self._portHandler.closePort()
	
	def initDXLinfo(self):
		for i in range(0, self._tools_cnt):
			self._tools[i]._dxl_info_cnt = 0;

	def setTools(self, model_number, id):
  		if self._tools_cnt == 0:
			self.initDXLinfo()
			self._tools.append(dyn_tool.DynamixelTool())
			self._tools[self._tools_cnt].addTool(model_number, id)
		else:
			if (self._tools[self._tools_cnt-1]._dxl_info[0]._model_name == self.findModelName(model_number)):
				self._tools[self._tools_cnt-1].addDXL(model_number, id)
				self._tools_cnt = self._tools_cnt - 1
			else:
				self._tools.append(addTool(model_number, id))
		self._tools_cnt = self._tools_cnt + 1

	def init(self, device_name, baud_rate):
  		if self.setPortHandler(device_name) == False:
			return False
		if self.setBaudrate(baud_rate) == False:
			return False
		if self.setPacketHandler() == False:
			return False
		return True

	def setPortHandler(self, device_name):
  		self._portHandler = dynSDK.PortHandler(device_name)
		if self._portHandler.openPort():
			return True
		else:
			return False

	def setPacketHandler(self, protocol_version = 1.0):
		self._packetHandler = dynSDK.PacketHandler(protocol_version)
		if (self._packetHandler.getProtocolVersion() == protocol_version):
	 		return True
		else:
			return False

	def setBaudrate(self, baud_rate):
		if(self._portHandler.setBaudRate(baud_rate)):
			return True
		else:
			return False

	def getProtocolVersion(self):
		return self._packetHandler.getProtocolVersion()

	def getBaudrate(self):
		return self._portHandler.getBaudRate()

	def getModelName(self, id):
		factor = self.getToolsFactor(id)
		for i in range(0, self._tools[factor]._dxl_info_cnt):
			if (self._tools[factor]._dxl_info[i]._id == id):
				return self._tools[factor]._dxl_info[i]._model_name

	def getModelNum(self, id):
		factor = self.getToolsFactor(id)
		for i in range(0, self._tools[factor]._dxl_info_cnt):
			if (self._tools[factor]._dxl_info[i]._id == id):
				return self._tools[factor]._dxl_info[i]._model_num


	def getTheNumberOfItem(self, id):
		factor = self.getToolsFactor(id)
		return self._tools[factor].getTheNumberOfItem()

	def scan(self, _range):
  		id = 0
		id_cnt = 0
		model_number = 0
		protocol_version = 1.0;
		get_ids = []
		self._tools_cnt = 0

		for id in range(1, _range+1):
			isOk, model_number, error = self._packetHandler.ping(self._portHandler, id, True)
			if(isOk == dynSDK.COMM_SUCCESS):
				get_ids.append(id)
				self.setTools(model_number, id)
				id_cnt = id_cnt + 1
				protocol_version = 1.0
		if(id_cnt == 0):
			for id in range(1, _range+1):
				isOk, model_number, error = self._packetHandler.ping(self._portHandler, id, True)
				if(isOk == dynSDK.COMM_SUCCESS):
					get_ids.append(id)
					self.setTools(model_number, id)
					id_cnt = id_cnt + 1
					protocol_version = 2.0
		if (id_cnt == 0):
			return False, 0, []
		elif (self.setPacketHandler(protocol_version) == False):
			return False, 0, []
		else:
			return True, id_cnt, get_ids


	def ping(self, id):
		model_number = 0
		protocol_version = 1.0
		isOk, model_number, error = self._packetHandler.ping(self._portHandler, id, True)
		if(isOk == dynSDK.COMM_SUCCESS):
			self.setTools(model_number, id)
			protocol_version = 1.0
		else:
			isOk, model_number, error = self._packetHandler.ping(self._portHandler, id, True)
			if(isOk == dynSDK.COMM_SUCCESS):
				self.setTools(model_number, id)
				protocol_version = 2.0
			else:
				return False, 0
		if (self.setPacketHandler(protocol_version) == False):
			return False, 0
		else:
			return True, model_number


	#TODO Check True / False
	def reboot(self, id):
		if (self._packetHandler.getProtocolVersion() == 1.0):
			return False
		else:
			error = 0
			comm_result = dynSDK.COMM_RX_FAIL

		comm_result, error = self._packetHandler.reboot(self._portHandler, id)
		time.sleep(2)

		if (comm_result == dynSDK.COMM_SUCCESS):
			if (error != 0):
				return True
			else:
				return False
		else:
			return False


	def reset(self, id):
		error = 0
		comm_result = dynSDK.COMM_RX_FAIL
		isOK = False
		baud = 0
		new_id = 1

		if (self._packetHandler.getProtocolVersion() == 1.0):
			#Reset Dynamixel except ID and Baudrate
			comm_result, error = self._packetHandler.factoryReset(self._portHandler, id, 0x00)
			time.sleep(2)
			
			if (comm_result == COMM_SUCCESS):
				if (error != 0):
					return False
				factor = self.getToolsFactor(id)
				
				for i in range(0, self._tools[factor]._dxl_info_cnt):
					if (self._tools[factor]._dxl_info[i]._id == id):
						self._tools[factor]._dxl_info[i]._id = new_id

				model_name = self.getModelName(new_id)
				if (model_name[:2] == "AX" or model_name == "MX-12W"):
					baud = 1000000
				else:
					baud = 57600
				if (self._portHandler.setBaudRate(baud) == false):
					time.sleep(2)
					return False
				else:
					time.sleep(2)
					isOK = self.setPacketHandler(1.0)

					if (isOK):
					  return True;
					else:
					  return False;
			else:
				return False

		elif (self._packetHandler.getProtocolVersion() == 2.0):
			comm_result, error = self._packetHandler.factoryReset(self._portHandler, id, 0xff)
			time.sleep(2)
			if (comm_result == dynSDK.COMM_SUCCESS):
				if error != 0:
					return False

				factor = self.getToolsFactor(id)

				for i in range(0, self._tools[factor]._dxl_info_cnt):
						if (self._tools[factor]._dxl_info[i]._id == id):
							self._tools[factor]._dxl_info[i]._id = new_id

				if (self.getModelName(new_id) == "XL-320"):
					baud = 1000000
				else:
					baud = 57600
				
				if (self._portHandler.setBaudRate(baud) == false):
					time.sleep(2)
					return False
				else:
					time.sleep(2)
			
					isOK = self.setPacketHandler(2.0)
					if (isOK):
						return True
					else:
						return False
			else:
				return False
		else:
			return False

	def writeRegister(self, id, item_name, data):
		error = 0
		dxl_comm_result = dynSDK.COMM_TX_FAIL

		cti = self._tools[self.getToolsFactor(id)].getControlItem(item_name)

		if (cti._data_length == BYTE):
			dxl_comm_result, error = self._packetHandler.write1ByteTxRx(self._portHandler, id, cti._address, int(data))
		elif (cti._data_length == WORD):
			dxl_comm_result, error = self._packetHandler.write2ByteTxRx(self._portHandler, id, cti._address, int(data))
		elif (cti._data_length == DWORD):
			dxl_comm_result, error = self._packetHandler.write4ByteTxRx(self._portHandler, id, cti._address, int(data))
		time.sleep(0.01)
		if (dxl_comm_result == dynSDK.COMM_SUCCESS):
			if (error != 0):
				return True
			else:
				return False
		else:
				return False
		
		return True

	def readRegister(self, id, item_name):
		error = 0
		dxl_comm_result = dynSDK.COMM_TX_FAIL
		value = 0

		cti = self._tools[self.getToolsFactor(id)].getControlItem(item_name)
		if (cti._data_length == BYTE):
			dxl_comm_result, value, error = self._packetHandler.read1ByteTxRx(self._portHandler, id, cti._address)
		elif (cti._data_length == WORD):
			dxl_comm_result, value, error = self._packetHandler.read2ByteTxRx(self._portHandler, id, cti._address)
		elif (cti._data_length == DWORD):
			dxl_comm_result, value, error = self._packetHandler.read4ByteTxRx(self._portHandler, id, cti._address)

		time.sleep(0.01)
		if (dxl_comm_result == dynSDK.COMM_SUCCESS):
			if (error != 0):
				return False, 0
			return True, value
		else:
				return False, 0

	def getToolsFactor(self, id):
		for i in range(0, self._tools_cnt):
			for j in range(0, self._tools[i]._dxl_info_cnt):
				if (self._tools[i]._dxl_info[j]._id == id):
					return i
		return -1

	def findModelName(self, model_number):
		if type(model_number) != int:
			return
		num = int(model_number)
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

	
	def addSyncWrite(self, item_name):
		cti = self._tools[0].getControlItem(item_name);
		swh = SyncWriteHandler()
		swh.setCTI(cti)
		gsw = df.GroupSyncWrite(self._portHandler, self._packetHandler, cti._address, cti._data_length)
		swh.setGroupSyncWrite(gsw)
		self._syncWriteHandler.append(swh)

		self._sync_write_handler_cnt = self._sync_write_handler_cnt + 1

	'''
	def syncWrite(self, item_name, data):
		dxl_addparam_result = False
		dxl_comm_result = dynSDK.COMM_TX_FAIL
		data_byte = []
		cnt = 0
		swh = SyncWriteHandler()
		for index in range(0, self._sync_write_handler_cnt):
			if (self._syncWriteHandler[index]._cti._item_name == item_name):
				swh = self._syncWriteHandler[index]
		for i in range(0, self._tools_cnt):
			for j in range(0, self._tools[i]._dxl_info_cnt):
				data_byte[0] = DXL_LOBYTE(DXL_LOWORD(data[cnt]))
				data_byte[1] = DXL_HIBYTE(DXL_LOWORD(data[cnt]))
				data_byte[2] = DXL_LOBYTE(DXL_HIWORD(data[cnt]))
				data_byte[3] = DXL_HIBYTE(DXL_HIWORD(data[cnt]))

		dxl_addparam_result, data_byte = swh.groupSyncWrite.addParam(self._tools[i]._dxl_info[j].id)
		if (dxl_addparam_result == False):
			return False

		cnt++;
		}
		}

		dxl_comm_result = swh.groupSyncWrite->txPacket();
		if (dxl_comm_result != COMM_SUCCESS)
		{
		return false;
		}
		swh.groupSyncWrite->clearParam();
		return true;
		}

		void DynamixelDriver::addSyncRead(const char *item_name)
		{
		ControlTableItem *cti;
		cti = tools_[0].getControlItem(item_name);

		syncReadHandler_[sync_read_handler_cnt_].cti = cti;

		syncReadHandler_[sync_read_handler_cnt_++].groupSyncRead = new dynamixel::GroupSyncRead(portHandler_,
		packetHandler_,
		cti->address,
		cti->data_length);

	bool DynamixelDriver::syncRead(const char *item_name, int32_t *data)
	{
	int dxl_comm_result = COMM_RX_FAIL;
	bool dxl_addparam_result = false;
	bool dxl_getdata_result = false;

	int index = 0;

	SyncReadHandler srh;

	for (int index = 0; index < sync_read_handler_cnt_; index++)
	{
	if (!strncmp(syncReadHandler_[index].cti->item_name, item_name, strlen(item_name)))
	{
	srh = syncReadHandler_[index];
	}
	}

	for (int i = 0; i < tools_cnt_; i++)
	{
	for (int j = 0; j < tools_[i].dxl_info_cnt_; j++)
	{
	dxl_addparam_result = srh.groupSyncRead->addParam(tools_[i].dxl_info_[j].id);
	if (dxl_addparam_result != true)
	return false;
	}
	}

	dxl_comm_result = srh.groupSyncRead->txRxPacket();
	if (dxl_comm_result != COMM_SUCCESS)
	{
	return false;
	}

	for (int i = 0; i < tools_cnt_; i++)
	{
	for (int j = 0; j < tools_[i].dxl_info_cnt_; j++)
	{
	uint8_t id = tools_[i].dxl_info_[j].id;

	dxl_getdata_result = srh.groupSyncRead->isAvailable(id, srh.cti->address, srh.cti->data_length);
	if (dxl_getdata_result)
	{
	data[index++] = srh.groupSyncRead->getData(id, srh.cti->address, srh.cti->data_length);
	}
	else
	{
	return false;
	}
	}
	}

	srh.groupSyncRead->clearParam();

	return true;
	}

	void DynamixelDriver::initBulkWrite()
	{
	groupBulkWrite_ = new dynamixel::GroupBulkWrite(portHandler_, packetHandler_);
	}

	bool DynamixelDriver::addBulkWriteParam(uint8_t id, const char *item_name, int32_t data)
	{
	bool dxl_addparam_result = false;
	uint8_t data_byte[4] = {0, };

	ControlTableItem *cti;
	cti = tools_[getToolsFactor(id)].getControlItem(item_name);

	data_byte[0] = DXL_LOBYTE(DXL_LOWORD(data));
	data_byte[1] = DXL_HIBYTE(DXL_LOWORD(data));
	data_byte[2] = DXL_LOBYTE(DXL_HIWORD(data));
	data_byte[3] = DXL_HIBYTE(DXL_HIWORD(data));

	dxl_addparam_result = groupBulkWrite_->addParam(id, cti->address, cti->data_length, data_byte);
	if (dxl_addparam_result != true)
	{
	return false;
	}

	return true;
	}

	bool DynamixelDriver::bulkWrite()
	{
	int dxl_comm_result = COMM_TX_FAIL;

	dxl_comm_result = groupBulkWrite_->txPacket();
	if (dxl_comm_result != COMM_SUCCESS)
	{
	return false;
	}

	groupBulkWrite_->clearParam();

	return true;
	}

	void DynamixelDriver::initBulkRead()
	{
	groupBulkRead_ = new dynamixel::GroupBulkRead(portHandler_, packetHandler_);
	}

	bool DynamixelDriver::addBulkReadParam(uint8_t id, const char *item_name)
	{
	bool dxl_addparam_result = false;

	ControlTableItem *cti;
	cti = tools_[getToolsFactor(id)].getControlItem(item_name);

	dxl_addparam_result = groupBulkRead_->addParam(id, cti->address, cti->data_length);
	if (dxl_addparam_result != true)
	{
	return false;
	}

	return true;
	}

	bool DynamixelDriver::sendBulkReadPacket()
	{
	int dxl_comm_result = COMM_RX_FAIL;

	dxl_comm_result = groupBulkRead_->txRxPacket();
	if (dxl_comm_result != COMM_SUCCESS)
	{
	return false;
	}

	return true;
	}

	bool DynamixelDriver::bulkRead(uint8_t id, const char *item_name, int32_t *data)
	{
	bool dxl_getdata_result = false;
	ControlTableItem *cti;
	cti = tools_[getToolsFactor(id)].getControlItem(item_name);

	dxl_getdata_result = groupBulkRead_->isAvailable(id, cti->address, cti->data_length);
	if (dxl_getdata_result != true)
	{
	return false;
	}

	*data = groupBulkRead_->getData(id, cti->address, cti->data_length);

	return true;
	}
	'''
	
	def convertRadian2Value(self, id, radian):
		value = 0;
		factor = self.getToolsFactor(id)
		if (radian > 0):
		  value = (radian * (self._tools[factor].getValueOfMaxRadianPosition() - self._tools[factor].getValueOfZeroRadianPosition()) / self._tools[factor].getMaxRadian()) + self._tools[factor].getValueOfZeroRadianPosition()
		elif (radian < 0):
			value = (radian * (self._tools[factor].getValueOfMinRadianPosition() - self._tools[factor].getValueOfZeroRadianPosition()) / self._tools[factor].getMinRadian()) + self._tools[factor].getValueOfZeroRadianPosition()
		else:
			value = self._tools[factor].getValueOfZeroRadianPosition()  
  		return value

	def convertValue2Radian(self, id, value):
		radian = 0.0
		factor = self.getToolsFactor(id)

		if (value > self.tools[factor].getValueOfZeroRadianPosition()):
			radian = float((value - self._tools[factor].getValueOfZeroRadianPosition())) * self._tools[factor].getMaxRadian() / float((self._tools[factor].getValueOfMaxRadianPosition() - self._tools[factor].getValueOfZeroRadianPosition()))
		elif (value < tools_[factor].getValueOfZeroRadianPosition()):
			radian = float((value - self._tools[factor].getValueOfZeroRadianPosition())) * self._tools[factor].getMinRadian() / float((self._tools[factor].getValueOfMinRadianPosition() - self._tools[factor].getValueOfZeroRadianPosition()))
  		return radiant


	def convertRadian2Value(self, radian, max_position, min_position, max_radian, min_radian):
		value = 0
		zero_position = (max_position + min_position)/2
		if (radian > 0):
			value = (radian * (max_position - zero_position) / max_radian) + zero_position
		elif (radian < 0):
			value = (radian * (min_position - zero_position) / min_radian) + zero_position
		else:
			value = zero_position
		return value

	def convertValue2Radian(self, value, max_position, min_position, max_radian, min_radian):
		radian = 0.0
		zero_position = (max_position + min_position)/2
		if (value > zero_position):
			radian = float(value - zero_position) * max_radian / float((max_position - zero_position))
		elif (value < zero_position):
			radian = float(value - zero_position) * min_radian / float((min_position - zero_position))
		return radian

	def convertVelocity2Value(self, id, velocity):
		value = 0
		factor = getToolsFactor(id)
		value = velocity * self._tools[factor].getVelocityToValueRatio()
		return value

	def convertValue2Velocity(self, id, value):
		velocity = 0
		factor = getToolsFactor(id)
		velocity = value / self._tools[factor].getVelocityToValueRatio()
		return velocity

	def convertTorque2Value(self, id, torque):
		value = 0;
		factor = getToolsFactor(id)
		value = torque * self._tools[factor].getTorqueToCurrentValueRatio()
		return value

	def convertValue2Torque(self, id, value):
		torque = 0.0
		factor = getToolsFactor(id)
		torque = value / self._tools[factor].getTorqueToCurrentValueRatio()
		return torque

