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
      this.mappedX = null;
      this.mappedY = null;
    }
    else {
      if (initObj.hasOwnProperty('mappedX')) {
        this.mappedX = initObj.mappedX
      }
      else {
        this.mappedX = 0.0;
      }
      if (initObj.hasOwnProperty('mappedY')) {
        this.mappedY = initObj.mappedY
      }
      else {
        this.mappedY = 0.0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type motor_controls_msg
    // Serialize message field [mappedX]
    bufferOffset = _serializer.float64(obj.mappedX, buffer, bufferOffset);
    // Serialize message field [mappedY]
    bufferOffset = _serializer.float64(obj.mappedY, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type motor_controls_msg
    let len;
    let data = new motor_controls_msg(null);
    // Deserialize message field [mappedX]
    data.mappedX = _deserializer.float64(buffer, bufferOffset);
    // Deserialize message field [mappedY]
    data.mappedY = _deserializer.float64(buffer, bufferOffset);
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
    return '501e3fc00f088a8af5e28080c514dcc4';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    float64 mappedX
    float64 mappedY
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new motor_controls_msg(null);
    if (msg.mappedX !== undefined) {
      resolved.mappedX = msg.mappedX;
    }
    else {
      resolved.mappedX = 0.0
    }

    if (msg.mappedY !== undefined) {
      resolved.mappedY = msg.mappedY;
    }
    else {
      resolved.mappedY = 0.0
    }

    return resolved;
    }
};

module.exports = motor_controls_msg;
