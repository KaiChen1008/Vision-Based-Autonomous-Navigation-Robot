#include <ros/ros.h>
#include <geometry_msgs/PoseWithCovarianceStamped.h>
#include <tf/transform_broadcaster.h>

tf::Transform transform;
tf::Quaternion q;

void pose_callback(const geometry_msgs::PoseWithCovarianceStampedPtr &pose)
{
   static tf::TransformBroadcaster br;
   q.setX(pose->pose.pose.orientation.x);
   q.setY(pose->pose.pose.orientation.y);
   q.setZ(pose->pose.pose.orientation.z);
   q.setW(pose->pose.pose.orientation.w);

   transform.setOrigin(tf::Vector3(pose->pose.pose.position.x, pose->pose.pose.position.y, 0.0));
   transform.setRotation(q);

   br.sendTransform(tf::StampedTransform(transform, ros::Time::now(), "map", "base_footprint"));
}

int main(int argc, char **argv)
{
	printf("hihi-------------------------------------------------------");
   ros::init(argc, argv, "pose_tf");
   ros::NodeHandle n("~");
   ros::Subscriber pose_sub = n.subscribe("/slam_pose", 1, pose_callback);
   ros::Rate loop_rate(100);
   while (ros::ok())
   {
      ros::spinOnce();
      loop_rate.sleep();
   }
}
