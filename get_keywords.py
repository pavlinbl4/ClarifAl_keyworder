from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import service_pb2_grpc
from clarifai_grpc.grpc.api import service_pb2, resources_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2
from cred import key


def generate_keywords(file_path):
    stub = service_pb2_grpc.V2Stub(ClarifaiChannel.get_grpc_channel())
    api_key = key
    metadata = (('authorization', f'Key {api_key}'),)

    with open(file_path, "rb") as f:
        file_bytes = f.read()

    request = service_pb2.PostModelOutputsRequest(
        model_id='general-image-recognition',
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        base64=file_bytes
                    )
                )
            )
        ])

    # This is the model ID of a publicly available General model. You may use any other public or custom model ID.
    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        raise Exception("Request failed, status code: " + str(response.status.code))

    keywords = []
    for concept in response.outputs[0].data.concepts:
        keywords.append(concept.name)
    return keywords


if __name__ == '__main__':
    print(generate_keywords("/Users/evgeniy/Pictures/20231026_Консерватория/20231026PEV_3283.JPG"))
