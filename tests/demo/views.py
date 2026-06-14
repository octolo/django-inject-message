from django.shortcuts import render


def single_message(request):
    """Demo page for injecting a single message."""
    return render(request, "demo/single_message.html")


def multiple_messages(request):
    """Demo page for injecting several messages on the same page."""
    return render(request, "demo/multiple_messages.html")


def message_multiple_places(request):
    """Demo page for injecting one message at several anchors."""
    return render(request, "demo/message_multiple_places.html")
