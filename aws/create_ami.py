__author__ = 'anoop'
from boto.ec2 import EC2Connection
import boto.ec2
import time
import re

access_key = ""
secret_key = ""
conn = EC2Connection(access_key,secret_key)



inst_id=''
epoch_time=int(time.time())
des=inst_id+"-"+str(epoch_time)
name="test-ami"

img_id=conn.create_image(instance_id=inst_id,description=des,name=name)
print(img_id)


instance_dict={}
images=conn.get_all_images(owners=['self'])

for image in images:

    description=str(image.description)
    if re.match(r'(i-)[0-9](.*)',description):
        instance_id=description[0:10]
        creationTime=description[11:]
        if instance_id in instance_dict.keys():
            dictd={}
            dictd["name"]=image.id
            dictd["CreationTime"]=creationTime
            instance_dict[instance_id].append(dictd)
        else:
            instance_dict[instance_id]=[]
            dictd={}
            dictd["name"]=image.id
            dictd["CreationTime"]=creationTime
            instance_dict[instance_id].append(dictd)



for instance_id,ami_ids in instance_dict.items():
    ami_ids= sorted(ami_ids,key=lambda k: k["CreationTime"],reverse=True)
    instance_dict[instance_id]=ami_ids
print(instance_id ,"AmiIds: ",instance_dict)
