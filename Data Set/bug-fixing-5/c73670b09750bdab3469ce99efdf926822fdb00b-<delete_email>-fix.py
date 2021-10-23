def delete_email(instance, **kwargs):
    if UserEmail.objects.filter(email__iexact=instance.email).exists():
        return
    Email.objects.filter(email=instance.email).delete()