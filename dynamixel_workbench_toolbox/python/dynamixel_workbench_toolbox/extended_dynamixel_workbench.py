from dynamixel_workbench_toolbox import *

# This Python porting of the original Dynamixel Workbench Toolbox from ROBOTIS
# was written by Patrick Roncagliolo and Marco Lapolla as part of a project
# developed at the DIBRIS BIOLab of the University of Genoa, Italy.

class ExtendedDynamixelWorkbench(DynamixelWorkbench):
    def readPresentPosition(self, dxl_id):
        return self.itemRead(dxl_id, "Present_Position")

    def torque(self, dxl_id, enable):
        return self._driver.writeRegister(dxl_id, "Torque_Enable", enable)

    def torqueAll(self, id_range, enable):
        res, count, ids = self.scan(id_range)
        if not res:
            return False
        else:
            for i in range(0, count):
                if self.torque(ids[i], enable) != dyn_sdk.COMM_SUCCESS:
                    return False
            return True

    def readPresentPosition(self, dxl_id):
        return self.itemRead(dxl_id, "Present_Position")

    def readPresentSpeed(self, id):
        return self.itemRead(id, "Present_Speed")

    def readPresentVoltage(self, id):
        return self.itemRead(id, "Present_Voltage")

    def readPresentTemperature(self, id):
        return self.itemRead(id, "Present_Temperature")

    def readAllPresentPosition(self, id_range):
        res, count, ids = self._driver.scan(id_range)
        return res, [self.readPresentPosition(ids[i]) for i in range(0, count) if res]

    def readAllPresentSpeed(self, range_):
	    speed_to_return = []
	    isOK, cont, ids = self.scan(range_)
	    if isOK == False:
		    return False, []
	    else:
		    for i in range(0, cont):
			    speed_to_return.append(self.readPresentSpeed(ids[i]))
		    return True, speed_to_return

    def readAllPresentVoltage(self, range_):
	    vol_to_return = []
	    isOK, cont, ids = self.scan(range_)
	    if isOK == False:
		    return False, []
	    else:
		    for i in range(0, cont):
			    vol_to_return.append(self.readPresentVoltage(ids[i]))
		    return True, vol_to_return

    def readAllPresentTemperature(self, range_):
	    temp_to_return = []
	    isOK, cont, ids = self.scan(range_)
	    if isOK == False:
		    return False, []
	    else:
		    for i in range(0, cont):
			    temp_to_return.append(self.readPresentTemperature(ids[i]))
		    return True, temp_to_return

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
            self.itemWrite("Alarm_LED", 127)
            self.itemWrite("Shutdown", 37)

    def setPositionControlMode(self, id):
        comm_result = False
        self._dxl = self._driver.getModelName(id)

        if self._driver.getProtocolVersion() == 1.0:
            if (self._dxl == "MX-28-2"
                    or self._dxl == "MX-64-2"
                    or self._dxl == "MX-106-2"
                    or self._dxl == "XL430"
                    or self._dxl[:2] == "XM"
                    or self._dxl[:2] == "XH"
                    or self._dxl[:3] == "PRO"):
                comm_result = self._driver.writeRegister(id, "Operating_Mode", X_SERIES_POSITION_CONTROL_MODE)
            elif self._dxl[:2] == "AX" or self._dxl[:2] == "RX":
                comm_result = self._driver.writeRegister(id, "CW_Angle_Limit", 0)
                comm_result = self._driver.writeRegister(id, "CCW_Angle_Limit", 1023)
            else:
                comm_result = self._driver.writeRegister(id, "CW_Angle_Limit", 0)
                comm_result = self._driver.writeRegister(id, "CCW_Angle_Limit", 4095)
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
            if (self._dxl == "MX-28-2"
                    or self._dxl == "MX-64-2"
                    or self._dxl == "MX-106-2"
                    or self._dxl == "XL430"
                    or self._dxl[:2] == "XM"
                    or self._dxl[:2] == "XH"
                    or self._dxl[:3] == "PRO"):
                comm_result = self._driver.writeRegister(id, "Operating_Mode", X_SERIES_VELOCITY_CONTROL_MODE)
            else:
                comm_result = self._driver.writeRegister(id, "CW_Angle_Limit", 0)
                comm_result = self._driver.writeRegister(id, "CCW_Angle_Limit", 0)
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
            comm_result = self._driver.writeRegister(id, "Operating_Mode", X_SERIES_CURRENT_BASED_POSITION_CONTROL_MODE)
        time.sleep(0.01)
        return comm_result
