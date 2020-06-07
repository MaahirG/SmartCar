// Auto-generated. Do not edit!

// (in-package rcProjPkg.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class motor_controls_msg {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.angle = null;
      this.magnitude = null;
    }
    else {
      if (initObj.hasOwnProperty('angle')) {
        this.angle = initObj.angle
      }
      else {
        this.angle = 0.0;
      }
      if (initObj.hasOwnProperty('magnitude')) {
        this.magnitude = initObj.magnitude
      }
      else {
        this.magnitude = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type motor_controls_msg
    // Serialize message field [angle]
    bufferOffset = _serializer.float64(obj.angle, buffer, bufferOffset);
    // Serialize message field [magnitude]
    bufferOffset = _serializer.float64(obj.magnitude, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type motor_controls_msg
    let len;
    let data = new motor_controls_msg(null);
    // Deserialize message field [angle]
    data.angle = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [magnitude]
    data.magnitude = _deserializer.float64(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 16;
  }

  static datatype() {
    // Returns string type for a message object
    return 'rcProjPkg/motor_controls_msg';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '9f60d5cf267edc4256952dd2a35a600f';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 angle
    float64 magnitude
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new motor_controls_msg(null);
    if (msg.angle !== undefined) {
      resolved.angle = msg.angle;
    }
    else {
      resolved.angle = 0.0
    }

    if (msg.magnitude !== undefined) {
      resolved.magnitude = msg.magnitude;
    }
    else {
      resolved.magnitude = 0.0
    }

    return resolved;
    }
};

module.exports = motor_controls_msg;
