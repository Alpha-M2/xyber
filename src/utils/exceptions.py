"""Custom exceptions for Xyber Chatbot."""


class XyberChatbotException(Exception):
    """Base exception for Xyber Chatbot."""

    pass


class ConfigurationError(XyberChatbotException):
    """Error in configuration."""

    pass
