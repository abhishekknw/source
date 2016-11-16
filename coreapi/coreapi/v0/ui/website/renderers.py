from rest_framework import renderers


class XlsxRenderer(renderers.BaseRenderer):
    """
    When a view is entered REST framework will perform content negotiation on the incoming request, and determine
    the most appropriate renderer to satisfy the request.The basic process of content negotiation involves examining
    the request's Accept header, to determine which media types it expects in the response.

    This custom renderer class is written so that GenericExportData API can use to determine what kind of content it
    needs to send in the response. It does so by examining what's in the Accept header of incoming request
    In this case the API is sending a binary response for file of type xlsx.
    """

    media_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    format = '.xlsx'
    charset = None
    render_style = 'binary'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data