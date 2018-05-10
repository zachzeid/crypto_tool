#!/usr/bin/env python

import argparse
import sys
from base64 import b64encode
from datetime import datetime
from os import chmod

import boto3
from Crypto.PublicKey import RSA


def main():
    args = arguments()
    if args.profile:
        aws_profile = args.profile[0]
    else:
        aws_profile = 'default'

    if not args.account_name:
        account_name = get_account_alias(aws_profile)
        print(account_name)
    else:
        account_name = args.account_name[0]
    team_name = args.team_name
    generated_key = generate_ssh_keys()
    store_ssh_keys(args.key_id[0], generated_key,
                   account_name, team_name, aws_profile)


def arguments():
    parser = argparse.ArgumentParser(description="make magic")
    parser.add_argument('-k', '--key_id', nargs='*', required=True)
    parser.add_argument('-a', '--account_name', nargs='*')
    # parser.add_argument('-b', '--key_size', nargs='*')
    parser.add_argument('-t', '--team_name', nargs='*', required=True)
    parser.add_argument('-p', '--profile', nargs='*')
    args = parser.parse_args()
    return args


def get_account_alias(aws_profile):
    session = boto3.session.Session(profile_name=aws_profile)
    iam_client = session.client('iam')
    account_name = iam_client.list_account_aliases()['AccountAliases'][0]
    return account_name


def store_ssh_keys(keyid, keybinary, account_name, team_name, aws_profile):
    session = boto3.session.Session(profile_name=aws_profile)
    ssm_client = session.client('ssm')
    kms_client = session.client('kms')

    encrypt_ssh_key = kms_client.encrypt(
        KeyId="alias/%s" % keyid, Plaintext=keybinary)
    encoded_blob = b64encode(encrypt_ssh_key['CiphertextBlob'])
    ssm_client.put_parameter(
        Description="Encrypted SSH Key",
        Type="SecureString",
        KeyId="alias/%s" % keyid,
        Name="/{}/{}/resource/sshkey".format(account_name, team_name[0]),
        Value=encoded_blob.decode('ascii'),
        Overwrite=True
    )

# Generated SSH private/public keys in the OpenSSH format.


def generate_ssh_keys():
    dt = datetime.today()
    print(f"{dt:%Y-%m-%d}")
    key = RSA.generate(4096)

    with open('private_key_{}'.format(f"{dt:%Y-%m-%d}"), "wb") as private_key_file:
        private_key_file.write(key.exportKey('OpenSSH'))

    public_key = key.publickey()

    with open('public_key_{}.pub'.format(f"{dt:%Y-%m-%d}"), 'wb') as public_key_file:
        public_key_file.write(public_key.exportKey('OpenSSH'))
    # We return this so we can go ahead and encrypt and store into SSM Parameter store.
    return key.export_key('OpenSSH').decode('ascii')


if __name__ == '__main__':
    main()
