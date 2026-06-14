"""Middleware that injects configured messages into HTML responses."""

from __future__ import annotations

from django.http import HttpResponseBase, StreamingHttpResponse

from .injector import get_matching_injections, inject_messages, inject_stylesheet


class InjectMessageMiddleware:
    """Inject active messages into rendered HTML responses."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return self.process_response(request, response)

    def process_response(
        self,
        request,
        response: HttpResponseBase,
    ) -> HttpResponseBase:
        if not self._should_process(response):
            return response

        injections = get_matching_injections(request.path)
        if not injections:
            return response

        charset = response.charset or "utf-8"
        try:
            content = response.content.decode(charset)
        except (UnicodeDecodeError, LookupError):
            return response

        content, modified = inject_messages(content, injections)
        if not modified:
            return response

        content = inject_stylesheet(content)
        response.content = content.encode(charset)
        if "Content-Length" in response:
            response["Content-Length"] = str(len(response.content))
        return response

    @staticmethod
    def _should_process(response: HttpResponseBase) -> bool:
        if isinstance(response, StreamingHttpResponse) or not hasattr(response, "content"):
            return False
        if not 200 <= response.status_code < 300:
            return False
        content_type = response.get("Content-Type", "")
        return content_type.startswith("text/html")
