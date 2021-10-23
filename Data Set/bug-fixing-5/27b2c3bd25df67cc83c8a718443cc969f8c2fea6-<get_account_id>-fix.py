def get_account_id(module, region=None, endpoint=None, **aws_connect_kwargs):
    "return the account id we are currently working on\n\n    get_account_id tries too find out the account that we are working\n    on.  It's not guaranteed that this will be easy so we try in\n    several different ways.  Giving either IAM or STS privilages to\n    the account should be enough to permit this.\n    "
    account_id = None
    try:
        sts_client = boto3_conn(module, conn_type='client', resource='sts', region=region, endpoint=endpoint, **aws_connect_kwargs)
        account_id = sts_client.get_caller_identity().get('Account')
    except ClientError:
        try:
            iam_client = boto3_conn(module, conn_type='client', resource='iam', region=region, endpoint=endpoint, **aws_connect_kwargs)
            account_id = iam_client.get_user()['User']['Arn'].split(':')[4]
        except ClientError as e:
            if (e.response['Error']['Code'] == 'AccessDenied'):
                except_msg = to_native(e.message)
                account_id = except_msg.search('arn:aws:iam::([0-9]{12,32}):\\w+/').group(1)
            if (account_id is None):
                module.fail_json_aws(e, msg='getting account information')
        except Exception as e:
            module.fail_json_aws(e, msg='getting account information')
    return account_id