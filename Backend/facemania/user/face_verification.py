import os
import io
import json
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
import requests
from PIL import Image, ImageDraw, ImageFont
from django.conf import settings

# Microsoft Face API
API_KEY = os.getenv('API_KEY')
ENDPOINT = os.getenv('ENDPOINT')
face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(API_KEY)) # Creating face client instance


def verify_face(source_url, target_url):
    """
    Matches source and target faces
    """

    response_detected_faces = face_client.face.detect_with_stream(
        image=open(os.path.join(settings.BASE_DIR,source_url), 'rb'),
        detection_model='detection_03',
        recognition_model='recognition_04',
    ) # detect faces in source image
    face_ids = [face.face_id for face in response_detected_faces] # face ids for all the detected faces

    img_source = open(os.path.join(settings.BASE_DIR,target_url[1:]), 'rb')
    response_face_source = face_client.face.detect_with_stream(
        image=img_source,
        detection_model='detection_03',
        recognition_model='recognition_04'
    ) # detect faces from the video stream from target URL
    face_id_source = response_face_source[0].face_id

    matched_faces = face_client.face.find_similar(
        face_id=face_id_source,
        face_ids=face_ids
    ) # search for similar-looking faces

    img = Image.open(open(os.path.join(settings.BASE_DIR,source_url), 'rb'))

    answer = False
    # verify whether two faces belong to a same person
    for matched_face in matched_faces:
        for face in response_detected_faces:
            if face.face_id == matched_face.face_id:
                rect = face.face_rectangle
                left = rect.left
                top = rect.top
                right = rect.width + left
                bottom = rect.height + top
                face_verified = face_client.face.verify_face_to_face(
                    face_id1=matched_faces[0].face_id,
                    face_id2=face.face_id
                )
                answer = answer or face_verified.is_identical

    return answer
