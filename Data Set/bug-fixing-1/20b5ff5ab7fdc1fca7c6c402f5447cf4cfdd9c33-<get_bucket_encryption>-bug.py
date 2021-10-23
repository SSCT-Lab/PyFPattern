

@AWSRetry.exponential_backoff(max_delay=120, catch_extra_error_codes=['NoSuchBucket'])
def get_bucket_encryption(s3_client, bucket_name):
    try:
        result = s3_client.get_bucket_encryption(Bucket=bucket_name)
        return result.get('ServerSideEncryptionConfiguration').get('Rules')[0].get('ApplyServerSideEncryptionByDefault')
    except ClientError as e:
        if (e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError'):
            return None
        else:
            raise e
