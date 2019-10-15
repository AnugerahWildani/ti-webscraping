import os
from deepdiff import DeepDiff 
import json
from django.core.mail import send_mail
from django.core import mail

def compare_data(path):
    listfile = os.listdir(path)
    full_path = [os.path.join(path,"{0}".format(x)) for x in listfile]
    oldest_file = min(full_path, key=os.path.getctime)
    newest_file = max(full_path, key=os.path.getctime)
    jsonDataold = open(oldest_file)
    jsonDatanew = open(newest_file)
    data_old = json.load(jsonDataold)

    data_new = json.load(jsonDatanew)

    # ddiff = DeepDiff(data_old, data_new, ignore_order=True)
    ddiff = DeepDiff(data_new, data_old, ignore_order=True, exclude_paths={"root['timestamp']"})
    return ddiff

