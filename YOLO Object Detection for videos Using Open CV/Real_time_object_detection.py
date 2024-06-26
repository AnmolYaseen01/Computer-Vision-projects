import cv2
import numpy as np

# Load Yolo
yolo_weight = "C:\\Users\\Admin\\Documents\\GitHub\\Computer vision\\YOLO Object Detection for Webcams Using Open CV\\yolov3.weights"
yolo_config = "C:\\Users\\Admin\\Documents\\GitHub\\Computer vision\\YOLO Object Detection for Webcams Using Open CV\\yolov3.cfg"
coco_labels = "C:\\Users\\Admin\\Documents\\GitHub\\Computer vision\\YOLO Object Detection for Webcams Using Open CV\\coco.names"

net = cv2.dnn.readNet(yolo_weight, yolo_config)

classes = []
with open(coco_labels, "r") as f:
    classes = [line.strip() for line in f.readlines()]

layer_names = net.getLayerNames()

# Find names of three output layers
output_layers_indices = net.getUnconnectedOutLayers()
print("Output layers indices:", output_layers_indices)

# Assuming output_layers_indices is a list of scalars
output_layers = [layer_names[i - 1] for i in output_layers_indices]
print("Output layers:", output_layers)

# Defining desired shape
fWidth = 256
fHeight = 256

# Below function will read video frames
cap = cv2.VideoCapture("path_to_your_video.mp4")

while True:
    read_ok, img = cap.read()
    
    if not read_ok:
        break  # Break the loop if the video is finished
    
    height, width, channels = img.shape

    # Detecting objects
    blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    font = cv2.FONT_HERSHEY_DUPLEX
    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            confidence_label = int(confidences[i] * 100)
            color = (255, 0, 0)  # Fixed color for now
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, f'{label, confidence_label}', (x - 25, y + 75), font, 2, color, 2)

    cv2.imshow("Image", img)
    # Close video window by pressing 'x'
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break
