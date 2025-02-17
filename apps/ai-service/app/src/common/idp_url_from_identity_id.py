def idp_url_from_identity_id(identity_id: str, region: str) -> str:
    return f"https://cognito-idp.{region}.amazonaws.com/{identity_id}"
