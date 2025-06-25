class ApiClientError(Exception):
    "Base exception for API client errors."
    pass

class ApiConnectionError(ApiClientError):
    "Exception for errors connecting to the API."
    pass

class ApiTimeoutError(ApiClientError):
    "Exception for API request timeouts."
    pass
