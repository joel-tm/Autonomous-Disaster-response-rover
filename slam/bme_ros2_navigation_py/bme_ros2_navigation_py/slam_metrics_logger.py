import rclpy
from rclpy.node import Node
import csv
import time
import math
from sensor_msgs.msg import LaserScan
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from geometry_msgs.msg import Quaternion

class SLAMMetricsLogger(Node):
    def __init__(self):
        super().__init__("slam_metrics_logger")
        
        # Subscribers
        self.odom_sub = self.create_subscription(Odometry, "/odom", self.odom_callback, 10)
        self.lidar_sub = self.create_subscription(LaserScan, "/scan", self.lidar_callback, 10)
        
        # Variables to store data
        self.prev_time = time.time()
        self.prev_x = None
        self.prev_y = None
        self.prev_speed = 0
        
        self.min_obstacle_distance = None
        self.lidar_point_count = 0
        self.rotation_angle = 0

        # CSV File Initialization
        self.csv_file = "slam_metrics_log.csv"
        with open(self.csv_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Time (s)", "X Position", "Y Position", "Z Position",
                "Speed (m/s)", "Acceleration (m/s²)", "Obstacle Distance (m)",
                "Rotation Angle (deg)", "LiDAR Points"
            ])

    def odom_callback(self, msg):
        current_time = time.time()
        dt = current_time - self.prev_time

        x = msg.pose.pose.position.x
        y = msg.pose.pose.position.y
        z = msg.pose.pose.position.z

        # Compute speed
        if self.prev_x is not None and self.prev_y is not None:
            distance = math.sqrt((x - self.prev_x) ** 2 + (y - self.prev_y) ** 2)
            speed = distance / dt
            acceleration = (speed - self.prev_speed) / dt if dt > 0 else 0
        else:
            speed, acceleration = 0, 0

        # Compute heading angle from quaternion
        quat = msg.pose.pose.orientation
        self.rotation_angle = self.quaternion_to_euler(quat)

        # Update previous values
        self.prev_x, self.prev_y = x, y
        self.prev_speed = speed
        self.prev_time = current_time

        # Log data to CSV
        self.log_data(current_time, x, y, z, speed, acceleration)

    def lidar_callback(self, msg):
        self.min_obstacle_distance = min(msg.ranges) if msg.ranges else float("inf")
        self.lidar_point_count = sum(1 for r in msg.ranges if r > 0)

    def quaternion_to_euler(self, quat):
        # Convert quaternion to Euler angles
        siny_cosp = 2 * (quat.w * quat.z + quat.x * quat.y)
        cosy_cosp = 1 - 2 * (quat.y**2 + quat.z**2)
        return math.degrees(math.atan2(siny_cosp, cosy_cosp))

    def log_data(self, time, x, y, z, speed, acceleration):
        with open(self.csv_file, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                round(time, 2), x, y, z,
                round(speed, 2), round(acceleration, 2),
                round(self.min_obstacle_distance, 2),
                round(self.rotation_angle, 2), self.lidar_point_count
            ])

def main(args=None):
    rclpy.init(args=args)
    node = SLAMMetricsLogger()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
