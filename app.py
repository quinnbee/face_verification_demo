from flask import Flask, render_template, request, redirect, url_for, jsonify
app = Flask(__name__)

import urllib
from azure.storage.blob import BlockBlobService, PublicAccess
import requests
import io
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person

def run_sample():
    print("In Run")
    try:
        blob_service_client = BlockBlobService(
            account_name='your_account_name', account_key='your_account_key')

        container_name = 'your_container_name'
        blob_service_client.create_container(container_name)

        blob_service_client.set_container_acl(
            container_name, public_access=PublicAccess.Container)
        # List the blobs in the container
        print("\nList blobs in the container")
        generator = blob_service_client.list_blobs(container_name)
        for blob in generator:
            print(blob.name)
    except Exception as e:
        print(e)

@app.route('/', methods=["GET","POST"])
def home():
    if request.method=="POST":
        data=request.get_json()['Data']
        response = urllib.request.urlopen(data)
        Data= io.BytesIO(response.file.read())
        print(response)
        run_sample()

        KEY = "your_key_from_cognitive_services"

        ENDPOINT = "your_endpoint_url"
        face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
        
        blobUrl = "your_blob_url"

        detected_faces1 = face_client.face.detect_with_url(blobUrl, detection_model='detection_03')
        blobImageId = detected_faces1[0].face_id

        detected_faces = face_client.face.detect_with_stream(Data, detection_model='detection_03')
        inputImageId=detected_faces[0].face_id

        verify_result_same = face_client.face.verify_face_to_face(blobImageId, inputImageId)
        print(verify_result_same.confidence)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
