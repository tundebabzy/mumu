
def status(request):
    """
    Returns a Payment object from which the user's status is determined.
    """
    status = getattr(request, 'status', None)

    return {'status': status}
