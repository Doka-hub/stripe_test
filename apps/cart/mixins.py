from django.http.response import JsonResponse


class AjaxMixin:
    response = {}

    def get_response(self, **kwargs) -> dict:
        self.response.update({**kwargs})
        return self.response.copy()

    def ajax_response(self, data: dict, **kwargs):
        return JsonResponse(data, **kwargs)
