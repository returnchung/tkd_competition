class custom_error(Exception):
    def __init__(self, message, code=500, payload=None):
        Exception.__init__(self)
        self.message = message
        self.code = code
        self.payload = payload
        self.headers = {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        }

    def to_dict(self):
        response = dict()
        errors = list()
        data = dict()
        try:
            data.update(self.payload)
        except TypeError:
            pass

        if data:
            errors.append(data)

        response["message"] = self.message
        response["errors"] = errors
        return response
