// Generated by gencpp from file rcProjPkg/motor_controls_msg.msg
// DO NOT EDIT!


#ifndef RCPROJPKG_MESSAGE_MOTOR_CONTROLS_MSG_H
#define RCPROJPKG_MESSAGE_MOTOR_CONTROLS_MSG_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace rcProjPkg
{
template <class ContainerAllocator>
struct motor_controls_msg_
{
  typedef motor_controls_msg_<ContainerAllocator> Type;

  motor_controls_msg_()
    : angle(0.0)
    , magnitude(0.0)  {
    }
  motor_controls_msg_(const ContainerAllocator& _alloc)
    : angle(0.0)
    , magnitude(0.0)  {
  (void)_alloc;
    }



   typedef double _angle_type;
  _angle_type angle;

   typedef double _magnitude_type;
  _magnitude_type magnitude;





  typedef boost::shared_ptr< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> const> ConstPtr;

}; // struct motor_controls_msg_

typedef ::rcProjPkg::motor_controls_msg_<std::allocator<void> > motor_controls_msg;

typedef boost::shared_ptr< ::rcProjPkg::motor_controls_msg > motor_controls_msgPtr;
typedef boost::shared_ptr< ::rcProjPkg::motor_controls_msg const> motor_controls_msgConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::rcProjPkg::motor_controls_msg_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::rcProjPkg::motor_controls_msg_<ContainerAllocator1> & lhs, const ::rcProjPkg::motor_controls_msg_<ContainerAllocator2> & rhs)
{
  return lhs.angle == rhs.angle &&
    lhs.magnitude == rhs.magnitude;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::rcProjPkg::motor_controls_msg_<ContainerAllocator1> & lhs, const ::rcProjPkg::motor_controls_msg_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace rcProjPkg

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "9f60d5cf267edc4256952dd2a35a600f";
  }

  static const char* value(const ::rcProjPkg::motor_controls_msg_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x9f60d5cf267edc42ULL;
  static const uint64_t static_value2 = 0x56952dd2a35a600fULL;
};

template<class ContainerAllocator>
struct DataType< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "rcProjPkg/motor_controls_msg";
  }

  static const char* value(const ::rcProjPkg::motor_controls_msg_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float64 angle\n"
"float64 magnitude\n"
;
  }

  static const char* value(const ::rcProjPkg::motor_controls_msg_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.angle);
      stream.next(m.magnitude);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct motor_controls_msg_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::rcProjPkg::motor_controls_msg_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::rcProjPkg::motor_controls_msg_<ContainerAllocator>& v)
  {
    s << indent << "angle: ";
    Printer<double>::stream(s, indent + "  ", v.angle);
    s << indent << "magnitude: ";
    Printer<double>::stream(s, indent + "  ", v.magnitude);
  }
};

} // namespace message_operations
} // namespace ros

#endif // RCPROJPKG_MESSAGE_MOTOR_CONTROLS_MSG_H
