
from boto3.session import Session
arn_secret_key = ""
arn_access_key = ""
arn_external_id=""
arn = ""
def get_function_name(conn,fn):
    return getattr(conn, fn)

def get_all_resources(conn, fn, key, marker_response_key=None,marker_payload_key_name=None,request_body=None):
    pagination = True
    marker_response_key = marker_response_key if marker_response_key is not None else "Marker"
    marker_payload_key_name = marker_payload_key_name if marker_payload_key_name is not None else "Marker"
    marker = ''
    all_items = []
    function_name = get_function_name(conn,fn)
    while pagination:
        if marker:
            if request_body is not None:
                request_body[marker_payload_key_name] = marker
            else:
                request_body = {marker_payload_key_name:marker}
            response = function_name(**request_body)
        else:
            if request_body is not None:
                response = function_name(**request_body)
            else:
                response = function_name()
        if response is not None:
            marker = response.get(marker_response_key)
            all_items.extend(response[key])
        if not marker:
            pagination = False
            return all_items



sess = Session(aws_access_key_id=arn_access_key,
                       aws_secret_access_key=arn_secret_key,
                       region_name='us-east-1')
sts_connection = sess.client('sts')
# Assuming Role
assume_role_object = sts_connection.assume_role(RoleArn=arn,
                                                        RoleSessionName="test",
                                                        ExternalId=arn_external_id,
                                                        DurationSeconds=3600)
credentials = assume_role_object['Credentials']
boto3_session = Session(
        aws_access_key_id=credentials['SecretAccessKey'],
        aws_secret_access_key=credentials['SessionToken'],
    aws_session_token=credentials['AccessKeyId']
    )
regions = ['us-east-1']
for region in regions:
    try:
        client = boto3_session.client(service_name='kms', region_name=region)
        print(client.list_aliases())
    except Exception as e:
        print(e)

for region in regions:
    try:
        aliases = get_all_resources(client, "list_aliases", "Aliases")
        print(aliases)
    except Exception as e:
        print(e)