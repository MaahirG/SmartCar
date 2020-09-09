# https://github.com/dusty-nv/jetson-inference/blob/master/docs/detectnet-example-2.md
# https://www.youtube.com/watch?v=bcM5AQSAzUY
# https://rawgit.com/dusty-nv/jetson-inference/dev/docs/html/python/jetson.utils.html#videoSource
# https://rawgit.com/dusty-nv/jetson-inference/dev/docs/html/python/jetson.utils.html#cudaImage
# VALUES IN DETECTIONS: https://github.com/NVIDIA/DIGITS/issues/2214
# COCO DATASET CLASSIDs (Corresponding to here) https://tech.amikelive.com/node-718/what-object-categories-labels-are-in-coco-dataset/


# Dusty Nvidia new Jetpack Object Detection with Utils LinkedIn Article: https://www.linkedin.com/pulse/realtime-object-detection-10-lines-python-code-jetson-dustin-franklin
# Install PyTorch to do some transfer learning: https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-transfer-learning.md
# RETRAIN MOBILE NET SSD ON OWN DATASET USING PYTORCH - Transfer learning to create your own model on already trained model: https://github.com/dusty-nv/jetson-inference/blob/master/docs/pytorch-ssd.md

# python bindings for core C++ library from hello AI world that use TensorRT library underneath to accelerate inferencing
import jetson.inference as ji
import jetson.utils
import numpy as np
import cv2


# # OLD RELIABLE
# net = ji.detectNet("ssd-mobilenet-v2", threshold=0.8) # pretrained model based on coco dataset https://github.com/dusty-nv/jetson-inference/#object-detection
# camera = jetson.utils.videoSource("csi://0")      # create camera object with '/dev/video0' for V4L2 or "csi://0" for MIPI RPi camera
# display = jetson.utils.videoOutput("display://0") # 'my_video.mp4' for file

# while display.IsStreaming():
#   img = camera.Capture()   # The returned image will be a jetson.utils.cudaImage object that contains attributes like width, height, and pixel format
#                              # block until next frame available, converts image to floating point RGBA to be input into neural network\
#   print("Height:",img.height, "Width:",img.width,"Format:",img.format)
#   print(type(img))
#   # frame=jetson.utils.cudaToNumpy(img,1280,720,4)
#   detections = net.Detect(img)
#   display.Render(img)         # Render takes the CUDA format image from camera capture and applies the bounding boxes and inplace applies it to the input image
#   display.SetStatus("Object Detection | Network {:.0f} FPS".format(net.GetNetworkFPS()))  # visualize the results with OpenGL


# NEXT STEPS: GET IT SO THAT IT WON'T ALLOW THE SAME CAR/TRUCK TWICE

truck = [13,28,5] # dx, dy, size, detection num 
car = [11,15,7]

# each detection is relative to the previous detection

# OPENCV DISPLAY
net = jetson.inference.detectNet("ssd-mobilenet-v2", threshold=0.8)
camera = jetson.utils.gstCamera(1280, 720, "0")
cv2.destroyAllWindows()
while True:
    img, width, height = camera.CaptureRGBA(zeroCopy=True)

    detections = net.Detect(img, width, height)
    
    if len(detections) > 0:
        for detection in detections:
            id = detection.ClassID
            print("ClassID:", id, "Left:", detection.Left, "Right:", detection.Right, "Width:", detection.Width, "Height:", detection.Height)
        if id == 8 or id == 6 or id ==3:
            print("Roadway")


    fps = net.GetNetworkFPS()

    jetson.utils.cudaDeviceSynchronize()
    # create a numpy ndarray that references the CUDA memory it won't be copied, but uses the same memory underneath
    aimg = jetson.utils.cudaToNumpy(img, width, height, 4)
    print ("img shape {}".format (aimg.shape))
    aimg = cv2.cvtColor (aimg.astype (np.uint8), cv2.COLOR_RGBA2BGR)
    cv2.putText(aimg, "FPS: {}".format(fps), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
    cv2.imshow("image", aimg)
    # cv2.moveWindow('image',0,0)
    if cv2.waitKey(1)==ord('q'):
        break

# WITHOUT THIS, GST CAMERA AND OPENCV DISPLAY MAY NOT OPEN AGAIN!
cv2.destroyAllWindows()

Attachments area
Preview YouTube video Real-Time Object Detection in 10 Lines of Python Code on Jetson Nano

