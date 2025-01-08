from rest_framework.renderers import JSONRenderer



class CustomeJSONRendered(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        mapper = {
            "GET" : "record fetched from db",
            "POST" : "record created",
            "PUT" : "record updated",
            "PATCH" : "record updated",
            "DELETE" : "record deleted",
        }
        response_data = {
            "status" : True,
            "data" : data,
            "message" : mapper[renderer_context['request'].method]
        }
        return super().render(response_data, accepted_media_type, renderer_context)