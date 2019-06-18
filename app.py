from flask import Flask, jsonify,render_template, request
import tensorflow as tf
import time,os,json
from PIL import Image
import numpy as np #модуль для численных манипуляций с большим объемом данных
import pandas as pd #модуль для работы с таблицами
import requests
from utils import label_map_util
from utils import visualization_utils as vis_util
import matplotlib.pyplot as plt
import matplotlib.image as mpimg 

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
PATH_TO_CKPT = '/root/application/SignalNeuroHack/trainedModels/ssd_mobilenet_Detector.pb' # Путь к обученной модели нейросети
PATH_TO_LABELS = '/root/application/SignalNeuroHack/trainedModels/label_map.pbtxt'  # Путь к label-файлу
NUM_CLASSES = 8
IMAGE_SIZE = (12, 8)
label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

detection_graph = tf.Graph()
with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
        serialized_graph = fid.read()
        od_graph_def.ParseFromString(serialized_graph)
        tf.import_graph_def(od_graph_def, name='')

@app.route('/')
def dash_overview():
	return render_template('index.html')
	
@app.route('/api/<file_name>', methods=['POST'])
def UploadFiles(file_name):
    data_post = json.loads(request.data) 
    lat = data_post['lat'] 
    long = data_post['long']
    data = data_post['data']
    time = data_post['time']
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            IMAGE_PATH = '/root/application/SignalNeuroHack/dataset/testimages/'+file_name
            sess.run(tf.global_variables_initializer())
            image = Image.open(IMAGE_PATH)
            (im_width, im_height) = image.size 
            image_np = np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
            to_pixel = np.array([im_height, im_width, im_height, im_width])
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            image_np_expanded = np.expand_dims(image_np, axis=0)
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            scores = detection_graph.get_tensor_by_name('detection_scores:0')
            classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            (boxes, scores, classes, num_detections) = sess.run(
            [boxes, scores, classes, num_detections],
            feed_dict={image_tensor: image_np_expanded})  
            vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            min_score_thresh=0.3,
            use_normalized_coordinates=True,
            line_thickness=3)
            #plt.figure(figsize=IMAGE_SIZE)
            #plt.imshow(image_np)
            #plt.savefig('new'+file_name)
            mpimg.imsave('new_'+file_name,image_np)
            #print (num_detections)
           # print (boxes)
            crack_num = 0
            pits_num = 0
            markup_num = 0
            for i in range(len(scores[0])):
                if scores[0][i] > 0.3:
                    if int(classes[0][i]) == 6:
                        pits_num += 1
                    elif (int(classes[0][i]) == 7) or (int(classes[0][i]) == 8):
                        markup_num += 1
                    else:
                        crack_num += 1
            print (crack_num, pits_num, markup_num)
            dataa = {
				  "lat":lat,
				  "long":long,
				  "data":data,
				  "time":time,
				  "precision_class":crack_num
				  }
            #say_hi('new_'+file_name,dataa)
    return jsonify(dataa)
if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=False, host='0.0.0.0', port=3334)