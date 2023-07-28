import os

import cv2
import json
import time
import numpy as np
from tqdm import tqdm
def get_text_data(filename):
    # Opening JSON file
    with open(filename, 'r') as openfile:
        json_object = json.load(openfile)
    # segment_result_test = json_object['annotationResults'][0]['textAnnotations'][0]
    segment_result = json_object['annotationResults'][0]['textAnnotations']
    all_text_data = []
    # print('Segment Result',segment_result)
    for result in segment_result:
        label = result['text']
        time = result['segments'][0]['segment']
        confidence = result['segments'][0]['confidence']
        time_stamps = result['segments'][0]['frames']
        data = dict(time)
        data['labels'] = label
        data['confidence'] = confidence
        data['frames'] = time_stamps
        all_text_data.append(data)
    return all_text_data


def get_logo_data(filename):
    with open(filename, 'r') as openfile:
        # Reading from json file
        json_object = json.load(openfile)
    logo_result = json_object['annotationResults'][0]['logoRecognitionAnnotations']
    all_logos_data = []
    for result in logo_result:
        label = result['entity']['description']
        time = result['tracks'][0]['segment']
        confidence = result['tracks'][0]['confidence']
        time_stamps = result['tracks'][0]['timestampedObjects']
        data = dict(time)
        data['labels'] = label
        data['confidence'] = confidence
        data['timestampedObjects'] = time_stamps
        all_logos_data.append(data)
    return all_logos_data


def get_fps_detail(video, json_path, type):
    fps = float(video.get(cv2.CAP_PROP_FPS))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps_detail = [[] for _ in range(total_frames)]
    if type == 'logo':
        brands = get_logo_data(json_path)
        for brand in brands:
            brand_name = brand['labels']
            for time in brand['timestampedObjects']:
                frame_no = int(float(time['timeOffset'][:-1]) * fps)
                bbox = time['normalizedBoundingBox']
                info = {brand_name: bbox}
                fps_detail[frame_no].append(info)

    else:

        brands = get_text_data(json_path)
        for brand in brands:
            brand_name = brand['labels']
            for time in brand['frames']:
                frame_no = int(float(time['timeOffset'][:-1]) * fps)
                bbox = time['rotatedBoundingBox']
                info = {brand_name: bbox}
                fps_detail[frame_no].append(info)

    return fps_detail


def draw_bbox(file_name, video_path, output_path, json_path, type_of_detection):

    video = cv2.VideoCapture(video_path+file_name)
    start_time = time.time()  # Record the start time
    # this function is making an array based on number of frames in the video
    frame_wise_info = get_fps_detail(video, json_path, type_of_detection)

    # Get video properties
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(video.get(cv2.CAP_PROP_FPS))
    result_video_fps = video.get(cv2.CAP_PROP_FPS)
    # Create a VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'avc1')
    output_video = cv2.VideoWriter(output_path, fourcc, result_video_fps, (frame_width, frame_height))
    if type_of_detection == 'logo':
        print('Starting Processing for Logo ... ')
    else:
        print('Starting Processing for Text ... ')

    for frame_number in tqdm(range(total_frames),colour="green"):
        _, frame = video.read()
        # this loop iterates the array of frames and if multiple brands are there on a single frame
        for brand_bbox in frame_wise_info[frame_number]:
            if brand_bbox:
                key = list(brand_bbox.keys())[0]
                # when logo is being drawn
                if type_of_detection == 'logo':

                    if (len(brand_bbox[key])) == 4:
                        left = int(brand_bbox[key]['left'] * frame_width)
                        top = int(brand_bbox[key]['top'] * frame_height)
                        right = int(brand_bbox[key]['right'] * frame_width)
                        bottom = int(brand_bbox[key]['bottom'] * frame_height)
                        cv2.putText(frame, key, (left, top - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                else:
                    # when text is being drawn on video
                    vertices = brand_bbox[key]['vertices']
                    if len(vertices[0])==2 and len(vertices[1])==2 and len(vertices[2])==2 and len(vertices[3])==2:
                        vertices_list = [
                            (vertices[0]['x'], vertices[0]['y']),
                            (vertices[1]['x'], vertices[1]['y']),
                            (vertices[2]['x'], vertices[2]['y']),
                            (vertices[3]['x'], vertices[3]['y'])
                        ]
                        pixel_vertices = [(int(vertex[0] * frame_width), int(vertex[1] * frame_height)) for vertex in
                                          vertices_list]
                        # Draw rotated bounding box on the frame
                        cv2.putText(frame, key, (int(vertices[0]['x'] * frame_width), int(vertices[0]['y'] * frame_height) - 5),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2)
                        cv2.polylines(frame, [np.array(pixel_vertices)], isClosed=True, color=(255, 255, 0), thickness=2)
        output_video.write(frame)
    # # Release the video and output video file
    video.release()
    output_video.release()
    print('Completed !')

    end_time = time.time()  # Record the end time

    execution_time = end_time - start_time
    print(f"Execution time: {execution_time} seconds")


if __name__ == '__main__':
    file_name = "sample_video.mp4"
    json_path = "path/to/sample_logo_detection.json"
    type_of_detection = 'Type of Detection ("text" or "logo")'

    draw_bbox(file_name, 'Source Directory',"Result Directory"+file_name, json_path, type_of_detection)


