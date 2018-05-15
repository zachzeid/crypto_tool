#!/usr/bin/env python

import argparse

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
    if args.get_parameter:
        print(get_parameter(aws_profile, args.get_parameter[0]))


def arguments():
    parser = argparse.ArgumentParser(description="""Keystore is a tool to
    upload sensitive parameters to AWS SSM Parameter Store""")
    parser.add_argument('-k', '--key_id', nargs='*', help="""
    The key name for encrypting parameters""")
    parser.add_argument('-n', '--parameter_name', nargs='*', help="""Name of the
    SSM Parameter in the format /<account name>/<team>/<type>/<resource_name>""")
    parser.add_argument('-p', '--profile', nargs='*', help="""AWS profile Name
    and credentials to be used.""")

    parser.add_argument('-u', '--upload', nargs='*', help="""Name of file to be
    uploaded as a parameter.""")
    parser.add_argument('-g', '--get_parameter', nargs='*', help=""" Name of the SSM
    parameter to be fetched.""")
    args = parser.parse_args()
    return args


def get_parameter(aws_profile, parameter_name):
    session = boto3.session.Session(profile_name=aws_profile)
    ssm_client = session.client('ssm')
    kms_client = session.client('kms')
    try:
        response = ssm_client.get_parameters(
            Names=[
                parameter_name
            ],
            WithDecryption=True
        )
        return response['Parameters'][0]['Value']
    except Exception as e:
        return e


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
            Overwrite=True
        )
        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            return "Parameter %s sucessfully uploaded." % "/{}".format(parameter_name)
    except Exception as e:
        return e


if __name__ == '__main__':
    main()
