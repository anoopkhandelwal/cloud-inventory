from boto.ec2 import EC2Connection
from boto.rds2.layer1 import RDSConnection
from boto.regioninfo import load_regions, RegionInfo
from boto.sts import STSConnection

aws_access_key_id=""
aws_secret_access_key = ""
external_id = ""
arn = ''
class STSService(object):
    def __init__(self, arn):
        sts_connection = STSConnection(aws_access_key_id=aws_access_key_id,
                                       aws_secret_access_key=aws_secret_access_key)

        self.credentials = sts_connection.assume_role(role_arn=arn,
                                                      role_session_name="testrole",
                                                      external_id=external_id, duration_seconds=3600).credentials

        self.tmp_access_key = self.credentials.access_key
        self.tmp_secret_key = self.credentials.secret_key
        self.security_token = self.credentials.session_token


class AWSConnections(object):
    def __init__(self, arn):
        self.tmp_credentials = STSService(arn).credentials

    def get_rds_connection(self, region):
        """
        Use this Method to get an RDS connection


        :type region: str
        :rtype : RDSConnection
        :param region: string for example us-east-1
        :param arn:
        :return:
        """

        region = RegionInfo(name=region, endpoint=load_regions()['rds'][region])
        tmp_access_key = self.tmp_credentials.access_key
        tmp_secret_key = self.tmp_credentials.secret_key
        security_token = self.tmp_credentials.session_token
        rds_connection = RDSConnection(aws_access_key_id=tmp_access_key, aws_secret_access_key=tmp_secret_key,
                                       region=region, security_token=security_token)
        return rds_connection

    def get_ec2_connection(self, region):
        """
        Use this Method to get an ec2 connection



        :type region: str
        :rtype : EC2Connection
        :param region: string for example us-east-1
        :return:
        """

        region = RegionInfo(name=region, endpoint=load_regions()['ec2'][region])

        tmp_access_key = self.tmp_credentials.access_key
        tmp_secret_key = self.tmp_credentials.secret_key
        security_token = self.tmp_credentials.session_token
        ec2_connection = EC2Connection(aws_access_key_id=tmp_access_key, aws_secret_access_key=tmp_secret_key,
                                       region=region, security_token=security_token)
        return ec2_connection


def get_error_message(e):
    """
    """
    message = ''
    if e.status is not None:
        message = message + "Status : " + str(e.status) + "  "
    if e.reason is not None:
        message = message + "Reason : " + str(e.reason) + "  "
    if e.message is not None:
        tmp_message = str(e.message).split(".")[0]
        message = message + "Message : " + str(tmp_message) + "  "
    else:
        tmp_message = str(e.body['Error']['Message'])
        message = message + "Message : " + str(tmp_message) + "  "
    return message



# RDS
conn = AWSConnections(arn=arn).get_rds_connection(region='us-east-1')
rds_instance_id = 'test-db'
snapshot_identifier = rds_instance_id[:45] + time.strftime("%Y-%m-%d-%H-%M-%S")
try:
    response = conn.create_db_snapshot(db_instance_identifier=rds_instance_id,
                                       db_snapshot_identifier=snapshot_identifier)
    print(response)
except BotoServerError as e:
    print(get_error_message(e))



# EC2
conn = AWSConnections(arn=arn).get_ec2_connection(region='us-east-1')
try:
    response = conn.create_snapshot(volume_id='')
except BotoServerError as e:
    print(get_error_message(e))
except Exception as e:
    print(get_error_message(e))
