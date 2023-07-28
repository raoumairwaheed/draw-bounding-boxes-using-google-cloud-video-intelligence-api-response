## Video Annotation Tool (Google Cloud Vision API)
<div style="display: flex;">
  <img src="sample1.png" alt="Annotated Video Sample 1" width="400" />
  <img src="sample2.png" alt="Annotated Video Sample 2" width="400" />
</div>

## Introduction
This project provides a video annotation tool that can draw bounding boxes and labels around logos and text detected in a video using json response returned by google cloud vision api.
### Google Cloud Vision API
The Google Cloud Vision API is a powerful image and video analysis tool that offers various features, including logo and text detection. When you submit a video to the API for analysis, it processes the video frames and returns JSON responses containing information about the detected logos and text. https://cloud.google.com/vision

Our video annotation tool uses the JSON responses obtained from the Google Cloud Vision API for both logo and text detection tasks. The responses contain relevant data such as the location of logos and text in each frame, along with confidence scores for the detections.

## Prerequisites
- Python 3.x
- OpenCV (cv2)
- NumPy
- tqdm

## Installation
1. Clone this repository to your local machine.
2. Install the required dependencies using the following command:
   ```bash
   pip install opencv-python numpy tqdm
   ```

## Usage
1. Place the video file (`filename.mp4`) you want to annotate in the "Source Directory".
2. Obtain the JSON response from the Google Cloud Vision API for both logo and text detection in the video. Save the JSON responses in separate files.
3. Update the `file_name`, `json_path` (for both logo and text JSON files), and `type_of_detection` variables in the `main.py` file.
   - `file_name`: Name of the video file to be annotated.
   - `json_path`: Path to the JSON response files from the Google Cloud Vision API for logo and text detection.
   - `type_of_detection`: Type of detection (either 'logo' or 'text').
4. Run the script using the following command:
   ```bash
   python draw_bbox.py
   ```
5. The annotated video will be saved in the "Result Directory" with the bounding boxes and labels drawn around the detected logos and text.

## Notes
- The tool utilizes the JSON responses from the Google Cloud Vision API for both logo and text detection tasks.
- The JSON responses should follow the structure specified in the sample code provided in the `main.py` file.

## Example
Suppose you want to annotate a video named `sample_video.mp4` with logo and text detection. Follow these steps:
1. Place the `sample_video.mp4` file in the "Source Directory".
2. Obtain the JSON response for logo detection using the Google Cloud Vision API and save it in a file named `sample_logo_detection.json`.
3. Obtain the JSON response for text detection using the Google Cloud Vision API and save it in a file named `sample_text_detection.json`.
4. Open the `main.py` file and update the variables:
   ```python
   file_name = "sample_video.mp4"
   json_path = "path/to/sample_logo_detection.json"
   type_of_detection = "logo"
   ```
   ```python
   file_name = "sample_video.mp4"
   json_path = "path/to/sample_text_detection.json"
   type_of_detection = "text"
   ```
5. Run the script using the command:
   ```bash
   python draw_bbox.py
   ```
6. The annotated video will be saved in the "Result Directory" with both logo and text bounding boxes and labels drawn around the detected entities.

