def delete_email(instance, **kwargs):
    if UserEmail.objects.filter(email=instance.email).exists():
        return
    Email.objects.filter(email=instance.email).delete()