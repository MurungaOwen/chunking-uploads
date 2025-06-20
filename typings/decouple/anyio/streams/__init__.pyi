"""
This type stub file was generated by pyright.
"""

import logging
import re
import ssl
import sys
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from functools import wraps
from typing import Any, TypeVar, TypeVarTuple, Unpack
from .. import BrokenResourceError, EndOfStream, aclose_forcefully, get_cancelled_exc_class, to_thread
from .._core._typedattr import TypedAttributeSet, typed_attribute
from ..abc import AnyByteStream, ByteStream, Listener, TaskGroup

if sys.version_info >= (3, 11):
    ...
else:
    ...
T_Retval = TypeVar("T_Retval")
PosArgsT = TypeVarTuple("PosArgsT")
_PCTRTT = tuple[tuple[str, str], ...]
_PCTRTTT = tuple[_PCTRTT, ...]
class TLSAttribute(TypedAttributeSet):
    """Contains Transport Layer Security related attributes."""
    alpn_protocol: str | None = ...
    channel_binding_tls_unique: bytes = ...
    cipher: tuple[str, str, int] = ...
    peer_certificate: None | dict[str, str | _PCTRTTT | _PCTRTT] = ...
    peer_certificate_binary: bytes | None = ...
    server_side: bool = ...
    shared_ciphers: list[tuple[str, str, int]] | None = ...
    ssl_object: ssl.SSLObject = ...
    standard_compatible: bool = ...
    tls_version: str = ...


@dataclass(eq=False)
class TLSStream(ByteStream):
    """
    A stream wrapper that encrypts all sent data and decrypts received data.

    This class has no public initializer; use :meth:`wrap` instead.
    All extra attributes from :class:`~TLSAttribute` are supported.

    :var AnyByteStream transport_stream: the wrapped stream

    """
    transport_stream: AnyByteStream
    standard_compatible: bool
    _ssl_object: ssl.SSLObject
    _read_bio: ssl.MemoryBIO
    _write_bio: ssl.MemoryBIO
    @classmethod
    async def wrap(cls, transport_stream: AnyByteStream, *, server_side: bool | None = ..., hostname: str | None = ..., ssl_context: ssl.SSLContext | None = ..., standard_compatible: bool = ...) -> TLSStream:
        """
        Wrap an existing stream with Transport Layer Security.

        This performs a TLS handshake with the peer.

        :param transport_stream: a bytes-transporting stream to wrap
        :param server_side: ``True`` if this is the server side of the connection,
            ``False`` if this is the client side (if omitted, will be set to ``False``
            if ``hostname`` has been provided, ``False`` otherwise). Used only to create
            a default context when an explicit context has not been provided.
        :param hostname: host name of the peer (if host name checking is desired)
        :param ssl_context: the SSLContext object to use (if not provided, a secure
            default will be created)
        :param standard_compatible: if ``False``, skip the closing handshake when
            closing the connection, and don't raise an exception if the peer does the
            same
        :raises ~ssl.SSLError: if the TLS handshake fails

        """
        ...
    
    async def unwrap(self) -> tuple[AnyByteStream, bytes]:
        """
        Does the TLS closing handshake.

        :return: a tuple of (wrapped byte stream, bytes left in the read buffer)

        """
        ...
    
    async def aclose(self) -> None:
        ...
    
    async def receive(self, max_bytes: int = ...) -> bytes:
        ...
    
    async def send(self, item: bytes) -> None:
        ...
    
    async def send_eof(self) -> None:
        ...
    
    @property
    def extra_attributes(self) -> Mapping[Any, Callable[[], Any]]:
        ...
    


@dataclass(eq=False)
class TLSListener(Listener[TLSStream]):
    """
    A convenience listener that wraps another listener and auto-negotiates a TLS session
    on every accepted connection.

    If the TLS handshake times out or raises an exception,
    :meth:`handle_handshake_error` is called to do whatever post-mortem processing is
    deemed necessary.

    Supports only the :attr:`~TLSAttribute.standard_compatible` extra attribute.

    :param Listener listener: the listener to wrap
    :param ssl_context: the SSL context object
    :param standard_compatible: a flag passed through to :meth:`TLSStream.wrap`
    :param handshake_timeout: time limit for the TLS handshake
        (passed to :func:`~anyio.fail_after`)
    """
    listener: Listener[Any]
    ssl_context: ssl.SSLContext
    standard_compatible: bool = ...
    handshake_timeout: float = ...
    @staticmethod
    async def handle_handshake_error(exc: BaseException, stream: AnyByteStream) -> None:
        """
        Handle an exception raised during the TLS handshake.

        This method does 3 things:

        #. Forcefully closes the original stream
        #. Logs the exception (unless it was a cancellation exception) using the
           ``anyio.streams.tls`` logger
        #. Reraises the exception if it was a base exception or a cancellation exception

        :param exc: the exception
        :param stream: the original stream

        """
        ...
    
    async def serve(self, handler: Callable[[TLSStream], Any], task_group: TaskGroup | None = ...) -> None:
        ...
    
    async def aclose(self) -> None:
        ...
    
    @property
    def extra_attributes(self) -> Mapping[Any, Callable[[], Any]]:
        ...
    


