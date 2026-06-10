#!/usr/bin/env python3

import rospy
from datetime import datetime

from geometry_msgs.msg import PoseStamped
from geometry_msgs.msg import TwistStamped
from autoware_mini.msg import VehicleCmd

class SyncLogger:
    def __init__(self, log_rate_hz=2.0):
        rospy.init_node('custom_sync_logger', anonymous=True)
        self.log_filename = f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        self.data_store = {}

        self.header_written = False
        
        self.topics_config = {
            "pose_position_x": (
                "/localization/current_pose",
                PoseStamped,
                lambda msg: msg.pose.position.x
            ),
            "pose_position_y": (
                "/localization/current_pose",
                PoseStamped,
                lambda msg: msg.pose.position.y
            ),
            "pose_position_z": (
                "/localization/current_pose",
                PoseStamped,
                lambda msg: msg.pose.position.z
            ),
            "pose_orientation_x": (
                "/localization/current_pose",
                PoseStamped,
                lambda msg: msg.pose.orientation.x
            ),
            "pose_orientation_y": (
                "/localization/current_pose",
                PoseStamped,
                lambda msg: msg.pose.orientation.y
            ),
            "pose_orientation_z": (
                "/localization/current_pose",
                PoseStamped,
                lambda msg: msg.pose.orientation.z
            ),
            "velocity_linear_x": (
                "/localization/current_velocity",
                TwistStamped,
                lambda msg: msg.twist.linear.x
            ),
            "velocity_linear_y": (
                "/localization/current_velocity",
                TwistStamped,
                lambda msg: msg.twist.linear.y
            ),
            "velocity_linear_z": (
                "/localization/current_velocity",
                TwistStamped,
                lambda msg: msg.twist.linear.z
            ),
            "velocity_angular_x": (
                "/localization/current_velocity",
                TwistStamped,
                lambda msg: msg.twist.angular.x
            ),
            "velocity_angular_y": (
                "/localization/current_velocity",
                TwistStamped,
                lambda msg: msg.twist.angular.y
            ),
            "velocity_angular_z": (
                "/localization/current_velocity",
                TwistStamped,
                lambda msg: msg.twist.angular.z
            ),
            "control_lamp_left": (
                "/control/vehicle_cmd",
                VehicleCmd,
                lambda msg: msg.lamp_cmd.l
            ),
            "control_lamp_right": (
                "/control/vehicle_cmd",
                VehicleCmd,
                lambda msg: msg.lamp_cmd.r
            ),
            "control_gear": (
                "/control/vehicle_cmd",
                VehicleCmd,
                lambda msg: msg.gear_cmd.gear
            ),
            "control_mode": (
                "/control/vehicle_cmd",
                VehicleCmd,
                lambda msg: msg.mode
            ),
            "control_ctrl_cmd_linear_velocity": (
                "/control/vehicle_cmd",
                VehicleCmd,
                lambda msg: msg.ctrl_cmd.linear_velocity
            ),
            "control_ctrl_cmd_linear_acceleration": (
                "/control/vehicle_cmd",
                VehicleCmd,
                lambda msg: msg.ctrl_cmd.linear_acceleration
            ),
            "control_ctrl_cmd_steering_angle": (
                "/control/vehicle_cmd",
                VehicleCmd,
                lambda msg: msg.ctrl_cmd.steering_angle
            ),
            "control_emergency": (
                "/control/vehicle_cmd",
                VehicleCmd,
                lambda msg: msg.emergency
            )

        }

        for log_name, (topic_name, msg_type, extract_func) in self.topics_config.items():
            self.data_store[log_name] = "N/D"
            rospy.Subscriber(
                topic_name, 
                msg_type, 
                self.generic_callback, 
                callback_args=(log_name, extract_func)
            )
            rospy.loginfo(f"Listening on topic: {topic_name} -> mapped to '{log_name}'")

        rospy.Timer(rospy.Duration(1.0 / log_rate_hz), self.write_log)
        rospy.loginfo(f"Logger started at {log_rate_hz}Hz. Saving to {self.log_filename}")

    def generic_callback(self, msg, args):
        """
        Generic callback. Receives the message and decodes it using
        the lambda function defined in the configuration.
        """
        log_name, extract_func = args
        try:
            extracted_value = extract_func(msg)
            self.data_store[log_name] = extracted_value
        except Exception as e:
            self.data_store[log_name] = f"ERR"

    def write_log(self, event):
        """
        Take a snapshot of the data_store and save it as CSV with a timestamp.
        """
        if not self.header_written:
            chiavi = ",".join(self.data_store.keys())
            header_line = f"timestamp,{chiavi}"
            
            with open(self.log_filename, "a") as f:
                f.write(header_line + "\n")
            
            self.header_written = True

        timestamp = datetime.now().strftime('%H:%M:%S.%f')[:-3]
        
        value_str = [str(value) for value in self.data_store.values()]
        
        data = ",".join(value_str)
        data_line = f"{timestamp},{data}"
        
        with open(self.log_filename, "a") as f:
            f.write(data_line + "\n")

if __name__ == '__main__':
    try:
        SyncLogger(log_rate_hz=20.0)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass