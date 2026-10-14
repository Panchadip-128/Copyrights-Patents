"""
Submission Gateway & Physical Interdiction Module for ARICCA-X

Implements concrete hardware-interfacing gateway interdiction controller,
session revocation, sandbox payload quarantining, transaction state locking,
thread pool suppression, and cryptographic audit payload emission.

Copyright (c) 2026. All rights reserved. Patent Pending.
"""

try:
    from .gateway_controller import (
        ActuationRecord,
        GatewayActionCode,
        ManuscriptSubmissionPayload,
        SubmissionGatewayInterdictionController,
    )
except (ImportError, ValueError):
    from submission_gateway.gateway_controller import (
        ActuationRecord,
        GatewayActionCode,
        ManuscriptSubmissionPayload,
        SubmissionGatewayInterdictionController,
    )

__all__ = [
    "ActuationRecord",
    "GatewayActionCode",
    "ManuscriptSubmissionPayload",
    "SubmissionGatewayInterdictionController",
]
