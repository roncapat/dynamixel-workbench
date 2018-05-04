#!/usr/bin/env python
# coding: UTF-8

import time
from dynamixel_workbench_toolbox import *

X_SERIES_CURRENT_CONTROL_MODE = 0
X_SERIES_VELOCITY_CONTROL_MODE = 1
X_SERIES_POSITION_CONTROL_MODE = 3
X_SERIES_EXTENDED_POSITION_CONTROL_MODE = 4
X_SERIES_CURRENT_BASED_POSITION_CONTROL_MODE = 5
X_SERIES_VOLTAGE_CONTROL_MODE = 16

PRO_SERIES_TORQUE_CONTROL_MODE = 0
PRO_SERIES_VELOCITY_CONTROL_MODE = 1
PRO_SERIES_POSITION_CONTROL_MODE = 3
PRO_SERIES_EXTENDED_POSITION_CONTROL_MODE = 4

ALARM_LED_LEGEND = ALARM_SHUTDOWN_LEGEND = (
    "Instruction Error  ",
    "Overload Error     ",
    "CheckSum Error     ",
    "Range Error        ",
    "OverHeating Error  ",
    "Angle Limit Error  ",
    "Input Voltage Error")


class DynamixelWorkbench:
    def __init__(self):
        self._driver = DynamixelDriver()
        self._dxl = ""

    def begin(self, device_name, baud_rate):
        isOK = False
        isOK = self._driver.init(device_name, baud_rate)
        return isOK

    def scan(self, range_):
        isOK = False
        isOK, id_cnt, get_ids = self._driver.scan(range_)
        return isOK, id_cnt, get_ids

    def ping(self, id):
        isOK = False
        isOK, model_number = self._driver.ping(id)
        return isOK, model_number

    def reboot(self, id):
        isOK = False
        isOK = self._driver.reboot(id)
        return isOK

    def reset(self, id):
        isOK = False
        isOK = self._driver.reset(id)
        return isOK

    def setID(self, id, new_id):
        comm_result = False
        self.torque(id, False)
        comm_result = self._driver.writeRegister(id, "ID", new_id)
        time.sleep(1)
        return comm_result

    def setBaud(self, id, new_baud):
        comm_result = False
        self.torque(id, False)
        if self._driver.getProtocolVersion() == 1.0:
            if new_baud == 9600:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 207)
            elif new_baud == 19200:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 103)
            elif new_baud == 57600:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 34)
            elif new_baud == 115200:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 16)
            elif new_baud == 200000:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 9)
            elif new_baud == 250000:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 7)
            elif new_baud == 400000:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 4)
            elif new_baud == 500000:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 3)
            elif new_baud == 1000000:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 1)
            else:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 34)
        elif self._driver.getProtocolVersion() == 2.0:
            if new_baud == 9600:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 0)
            elif new_baud == 57600:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 1)
            elif new_baud == 115200:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 2)
            elif new_baud == 1000000:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 3)
            elif new_baud == 2000000:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 4)
            elif new_baud == 3000000:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 5)
            elif new_baud == 4000000:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 6)
            elif new_baud == 4500000:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 7)
            elif new_baud == 10500000:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 8)
            else:
                comm_result = self._driver.writeRegister(id, "Baud_Rate", 1)
        time.sleep(2)
        return comm_result

    def setPacketHandler(self, protocol_version):
        return self._driver.setPacketHandler(protocol_version)

    def getModelName(self, id):
        return self._driver.getModelName(id)

    def ledOn(self, id):
        comm_result = False
        if self.getModelName(id)[:3] == "PRO":
            comm_result = self._driver.writeRegister(id, "LED_RED", 1)
        else:
            comm_result = self._driver.writeRegister(id, "LED", 1)
        return comm_result

    def ledOff(self, id):
        comm_result = False
        if self.getModelName(id)[:3] == "PRO":
            comm_result = self._driver.writeRegister(id, "LED_RED", 0)
        else:
            comm_result = self._driver.writeRegister(id, "LED", 0)
        return comm_result

    def jointMode(self, id, vel, acc=0):
        comm_result = False
        self._dxl = self._driver.getModelName(id)
        comm_result = torque(id, False)
        comm_result = setPositionControlMode(id)
        comm_result = torque(id, True)
        if self._driver.getProtocolVersion() == 1.0:
            if (self._dxl == "MX-28-2" or self._dxl == "MX-64-2" or self._dxl == "MX-106-2" or
                    self._dxl == "XL430" or self._dxl[:2] == "XM" or self._dxl[:2] == "XH"):
                comm_result = self._driver.writeRegister(id, "Profile_Acceleration", acc)
                comm_result = self._driver.writeRegister(id, "Profile_Velocity", vel)
            else:
                comm_result = self._driver.writeRegister(id, "Moving_Speed", vel)
        elif self._driver.getProtocolVersion() == 2.0:
            if self._dxl == "XL-320" or self._dxl[:3] == "PRO", 3:
                comm_result = self._driver.writeRegister(id, "Moving_Speed", vel)
            else:
                comm_result = self._driver.writeRegister(id, "Profile_Acceleration", acc)
                comm_result = self._driver.writeRegister(id, "Profile_Velocity", vel)
        return comm_result

    def wheelMode(self, id, vel, acc):
        comm_result = False
        self._dxl = self._driver.getModelName(id)
        comm_result = torque(id, False)
        comm_result = setVelocityControlMode(id)
        comm_result = torque(id, True)
        if self._driver.getProtocolVersion() == 1.0:
            if (self._dxl == "MX-28-2" or self._dxl == "MX-64-2" or self._dxl == "MX-106-2" or
                    self._dxl == "XL430" or self._dxl[:2] == "XM" or self._dxl[:2] == "XH"):
                comm_result = self._driver.writeRegister(id, "Profile_Acceleration", acc)
                comm_result = self._driver.writeRegister(id, "Profile_Velocity", vel)
        elif self._driver.getProtocolVersion() == 2.0:
            if self._dxl == "XL-320" or self._dxl[:3] == "PRO", 3:
                comm_result = self._driver.writeRegister(id, "Moving_Speed", vel)
        return comm_result

    def currentMode(self, id, cur):
        comm_result = False
        self._dxl = self._driver.getModelName(id)
        comm_result = torque(id, False)
        comm_result = setCurrentControlMode(id)
        comm_result = torque(id, True)
        if self._dxl[:1] == "X" or self._dxl == "MX-64-2" or self._dxl == "MX-106-2":
            comm_result = self._driver.writeRegister(id, "Goal_Current", cur)
        return comm_result

    def goalPosition(self, id, goal):
        comm_result = False
        comm_result = self._driver.writeRegister(id, "Goal_Position", goal)
        return comm_result

    def goalSpeed(self, id, goal):
        comm_result = False
        self._dxl = self._driver.getModelName(id)
        if self._driver.getProtocolVersion() == 1.0:
            if (self._dxl == "MX-28-2" or self._dxl == "MX-64-2" or self._dxl == "MX-106-2" or
                    self._dxl == "XL430" or self._dxl[:2] == "XM" or self._dxl[:2] == "XH"):
                comm_result = self._driver.writeRegister(id, "Goal_Velocity", goal)
            else:
                if goal < 0:
                    goal = (-1) * goal
                    goal |= 1024
                comm_result = self._driver.writeRegister(id, "Moving_Speed", goal)
        elif self._driver.getProtocolVersion() == 2.0:
            if self._dxl != "XL-320":
                if goal < 0:
                    goal = (-1) * goal
                    goal |= 1024
                comm_result = self._driver.writeRegister(id, "Moving_Speed", goal)
            else:
                comm_result = self._driver.writeRegister(id, "Goal_Velocity", goal)
        return comm_result

    def itemWrite(self, id, item_name, value):
        comm_result = False
        comm_result = self._driver.writeRegister(id, item_name, value)
        return comm_result

    def itemRead(self, id, item_name):
        data = 0
        isOk = False
        isOk, data = self._driver.readRegister(id, item_name)
        if isOk:
            return data

    def readPresentPosition(self, id):
        return self.itemRead(id, "Present_Position")

    def torque(self, id, onoff):
        comm_result = False
        comm_result = self._driver.writeRegister(id, "Torque_Enable", onoff)
        return comm_result

    def torqueAll(self, range_, onoff):
        isOK, cont, ids = dw.scan(range_)
        if not isOK:
            return False
        else:
            for i in range(0, cont):
                if self.torque(ids[i], onoff) != dynSDK.COMM_SUCCESS:
                    return False
            return True

    def readAllPresentPosition(self, range_):
        pos_to_return = []
        isOK, cont, ids = dw.scan(range_)
        if not isOK:
            return False, []
        else:
            for i in range(0, cont):
                pos_to_return.append(dw.readPresentPosition(ids[i]))
            return True, pos_to_return

    def getAlarmShutdownStatus(self, id):
        dxl_alarm_shutdown = self.itemRead(id, "Shutdown")
        dxl_alarm_shutdown_bits = ((dxl_alarm_shutdown & 0b01000000) >> 6,
                                   (dxl_alarm_shutdown & 0b00100000) >> 5,
                                   (dxl_alarm_shutdown & 0b00010000) >> 4,
                                   (dxl_alarm_shutdown & 0b00001000) >> 3,
                                   (dxl_alarm_shutdown & 0b00000100) >> 2,
                                   (dxl_alarm_shutdown & 0b00000010) >> 1,
                                   (dxl_alarm_shutdown & 0b00000001))
        print("\nAlarm Shutdown:")
        for i in range(0, 7):
            print("%s : %s" % (ALARM_LED_LEGEND[i], bool(dxl_alarm_shutdown_bits[i])))

    def getLedAlarmStatus(self, id):
        dxl_led_alarm = self.itemRead(id, "Alarm_LED")
        dxl_led_alarm_bits = ((dxl_led_alarm & 0b01000000) >> 6,
                              (dxl_led_alarm & 0b00100000) >> 5,
                              (dxl_led_alarm & 0b00010000) >> 4,
                              (dxl_led_alarm & 0b00001000) >> 3,
                              (dxl_led_alarm & 0b00000100) >> 2,
                              (dxl_led_alarm & 0b00000010) >> 1,
                              (dxl_led_alarm & 0b00000001))
        print("\nLED Alarm:")
        for i in range(0, 7):
            print("%s : %s" % (ALARM_LED_LEGEND[i], bool(dxl_led_alarm_bits[i])))

    def setAlarms(self, _range):
        for i in range(0, _range):
            dw.itemWrite("Alarm_LED", 127)
            dw.itemWrite("Shutdown", 37)

    def convertRadian2Value(self, id, radian):
        return self._driver.convertRadian2Value(id, radian)

    def convertValue2Radian(self, id, value):
        return self._driver.convertValue2Radian(id, value)

    def convertRadian2Value(self, radian, max_position, min_position, max_radian, min_radian):
        return self._driver.convertRadian2Value(radian, max_position, min_position, max_radian, min_radian)

    def convertValue2Radian(self, value, max_position, min_position, max_radian, min_radian):
        return self._driver.convertValue2Radian(value, max_position, min_position, max_radian, min_radian)

    def convertVelocity2Value(self, id, velocity):
        return self._driver.convertVelocity2Value(id, velocity)

    def convertValue2Velocity(self, id, value):
        return self._driver.convertValue2Velocity(id, value)

    def convertTorque2Value(self, id, torque):
        return self._driver.convertTorque2Value(id, torque)

    def convertValue2Torque(self, id, value):
        return self._driver.convertValue2Torque(id, value)

    def setPositionControlMode(self, id):
        comm_result = False
        self._dxl = self._driver.getModelName(id)

        if self._driver.getProtocolVersion() == 1.0:
            if (
                    self._dxl == "MX-28-2" or self._dxl == "MX-64-2" or self._dxl == "MX-106-2" or self._dxl == "XL430" or self._dxl[
                                                                                                                           :2] == "XM" or self._dxl[
                                                                                                                                          :2] == "XH" or self._dxl[
                                                                                                                                                         :3] == "PRO"):
                comm_result = driver_.writeRegister(id, "Operating_Mode", X_SERIES_POSITION_CONTROL_MODE)
            elif self._dxl[:2] == "AX" or self._dxl[:2] == "RX":
                comm_result = driver_.writeRegister(id, "CW_Angle_Limit", 0)
                comm_result = driver_.writeRegister(id, "CCW_Angle_Limit", 1023)
            else:
                comm_result = driver_.writeRegister(id, "CW_Angle_Limit", 0)
                comm_result = driver_.writeRegister(id, "CCW_Angle_Limit", 4095)
        elif self._driver.getProtocolVersion() == 2.0:
            if self._dxl == "XL-320":
                comm_result = self._driver.writeRegister(id, "CW_Angle_Limit", 0)
                comm_result = self._driver.writeRegister(id, "CCW_Angle_Limit", 1023)
            else:
                comm_result = self._driver.writeRegister(id, "Operating_Mode", X_SERIES_POSITION_CONTROL_MODE)
        time.sleep(0.01)
        return comm_result

    def setVelocityControlMode(self, id):
        comm_result = False
        self._dxl = self._driver.getModelName(id)

        if self._driver.getProtocolVersion() == 1.0:
            if (
                    self._dxl == "MX-28-2" or self._dxl == "MX-64-2" or self._dxl == "MX-106-2" or self._dxl == "XL430" or self._dxl[
                                                                                                                           :2] == "XM" or self._dxl[
                                                                                                                                          :2] == "XH" or self._dxl[
                                                                                                                                                         :3] == "PRO"):
                comm_result = driver_.writeRegister(id, "Operating_Mode", X_SERIES_VELOCITY_CONTROL_MODE)
            else:
                comm_result = driver_.writeRegister(id, "CW_Angle_Limit", 0)
                comm_result = driver_.writeRegister(id, "CCW_Angle_Limit", 0)
        elif self._driver.getProtocolVersion() == 2.0:
            if self._dxl == "XL-320":
                comm_result = self._driver.writeRegister(id, "CW_Angle_Limit", 0)
                comm_result = self._driver.writeRegister(id, "CCW_Angle_Limit", 0)
            else:
                comm_result = self._driver.writeRegister(id, "Operating_Mode", X_SERIES_VELOCITY_CONTROL_MODE)
        time.sleep(0.01)
        return comm_result

    def setCurrentControlMode(self, id):
        comm_result = False
        self._dxl = self._driver.getModelName(id)
        if self._dxl[:1] == "X" or self._dxl == "MX-64-2" or self._dxl == "MX-106-2":
            comm_result = driver_.writeRegister(id, "Operating_Mode", X_SERIES_CURRENT_BASED_POSITION_CONTROL_MODE)
        time.sleep(0.01)
        return comm_result

    '''




bool DynamixelWorkbench::syncWrite(const char *item_name, int32_t* value)
{
  bool isOK = false;

  isOK =  driver_.syncWrite(item_name, value);

  return isOK;
}

bool DynamixelWorkbench::bulkWrite()
{
  bool isOK = false;

  isOK = driver_.bulkWrite();

  return isOK;
}

int32_t* DynamixelWorkbench::syncRead(const char *item_name)
{
  static int32_t data[16];
  if (driver_.syncRead(item_name, data))
    return data;
}

int32_t DynamixelWorkbench::bulkRead(uint8_t id, const char* item_name)
{
  static int32_t data;
  if (driver_.bulkRead(id, item_name, &data))
    return data;
}

void DynamixelWorkbench::addSyncWrite(const char* item_name)
{
  driver_.addSyncWrite(item_name);
}

void DynamixelWorkbench::addSyncRead(const char* item_name)
{
  driver_.addSyncRead(item_name);
}

void DynamixelWorkbench::initBulkWrite()
{
  driver_.initBulkWrite();
}

void DynamixelWorkbench::initBulkRead()
{
  driver_.initBulkRead();
}

bool DynamixelWorkbench::addBulkWriteParam(uint8_t id, const char *item_name, int32_t data)
{
  bool isOK = false;

  isOK = driver_.addBulkWriteParam(id, item_name, data);

  return isOK;
}

bool DynamixelWorkbench::addBulkReadParam(uint8_t id, const char *item_name)
{
  bool isOK = false;

  isOK = driver_.addBulkReadParam(id, item_name);

  return isOK;
}

bool DynamixelWorkbench::setBulkRead()
{
  bool isOK = false;

  isOK = driver_.sendBulkReadPacket();

  return isOK;
}

    '''


dw = DynamixelWorkbench()
dw.begin("/dev/ttyACM0", 1000000)
isOK, cont, ids = dw.scan(18)
dw.ping(1)
dw.ping(2)

dw.ledOff(13)

isOk, positions = dw.readAllPresentPosition(18)
print(positions)

dw.torqueAll(18, True)

dw.getLedAlarmStatus(16)
dw.getAlarmShutdownStatus(16)
