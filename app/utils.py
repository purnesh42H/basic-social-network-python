def get_token(request):
    authorization_header = request.headers.get('Authorization', '')
    token = authorization_header.replace('Bearer ', '')  # Assuming a "Bearer" token format
    return token

def get_requestor_id(request):
    return request.headers.get('requestor_id', '')