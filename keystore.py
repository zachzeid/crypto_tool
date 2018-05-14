#!/usr/bin/env python

import argparse
from base64 import b64encode
from datetime import datetime

import boto3


def main():
    args = arguments()
    if args.profile:
        aws_profile = args.profile[0]
    else:
        aws_profile = 'default'
    if args.upload:
        ssh_key_file = file_upload(args.upload[0])
        print(store_ssh_keys(
            args.key_id[0],
            ssh_key_file,
            args.parameter_name[0],
            aws_profile
        ))


def arguments():
    parser = argparse.ArgumentParser(description="make magic")
    parser.add_argument('-k', '--key_id', nargs='*', required=True)
    parser.add_argument('-n', '--parameter_name', nargs='*', help="""Name of the
    SSM Parameter in the format /<account name>/<team>/resource/<ssh_key_name>""")
    parser.add_argument('-p', '--profile', nargs='*')
    parser.add_argument('-u', '--upload', nargs='*')
    args = parser.parse_args()
    return args


def file_upload(filename):
    with open(filename, 'r') as f:
        return f.read()


def store_ssh_keys(keyid, keybinary, parameter_name, aws_profile):
    session = boto3.session.Session(profile_name=aws_profile)
    ssm_client = session.client('ssm')
    kms_client = session.client('kms')

    encrypt_ssh_key = keybinary
    encoded_blob = encrypt_ssh_key

    try:
        response = ssm_client.put_parameter(
            Description="Encrypted SSH Key",
            Type="SecureString",
            KeyId="alias/%s" % keyid,
            Name="/{}".format(parameter_name),
            Value=encoded_blob,

            # Value=encoded_blob.decode('ascii'),
            Overwrite=True
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return "Parameter %s sucessfully uploaded." % "/{}".format(parameter_name)
    except Exception as e:
        return e


if __name__ == '__main__':
    main()
