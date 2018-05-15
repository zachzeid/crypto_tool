James says I should have a README.md

Crypto_tool has nothing to do with crytpography.  All this tool will do is take
a file (-f) and upload the content into AWS SSM Parameter Store and encrypt it
with a given AWS KMS alias (-k).  You can also get parameters (-g) and this
program assumes that anything you are putting into SSM is encrypted, and will
try to decrypt it.

usage: parameterstore.py [-h] [-k [KEY_ID [KEY_ID ...]]]
                         [-n [PARAMETER_NAME [PARAMETER_NAME ...]]]
                         [-p [PROFILE [PROFILE ...]]]
                         [-u [UPLOAD [UPLOAD ...]]]
                         [-g [GET_PARAMETER [GET_PARAMETER ...]]]

Keystore is a tool to upload sensitive parameters to AWS SSM Parameter Store

optional arguments:
  -h, --help            show this help message and exit
  -k [KEY_ID [KEY_ID ...]], --key_id [KEY_ID [KEY_ID ...]]
                        The key name for encrypting parameters
  -n [PARAMETER_NAME [PARAMETER_NAME ...]], --parameter_name [PARAMETER_NAME [PARAMETER_NAME ...]]
                        Name of the SSM Parameter in the format /<account
                        name>/<team>/<type>/<resource_name>
  -p [PROFILE [PROFILE ...]], --profile [PROFILE [PROFILE ...]]
                        AWS profile Name and credentials to be used.
  -u [UPLOAD [UPLOAD ...]], --upload [UPLOAD [UPLOAD ...]]
                        Name of file to be uploaded as a parameter.
  -g [GET_PARAMETER [GET_PARAMETER ...]], --get_parameter [GET_PARAMETER [GET_PARAMETER ...]]
                        Name of the SSM parameter to be fetched.
