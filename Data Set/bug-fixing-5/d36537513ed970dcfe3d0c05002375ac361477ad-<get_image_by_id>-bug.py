def get_image_by_id(module, connection, image_id):
    try:
        try:
            images_response = connection.describe_images(ImageIds=[image_id])
        except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
            module.fail_json_aws(e, msg=('Error retrieving image %s' % image_id))
        images = images_response.get('Images')
        no_images = len(images)
        if (no_images == 0):
            return None
        if (no_images == 1):
            result = images[0]
            try:
                result['LaunchPermissions'] = connection.describe_image_attribute(Attribute='launchPermission', ImageId=image_id)['LaunchPermissions']
                result['ProductCodes'] = connection.describe_image_attribute(Attribute='productCodes', ImageId=image_id)['ProductCodes']
            except botocore.exceptions.ClientError as e:
                if (e.response['Error']['Code'] != 'InvalidAMIID.Unavailable'):
                    module.fail_json_aws(e, msg=('Error retrieving image attributes' % image_id))
            except botocore.exceptions.BotoCoreError as e:
                module.fail_json_aws(e, msg=('Error retrieving image attributes' % image_id))
            return result
        module.fail_json(msg=('Invalid number of instances (%s) found for image_id: %s.' % (str(len(images)), image_id)))
    except (botocore.exceptions.BotoCoreError, botocore.exceptions.ClientError) as e:
        module.fail_json_aws(e, msg='Error retrieving image by image_id')