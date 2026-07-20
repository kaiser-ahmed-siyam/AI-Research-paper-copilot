from __future__ import annotations

import ssl

import certifi

# Windows Python's bundled OpenSSL doesn't read the OS certificate store, so
# urlopen() can fail CERTIFICATE_VERIFY_FAILED even on a fine connection.
# Pinning to certifi's CA bundle keeps verification on (no security downgrade)
# while working around that gap.
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
