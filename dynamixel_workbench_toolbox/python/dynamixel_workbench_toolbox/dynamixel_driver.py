#!/usr/bin/env python
# coding: UTF-8

import time

import dynamixel_sdk as dynSDK

import dynamixel_item as dyn_item
import dynamixel_tool as dyn_tool

MAX_DXL_SERIES_NUM = 3
MAX_HANDLER_NUM = 5

BYTE = 1
WORD = 2
DWORD = 4


# ct_item.ControlTableItem control_table; dynSDK.GroupSyncWrite _groupSyncWrite;
class SyncWriteHandler:
    def __init__(self):
        self.control_table = None
        self._groupSyncWrite = None


# ct_item.ControlTableItem control_table; dynSDK.GroupSyncRead _groupSyncRead;
class SyncReadHandler:
    def __init__(self):
        self.control_table = None
        self._groupSyncWrite = None


class DynamixelDriver:
    def __init__(self):
        self.tools = []
        self.syncWriteHandler = []
        self.syncReadHandler = []
        self.portHandler = None
        self.packetHandler = None
        self.packetHandler_1 = None
        self.packetHandler_2 = None

    def __del__(self):
        for i in range(0, self.tools_cnt):
            for j in range(0, self.tools[i].dxl_info_cnt):
                self.writeRegister(self.tools[i].dxl_info[j].id, "Torque_Enable", False)
        self.portHandler.closePort()

    def initDXLinfo(self):
        for x in self.tools:
            x.dxl_info = []

    def setTools(self, model_number, id):
        if len(self.tools) == 0:
            self.initDXLinfo()
            tool = dyn_tool.DynamixelTool()
            tool.addTool(model_number, id)
            self.tools.append(tool)
        elif self.tools[-1].dxl_info[0].model_name == self.findModelName(model_number):
            self.tools[-1].addDXL(model_number, id)
        else:
            tool = dyn_tool.DynamixelTool()
            tool.addTool(model_number, id)
            self.tools.append(tool)

    def init(self, device_name, baud_rate):
        return self.setPortHandler(device_name) and self.setBaudrate(baud_rate) and self.setPacketHandler()

    def setPortHandler(self, device_name):
        self.portHandler = dynSDK.PortHandler(device_name)
        return self.portHandler.openPort()

    def setPacketHandler(self, protocol_version=1.0):
        self.packetHandler_1 = dynSDK.PacketHandler(1.0)
        self.packetHandler_2 = dynSDK.PacketHandler(2.0)
        self.packetHandler = self.packetHandler_1 if protocol_version == 1.0 else self.packetHandler_2
        return True

    def setBaudrate(self, baud_rate):
        return self.portHandler.setBaudRate(baud_rate)

    def getProtocolVersion(self):
        return self.packetHandler.getProtocolVersion()

    def getBaudrate(self):
        return self.portHandler.getBaudRate()

    def getModelName(self, id):
        for x in self.tools:
            for y in x.dxl_info:
                if y.id == id:
                    return y.model_name

    def getModelNum(self, id):
        for x in self.tools:
            for y in x.dxl_info:
                if y.id == id:
                    return y.model_num

    def getcontrolItem(self, id):
        for x in self.tools:
            for y in x.dxl_info:
                if y.id == id:
                    return x.control_table

    def getTheNumberOfItem(self, id):
        for x in self.tools:
            for y in x.dxl_info:
                if y.id == id:
                    return len(x.control_table)

    def scan(self, _range):
        protocol_version = 2.0
        get_ids = []
        self.tools = []

        for dxl_id in range(1, _range + 1):
            ok, model_number, error = self.packetHandler_1.ping(self.portHandler, dxl_id, True)
            if ok == dynSDK.COMM_SUCCESS:
                get_ids.append(dxl_id)
                self.setTools(model_number, dxl_id)
                protocol_version = 1.0

        for dxl_id in range(1, _range + 1):
            ok, model_number, error = self.packetHandler_2.ping(self.portHandler, dxl_id, True)
            if ok == dynSDK.COMM_SUCCESS:
                get_ids.append(dxl_id)
                self.setTools(model_number, dxl_id)
                protocol_version = 2.0

        if len(get_ids) == 0 or not self.setPacketHandler(protocol_version):
            return False, len(get_ids), get_ids
        else:
            return True, len(get_ids), get_ids

    ###

    def ping(self, dxl_id):
        protocol_version = 1.0

        ok, model_number, error = self.packetHandler_1.ping(self.portHandler, dxl_id, True)
        if ok == dynSDK.COMM_SUCCESS:
            self.setTools(model_number, dxl_id)
            protocol_version = 1.0
        else:
            ok, model_number, error = self.packetHandler_2.ping(self.portHandler, dxl_id, True)
            if ok == dynSDK.COMM_SUCCESS:
                self.setTools(model_number, dxl_id)
                protocol_version = 2.0
            else:
                return False, 0

        if not self.setPacketHandler(protocol_version):
            return False, 0
        else:
            return True, model_number

    def reboot(self, dxl_id):
        if self.packetHandler.getProtocolVersion() == 1.0:
            return False

        comm_result, error = self.packetHandler.reboot(self.portHandler, dxl_id)
        time.sleep(2)

        return comm_result == dynSDK.COMM_SUCCESS and error != 0

    ##

    def reset(self, dxl_id):
        ok = False
        baud = 0
        new_id = 1

        if self.packetHandler.getProtocolVersion() == 1.0:
            # Reset Dynamixel except ID and Baudrate
            comm_result, error = self.packetHandler_1.factoryReset(self.portHandler, dxl_id, 0x00)
            time.sleep(2)

            if comm_result == dynSDK.COMM_SUCCESS:
                if error != 0:
                    return False

                for x in self.tools:
                    for y in x.dxl_info:
                        if y.id == id:
                            y.id = new_id

                model_name = self.getModelName(new_id)
                if model_name[:2] == "AX" or model_name == "MX-12W":
                    baud = 1000000
                else:
                    baud = 57600

                if not self.portHandler.setBaudRate(baud):
                    time.sleep(2)
                    return False
                else:
                    time.sleep(2)
                    if model_name == "MX-28-2" or \
                            model_name == "MX-64-2" or \
                            model_name == "MX-106-2" or \
                            model_name[:2] == "XL" or \
                            model_name[:2] == "XM" or \
                            model_name[:2] == "XH" or \
                            model_name[:3] == "PRO":

                        return self.setPacketHandler(1.0)
                    else:
                        return self.setPacketHandler(2.0)
            else:
                return False

        elif self.packetHandler.getProtocolVersion() == 2.0:
            # Reset Dynamixel except ID and Baudrate
            comm_result, error = self.packetHandler_2.factoryReset(self.portHandler, dxl_id, 0x00)
            time.sleep(2)

            if comm_result == dynSDK.COMM_SUCCESS:
                if error != 0:
                    return False

                for x in self.tools:
                    for y in x.dxl_info:
                        if y.id == id:
                            y.id = new_id

                model_name = self.getModelName(new_id)
                if model_name[:2] == "XL-320":
                    baud = 1000000
                else:
                    baud = 57600

                if not self.portHandler.setBaudRate(baud):
                    time.sleep(2)
                    return False
                else:
                    time.sleep(2)
                    return self.setPacketHandler(2.0)
            else:
                return False
        return False

    def writeRegister(self, dxl_id, item_name, data):
        error = 0
        dxl_comm_result = dynSDK.COMM_TX_FAIL

        cti = self.tools[self.getToolsFactor(dxl_id)].getControlItem(item_name)

        if cti.data_length == BYTE:
            dxl_comm_result, error = self.packetHandler.write1ByteTxRx(self.portHandler, dxl_id, cti.address, data)
        elif cti.data_length == WORD:
            dxl_comm_result, error = self.packetHandler.write2ByteTxRx(self.portHandler, dxl_id, cti.address, data)
        elif cti.data_length == DWORD:
            dxl_comm_result, error = self.packetHandler.write4ByteTxRx(self.portHandler, dxl_id, cti.address, data)

        return dxl_comm_result == dynSDK.COMM_SUCCESS and error != 0

    def readRegister(self, id, item_name):
        error = 0
        dxl_comm_result = dynSDK.COMM_TX_FAIL
        value = 0

        cti = self.tools[self.getToolsFactor(id)].getControlItem(item_name)
        if cti.data_length == BYTE:
            dxl_comm_result, value, error = self.packetHandler.read1ByteTxRx(self.portHandler, id, cti.address)
        elif cti.data_length == WORD:
            dxl_comm_result, value, error = self.packetHandler.read2ByteTxRx(self.portHandler, id, cti.address)
        elif cti.data_length == DWORD:
            dxl_comm_result, value, error = self.packetHandler.read4ByteTxRx(self.portHandler, id, cti.address)

        return dxl_comm_result == dynSDK.COMM_SUCCESS and error != 0

    def getToolsFactor(self, id):
        for i, x in enumerate(self.tools):
            for y in x.dxl_info:
                if y.id == id:
                    return i
        return -1

    def findModelName(self, model_number):
        if model_number == dyn_item.AX_12A:
            return "AX-12A"
        elif model_number == dyn_item.AX_12W:
            return "AX-12W"
        elif model_number == dyn_item.AX_18A:
            return "AX-18A"
        elif model_number == dyn_item.RX_10:
            return "RX-10"
        elif model_number == dyn_item.RX_24F:
            return "RX-24F"
        elif model_number == dyn_item.RX_28:
            return "RX-28"
        elif model_number == dyn_item.RX_64:
            return "RX-64"
        elif model_number == dyn_item.EX_106:
            return "EX-106"
        elif model_number == dyn_item.MX_12W:
            return "MX-12W"
        elif model_number == dyn_item.MX_28:
            return "MX-28"
        elif model_number == dyn_item.MX_28_2:
            return "MX-28-2"
        elif model_number == dyn_item.MX_64:
            return "MX-64"
        elif model_number == dyn_item.MX_64_2:
            return "MX-64-2"
        elif model_number == dyn_item.MX_106:
            return "MX-106"
        elif model_number == dyn_item.MX_106_2:
            return "MX-106-2"

    def addSyncWrite(self, item_name):
        swh = SyncWriteHandler()
        swh.control_table = self.tools[0].getControlItem(item_name)
        swh._groupSyncWrite = dynSDK.GroupSyncWrite(self.portHandler, self.packetHandler, swh.control_table.address,
                                                    swh.control_table.data_length)
        self.syncWriteHandler.append(swh)

    '''
    def syncWrite(self, item_name, data):
        dxl_addparam_result = False
        dxl_comm_result = dynSDK.COMM_TX_FAIL
        data_byte = []
        cnt = 0
        swh = SyncWriteHandler()
        for index in range(0, self.sync_write_handler_cnt):
            if (self.syncWriteHandler[index].control_table.item_name == item_name):
                swh = self.syncWriteHandler[index]
        for i in range(0, self.tools_cnt):
            for j in range(0, self.tools[i].dxl_info_cnt):
                data_byte[0] = DXL_LOBYTE(DXL_LOWORD(data[cnt]))
                data_byte[1] = DXL_HIBYTE(DXL_LOWORD(data[cnt]))
                data_byte[2] = DXL_LOBYTE(DXL_HIWORD(data[cnt]))
                data_byte[3] = DXL_HIBYTE(DXL_HIWORD(data[cnt]))

        dxl_addparam_result, data_byte = swh.groupSyncWrite.addParam(self.tools[i].dxl_info[j].id)
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

    def convertRadian2Value(self, dxl_id, radian):
        t = self.tools[self.getToolsFactor(dxl_id)]
        return self.convertValue2Radian(radian,
                                        t.getValueOfMaxRadianPosition(),
                                        t.getValueOfMinRadianPosition(),
                                        t.getMaxRadian(),
                                        t.getMinRadian())

    def convertValue2Radian(self, dxl_id, value):
        t = self.tools[self.getToolsFactor(dxl_id)]
        return self.convertValue2Radian(value,
                                        t.getValueOfMaxRadianPosition(),
                                        t.getValueOfMinRadianPosition(),
                                        t.getMaxRadian(),
                                        t.getMinRadian())

    def convertRadian2Value(self, radian, max_position, min_position, max_radian, min_radian):
        zero_position = (max_position + min_position) / 2
        if radian > 0:
            value = (radian * (max_position - zero_position) / max_radian) + zero_position
        elif radian < 0:
            value = (radian * (min_position - zero_position) / min_radian) + zero_position
        else:
            value = zero_position
        return value

    def convertValue2Radian(self, value, max_position, min_position, max_radian, min_radian):
        zero_position = (max_position + min_position) / 2
        if value > zero_position:
            radian = float(value - zero_position) * max_radian / float((max_position - zero_position))
        elif value < zero_position:
            radian = float(value - zero_position) * min_radian / float((min_position - zero_position))
        return radian

    def convertVelocity2Value(self, dxl_id, velocity):
        factor = self.getToolsFactor(dxl_id)
        value = velocity * self.tools[factor].getVelocityToValueRatio()
        return value

    def convertValue2Velocity(self, dxl_id, value):
        factor = self.getToolsFactor(dxl_id)
        velocity = value / self.tools[factor].getVelocityToValueRatio()
        return velocity

    def convertTorque2Value(self, dxl_id, torque):
        factor = self.getToolsFactor(dxl_id)
        value = torque * self.tools[factor].getTorqueToCurrentValueRatio()
        return value

    def convertValue2Torque(self, dxl_id, value):
        factor = self.getToolsFactor(dxl_id)
        torque = value / self.tools[factor].getTorqueToCurrentValueRatio()
        return torque
