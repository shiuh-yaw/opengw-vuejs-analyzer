from typing import Dict, Any, Optional, List

# Mock database of PSPs and their identifying keywords
PSP_IDENTIFIERS: Dict[str, List[str]] = {
    "Stripe": ["stripe.com", "Stripe API", "sk_live_"],
    "PayPal": ["paypal.com", "PayPal API", "Bearer A21AA"],
    "Adyen": ["adyen.com", "Adyen API", "adyen_live_"]
}

# Mock database of PSP API documentation and optimization suggestions
PSP_API_DOCS: Dict[str, Dict[str, Any]] = {
    "Stripe": {
        "endpoints": {
            "/v1/charges": {
                "status": "legacy",
                "recommendation": "Use the PaymentIntents API for modern integrations. It offers better flexibility and SCA support."
            },
            "/v1/payment_intents": {
                "status": "recommended",
                "recommendation": "Ensure you are using the latest API version to take advantage of new features and security enhancements."
            }
        },
        "optimizations": [
            "Use idempotency keys to safely retry requests without creating duplicate charges.",
            "Expand objects in your API calls to reduce the number of subsequent requests."
        ]
    },
    "PayPal": {
        "endpoints": {
            "/v1/payments/payment": {
                "status": "active",
                "recommendation": "Ensure you are handling asynchronous payment confirmations via webhooks for reliability."
            },
            "/v2/checkout/orders": {
                "status": "recommended",
                "recommendation": "This is the preferred endpoint for new integrations. It supports more payment methods and a better user experience."
            }
        },
        "optimizations": [
            "Use the `PayPal-Request-Id` header to trace requests and troubleshoot issues.",
            "Cache access tokens until they expire to reduce authentication overhead."
        ]
    },
    "Adyen": {
        "endpoints": {
            "/v67/payments": {
                "status": "active",
                "recommendation": "Utilize the `additionalData` field for passing custom data and enabling advanced features."
            }
        },
        "optimizations": [
            "Implement webhooks for real-time payment status updates.",
            "Use Adyen\'s library for your platform to simplify integration and ensure best practices."
        ]
    }
}

def identify_psp(content: str) -> Optional[str]:
    """Identifies the PSP from a block of text based on keywords."""
    for psp, keywords in PSP_IDENTIFIERS.items():
        for keyword in keywords:
            if keyword.lower() in content.lower():
                return psp
    return None

def get_psp_api_docs(psp_name: str) -> Optional[Dict[str, Any]]:
    """Retrieves the API documentation for a given PSP."""
    return PSP_API_DOCS.get(psp_name)

