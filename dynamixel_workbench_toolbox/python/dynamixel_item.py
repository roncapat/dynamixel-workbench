#!/usr/bin/env python
#coding: UTF-8

import control_table_item as ct_item

# Type of Servo-Motors
AX_12A     = 12
AX_12W     = 300
AX_18A     = 18
RX_10      = 10
RX_24F     = 24
RX_28      = 28
RX_64      = 64
EX_106     = 107
MX_12W     = 360
MX_28      = 29
MX_28_2    = 30
MX_64      = 310
MX_64_2    = 311
MX_106     = 320
MX_106_2   = 321
XL_320     = 350
XL430_W250 = 1060
XM430_W210 = 1030
XM430_W350 = 1020
XM540_W150 = 1130
XM540_W270 = 1120
XH430_V210 = 1050
XH430_V350 = 1040
XH430_W210 = 1010
XH430_W350 = 1000
PRO_L42_10_S300_R  = 35072
PRO_L54_30_S400_R  = 37928
PRO_L54_30_S500_R  = 37896
PRO_L54_50_S290_R  = 38176
PRO_L54_50_S500_R  = 38152
PRO_M42_10_S260_R  = 43288
PRO_M54_40_S250_R  = 46096
PRO_M54_60_S250_R  = 46352
PRO_H42_20_S300_R  = 51200
PRO_H54_100_S500_R = 53768
PRO_H54_200_S500_R = 54024

# Control table address EEPROM
ADDR_AX_MODEL_NUMBER       				= 0			#2 bytes
ADDR_AX_FIRMWARE_VERSION   				= 2
ADDR_AX_ID			       				= 3			#DON'T TOUCH!!!!!
ADDR_AX_BAUDRATE						= 4
ADDR_AX_RETURN_DELAY					= 5
ADDR_AX_CLOCKWISE_ANGLE_LIMIT 			= 6 		#2 BYTES
ADDR_AX_COUNTER_CLOCKWISE_ANGLE_LIMIT 	= 8 		#2 BYTES
ADDR_AX_MAX_TEMPERATURE					= 11
ADDR_AX_MIN_VOLTAGE						= 12
ADDR_AX_MAX_VOLTAGE						= 13
ADDR_AX_MAX_TORQUE						= 14 		#2 BYTES
ADDR_AX_STATUS_RETURN_LEVEL				= 16		#QUANDO ASPETTARSI PACCHETTO DI RITORNO
ADDR_AX_LED_ALARM						= 17
ADDR_AX_ALARM_SHUTDOWN					= 18

# Control table address RAM
ADDR_AX_TORQUE_ENABLE       			= 24
ADDR_AX_LED								= 25
ADDR_AX_CLOCKWISE_MARGIN				= 26
ADDR_AX_COUNTER_CLOCKWISE_MARGIN		= 27
ADDR_AX_CLOCKWISE_SLOPE					= 28
ADDR_AX_COUNTER_CLOCKWISE_SLOPE			= 29
ADDR_AX_GOAL_POSITION					= 30 		#2 BYTES
ADDR_AX_MOVING_SPEED 					= 32 		#2 BYTES
ADDR_AX_TORQUE_LIMIT					= 34		#2 BYTES
ADDR_AX_PRESENT_POSITION				= 36		#2 BYTES
ADDR_AX_PRESENT_SPEED					= 38		#2 BYTES
ADDR_AX_PRESENT_LOAD					= 40		#2 BYTES
ADDR_AX_PRESENT_VOLTAGE					= 42
ADDR_AX_PRESENT_TEMPERATURE				= 43
ADDR_AX_REGISTERED						= 44
ADDR_AX_MOVING							= 46
ADDR_AX_LOCK							= 47
ADDR_AX_PUNCH							= 48		 #2 BYTES

# Name of Motors
MOTOR_SHOULDER_Y_RIGHT					= 1
MOTOR_SHOULDER_Y_LEFT					= 2
MOTOR_SHOULDER_X_RIGHT					= 3
MOTOR_SHOULDER_X_LEFT					= 4
MOTOR_ELBOW_RIGHT						= 5
MOTOR_ELBOW_LEFT						= 6
MOTOR_HIP_Z_RIGHT						= 7
MOTOR_HIP_Z_LEFT						= 8
MOTOR_HIP_X_RIGHT						= 9
MOTOR_HIP_X_LEFT						= 10
MOTOR_HIP_Y_RIGHT						= 11
MOTOR_HIP_Y_LEFT						= 12
MOTOR_KNEE_RIGHT						= 13
MOTOR_KNEE_LEFT							= 14
MOTOR_ANKLE_Y_RIGHT						= 15
MOTOR_ANKLE_Y_LEFT						= 16
MOTOR_ANKLE_X_RIGHT						= 17
MOTOR_ANKLE_X_LEFT						= 18

# Chains
CHAIN_A 								= [3, 5]
CHAIN_B 								= [4, 6]
CHAIN_C 								= [1, 7, 9, 11, 13, 15, 17]
CHAIN_D 								= [2, 8, 10, 12, 14, 16, 18]

# Sections
ARM_RIGHT 								= [1, 3, 5]
ARM_LEFT 								= [2, 4, 6]
LEG_RIGHT 								= [7, 9, 11, 13, 15, 17]
LEG_LEFT 								= [8, 10, 12, 14, 16, 18]

# Values
ON										= 1
OFF										= 0

# Length
BYTE									= 1
WORD									= 2

# AX Model Value
AX_VELOCITY_TO_VALUE_RATIO         	= 86.03		# AX series don't support exact speed in wheel mode.
AX_VALUE_OF_MIN_RADIAN_POSITIION  	= 0
AX_VALUE_OF_0_RADIAN_POSITION      	= 512
AX_VALUE_OF_MAX_RADIAN_POSITION    	= 1023
AX_MIN_RADIAN                      	= -2.61799
AX_MAX_RADIAN                      	=  2.61799

class ModelInfo:
	def __init__(self):
		self._item = []
		self._the_number_of_item = 0
	
	def setAXItem(self):
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MODEL_NUMBER, "Model_Number", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_FIRMWARE_VERSION, "Firmware_Version", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_ID,	"ID", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_BAUDRATE, "Baud_Rate", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_RETURN_DELAY, "Return_Delay_Time", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_ANGLE_LIMIT, "CW_Angle_Limit" , WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_ANGLE_LIMIT,"CCW_Angle_Limit", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_TEMPERATURE, "Temperature_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MIN_VOLTAGE, "Min_Voltage_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_VOLTAGE, "Max_Voltage_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_TORQUE, "Max_Torque", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_STATUS_RETURN_LEVEL, "Status_Return_Level", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LED_ALARM, "Alarm_LED", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_ALARM_SHUTDOWN, "Shutdown", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_TORQUE_ENABLE, "Torque_Enable", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LED, "LED", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_MARGIN, "CW_Compliance_Margin", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_MARGIN, "CCW_Compliance_Margin", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_SLOPE, "CW_Compliance_Slope", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_SLOPE, "CCW_Compliance_Slope", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_GOAL_POSITION, "Goal_Position", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MOVING_SPEED, "Moving_Speed", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_TORQUE_LIMIT, "Torque_Limit", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_POSITION, "Present_Position", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_SPEED, "Present_Speed", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_LOAD, "Present_Load", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_VOLTAGE, "Present_Voltage", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_TEMPERATURE, "Present_Temperature", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_REGISTERED, "Registered", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MOVING, "Moving", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LOCK, "Lock", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PUNCH, "Punch", WORD))
		self._the_number_of_item = 32

	def setAXInfo(self):
		self._velocity_to_value_ratio = float(AX_VELOCITY_TO_VALUE_RATIO)

		self._value_of_min_radian_position = int(AX_VALUE_OF_MIN_RADIAN_POSITIION)
		self._value_of_0_radian_position = int(AX_VALUE_OF_0_RADIAN_POSITION)
		self._value_of_max_radian_position = int(AX_VALUE_OF_MAX_RADIAN_POSITION)

		self._min_radian = float(AX_MIN_RADIAN)
		self._max_radian = float(AX_MAX_RADIAN)

	def setRXItem(self):
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MODEL_NUMBER, "Model_Number", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_FIRMWARE_VERSION, "Firmware_Version", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_ID,	"ID", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_BAUDRATE, "Baud_Rate", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_RETURN_DELAY, "Return_Delay_Time", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_ANGLE_LIMIT, "CW_Angle_Limit" , WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_ANGLE_LIMIT,"CCW_Angle_Limit", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_TEMPERATURE, "Temperature_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MIN_VOLTAGE, "Min_Voltage_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_VOLTAGE, "Max_Voltage_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_TORQUE, "Max_Torque", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_STATUS_RETURN_LEVEL, "Status_Return_Level", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LED_ALARM, "Alarm_LED", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_ALARM_SHUTDOWN, "Shutdown", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_TORQUE_ENABLE, "Torque_Enable", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LED, "LED", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_MARGIN, "CW_Compliance_Margin", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_MARGIN, "CCW_Compliance_Margin", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_SLOPE, "CW_Compliance_Slope", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_SLOPE, "CCW_Compliance_Slope", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_GOAL_POSITION, "Goal_Position", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MOVING_SPEED, "Moving_Speed", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_TORQUE_LIMIT, "Torque_Limit", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_POSITION, "Present_Position", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_SPEED, "Present_Speed", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_LOAD, "Present_Load", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_VOLTAGE, "Present_Voltage", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_TEMPERATURE, "Present_Temperature", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_REGISTERED, "Registered", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MOVING, "Moving", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LOCK, "Lock", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PUNCH, "Punch", WORD))
		self._the_number_of_item = 32

	def setRXInfo(self):
		self._velocity_to_value_ratio = float(86.03)

		self._value_of_min_radian_position = int(0)
		self._value_of_0_radian_position = int(512)
		self._value_of_max_radian_position = int(1023)

		self._min_radian = float(-2.61799)
		self._max_radian = float(2.61799)

	def setEXItem(self):
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MODEL_NUMBER, "Model_Number", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_FIRMWARE_VERSION, "Firmware_Version", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_ID,	"ID", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_BAUDRATE, "Baud_Rate", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_RETURN_DELAY, "Return_Delay_Time", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_ANGLE_LIMIT, "CW_Angle_Limit" , WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_ANGLE_LIMIT,"CCW_Angle_Limit", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_TEMPERATURE, "Temperature_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MIN_VOLTAGE, "Min_Voltage_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_VOLTAGE, "Max_Voltage_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_TORQUE, "Max_Torque", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_STATUS_RETURN_LEVEL, "Status_Return_Level", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LED_ALARM, "Alarm_LED", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_ALARM_SHUTDOWN, "Shutdown", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_TORQUE_ENABLE, "Torque_Enable", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LED, "LED", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_MARGIN, "CW_Compliance_Margin", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_MARGIN, "CCW_Compliance_Margin", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_SLOPE, "CW_Compliance_Slope", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_SLOPE, "CCW_Compliance_Slope", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_GOAL_POSITION, "Goal_Position", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MOVING_SPEED, "Moving_Speed", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_TORQUE_LIMIT, "Torque_Limit", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_POSITION, "Present_Position", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_SPEED, "Present_Speed", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_LOAD, "Present_Load", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_VOLTAGE, "Present_Voltage", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_TEMPERATURE, "Present_Temperature", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_REGISTERED, "Registered", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MOVING, "Moving", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LOCK, "Lock", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PUNCH, "Punch", WORD))
		self._item.append(ct_item.ControlTableItem(56, "Punch", WORD))
		self._the_number_of_item = 33

	def setEXInfo(self):
		self._velocity_to_value_ratio = float(86.03)

		self._value_of_min_radian_position = int(0)
		self._value_of_0_radian_position = int(2048)
		self._value_of_max_radian_position = int(4095)

		self._min_radian = float(-2.18969008)
		self._max_radian = float(2.18969008)

	def setMXItem(self):
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MODEL_NUMBER, "Model_Number", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_FIRMWARE_VERSION, "Firmware_Version", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_ID,	"ID", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_BAUDRATE, "Baud_Rate", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_RETURN_DELAY, "Return_Delay_Time", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_ANGLE_LIMIT, "CW_Angle_Limit" , WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_ANGLE_LIMIT,"CCW_Angle_Limit", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_TEMPERATURE, "Temperature_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MIN_VOLTAGE, "Min_Voltage_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_VOLTAGE, "Max_Voltage_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_TORQUE, "Max_Torque", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_STATUS_RETURN_LEVEL, "Status_Return_Level", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LED_ALARM, "Alarm_LED", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_ALARM_SHUTDOWN, "Shutdown", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_TORQUE_ENABLE, "Torque_Enable", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LED, "LED", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_MARGIN, "CW_Compliance_Margin", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_MARGIN, "CCW_Compliance_Margin", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_SLOPE, "CW_Compliance_Slope", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_SLOPE, "CCW_Compliance_Slope", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_GOAL_POSITION, "Goal_Position", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MOVING_SPEED, "Moving_Speed", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_TORQUE_LIMIT, "Torque_Limit", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_POSITION, "Present_Position", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_SPEED, "Present_Speed", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_LOAD, "Present_Load", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_VOLTAGE, "Present_Voltage", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_TEMPERATURE, "Present_Temperature", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_REGISTERED, "Registered", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MOVING, "Moving", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LOCK, "Lock", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PUNCH, "Punch", WORD))
		self._item.append(ct_item.ControlTableItem(56, "Punch", WORD))
		self._item.append(ct_item.ControlTableItem(73, "Goal_Acceleration", BYTE))
		self._the_number_of_item = 34

	def setMXInfo(self):
		self._velocity_to_value_ratio = float(86.81)

		self._value_of_min_radian_position = int(0)
		self._value_of_0_radian_position = int(2048)
		self._value_of_max_radian_position = int(4095)

		self._min_radian = float(-3.14159265)
		self._max_radian = float(3.14159265)


	def setMX2Item(self):
		self._item.append(ct_item.ControlTableItem(0  , "Model_Number"          , 2))
		self._item.append(ct_item.ControlTableItem(6  , "Firmware_Version"      , 1))
		self._item.append(ct_item.ControlTableItem(7  , "ID"                    , 1))
		self._item.append(ct_item.ControlTableItem(8  , "Baud_Rate"             , 1))
		self._item.append(ct_item.ControlTableItem(9  , "Return_Delay_Time"     , 1))
		self._item.append(ct_item.ControlTableItem(10 , "Drive_Mode"            , 1))
		self._item.append(ct_item.ControlTableItem(11 , "Operating_Mode"        , 1))
		self._item.append(ct_item.ControlTableItem(12 , "Secondary_ID"          , 1))
		self._item.append(ct_item.ControlTableItem(13 , "Protocol_Version"      , 1))
		self._item.append(ct_item.ControlTableItem(20 , "Homing_Offset"         , 4))
		self._item.append(ct_item.ControlTableItem(24 , "Moving_Threshold"      , 4))
		self._item.append(ct_item.ControlTableItem(31 , "Temperature_Limit"     , 1))
		self._item.append(ct_item.ControlTableItem(32 , "Max_Voltage_Limit"     , 2))
		self._item.append(ct_item.ControlTableItem(34 , "Min_Voltage_Limit"     , 2))
		self._item.append(ct_item.ControlTableItem(36 , "PWM_Limit"             , 2))
		self._item.append(ct_item.ControlTableItem(40 , "Acceleration_Limit"    , 4))
		self._item.append(ct_item.ControlTableItem(44 , "Velocity_Limit"        , 4))
		self._item.append(ct_item.ControlTableItem(48 , "Max_Position_Limit"    , 4))
		self._item.append(ct_item.ControlTableItem(52 , "Min_Position_Limit"    , 4))
		self._item.append(ct_item.ControlTableItem(63 , "Shutdown"              , 1))
		self._item.append(ct_item.ControlTableItem(64 , "Torque_Enable"         , 1))
		self._item.append(ct_item.ControlTableItem(65 , "LED"                   , 1))
		self._item.append(ct_item.ControlTableItem(68 , "Status_Return_Level"   , 1))
		self._item.append(ct_item.ControlTableItem(69 , "Registered_Instruction", 1))
		self._item.append(ct_item.ControlTableItem(70 , "Hardware_Error_Status" , 1))
		self._item.append(ct_item.ControlTableItem(76 , "Velocity_I_Gain"       , 2))
		self._item.append(ct_item.ControlTableItem(78 , "Velocity_P_Gain"       , 2))
		self._item.append(ct_item.ControlTableItem(80 , "Position_D_Gain"       , 2))
		self._item.append(ct_item.ControlTableItem(82 , "Position_I_Gain"       , 2))
		self._item.append(ct_item.ControlTableItem(84 , "Position_P_Gain"       , 2))
		self._item.append(ct_item.ControlTableItem(88 , "Feedforward_2nd_Gain"  , 2))
		self._item.append(ct_item.ControlTableItem(90 , "Feedforward_1st_Gain"  , 2))
		self._item.append(ct_item.ControlTableItem(98 , "Bus_Watchdog"          , 1))
		self._item.append(ct_item.ControlTableItem(100, "Goal_PWM"              , 2))
		self._item.append(ct_item.ControlTableItem(104, "Goal_Velocity"         , 4))
		self._item.append(ct_item.ControlTableItem(108, "Profile_Acceleration"  , 4))
		self._item.append(ct_item.ControlTableItem(112, "Profile_Velocity"      , 4))
		self._item.append(ct_item.ControlTableItem(116, "Goal_Position"         , 4))
		self._item.append(ct_item.ControlTableItem(120, "Realtime_Tick"         , 2))
		self._item.append(ct_item.ControlTableItem(122, "Moving"                , 1))
		self._item.append(ct_item.ControlTableItem(123, "Moving_Status"         , 1))
		self._item.append(ct_item.ControlTableItem(124, "Present_PWM"           , 2))
		self._item.append(ct_item.ControlTableItem(126, "Present_Load"          , 2))
		self._item.append(ct_item.ControlTableItem(128, "Present_Velocity"      , 4))
		self._item.append(ct_item.ControlTableItem(132, "Present_Position"      , 4))
		self._item.append(ct_item.ControlTableItem(136, "Velocity_Trajectory"   , 4))
		self._item.append(ct_item.ControlTableItem(140, "Position_Trajectory"   , 4))
		self._item.append(ct_item.ControlTableItem(144, "Present_Input_Voltage" , 2))
		self._item.append(ct_item.ControlTableItem(146, "Present_Temperature"   , 1))
		self._the_number_of_item = 49


	def setMX2Info(self):
		self._velocity_to_value_ratio = float(41.70)

		self._value_of_min_radian_position = int(0)
		self._value_of_0_radian_position = int(2048)
		self._value_of_max_radian_position = int(4095)

		self._min_radian = float(-3.14159265)
		self._max_radian = float(3.14159265)


	def setExtMXItem(self):
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MODEL_NUMBER, "Model_Number", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_FIRMWARE_VERSION, "Firmware_Version", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_ID,	"ID", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_BAUDRATE, "Baud_Rate", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_RETURN_DELAY, "Return_Delay_Time", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_ANGLE_LIMIT, "CW_Angle_Limit" , WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_ANGLE_LIMIT,"CCW_Angle_Limit", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_TEMPERATURE, "Temperature_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MIN_VOLTAGE, "Min_Voltage_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_VOLTAGE, "Max_Voltage_Limit", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MAX_TORQUE, "Max_Torque", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_STATUS_RETURN_LEVEL, "Status_Return_Level", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LED_ALARM, "Alarm_LED", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_ALARM_SHUTDOWN, "Shutdown", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_TORQUE_ENABLE, "Torque_Enable", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LED, "LED", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_MARGIN, "CW_Compliance_Margin", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_MARGIN, "CCW_Compliance_Margin", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_CLOCKWISE_SLOPE, "CW_Compliance_Slope", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_COUNTER_CLOCKWISE_SLOPE, "CCW_Compliance_Slope", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_GOAL_POSITION, "Goal_Position", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MOVING_SPEED, "Moving_Speed", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_TORQUE_LIMIT, "Torque_Limit", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_POSITION, "Present_Position", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_SPEED, "Present_Speed", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_LOAD, "Present_Load", WORD))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_VOLTAGE, "Present_Voltage", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PRESENT_TEMPERATURE, "Present_Temperature", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_REGISTERED, "Registered", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_MOVING, "Moving", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_LOCK, "Lock", BYTE))
		self._item.append(ct_item.ControlTableItem(ADDR_AX_PUNCH, "Punch", WORD))
		self._item.append(ct_item.ControlTableItem(56, "Punch", WORD))
		self._item.append(ct_item.ControlTableItem(68, "Current", WORD))
		self._item.append(ct_item.ControlTableItem(70, "Torque_Control_Mode_Enable", BYTE))
		self._item.append(ct_item.ControlTableItem(71, "Goal_Torque", WORD))
		self._item.append(ct_item.ControlTableItem(73, "Goal_Acceleration", BYTE))
		self._the_number_of_item = 37

	def setExtMXInfo(self):
		self._velocity_to_value_ratio = float(86.81)

		self._value_of_min_radian_position = int(0)
		self._value_of_0_radian_position = int(2048)
		self._value_of_max_radian_position = int(4095)

		self._min_radian = float(-3.14159265)
		self._max_radian = float(3.14159265)


	def getConrolTableItem(self, model_number):
		num = int(model_number)
		if (num == AX_12A or num == AX_12W or num == AX_18A):
			self.setAXItem()
		elif (num == RX_10 or num == RX_24F or num == RX_28 or num == RX_64):
			self.setRXItem()
		elif (num == EX_106):
			self.setEXItem()
		elif (num == MX_12W or num == MX_28):
			self.setMXItem()
		elif (num == MX_64 or num == MX_106):
			self.setExtMXItem()
		elif (num == MX_28_2):
			self.setMX2Item()
		elif (num == MX_64_2 or num == MX_106_2):
			self.setExtMX2Item()
		return self._item

	def getModelInfo(self, model_number):
		num = int(model_number)

		if (num == AX_12A or num == AX_12W or num == AX_18A):
			self.setAXInfo()
		elif (num == RX_10 or num == RX_24F or num == RX_28 or num == RX_64):
			self.setRXInfo()
		elif (num == EX_106):
			self.setEXInfo()
		elif (num == MX_12W or num == MX_28):
			self.setMXInfo()
		elif (num == MX_64 or num == MX_106):
			self.setExtMXInfo()
		elif (num == MX_28_2):
			self.setMX2Info()
		elif (num == MX_64_2 or num == MX_106_2):
			self.setExtMX2Info()
		return self

	def getTheNumberOfControlItem(self):
		return self._the_number_of_item


































