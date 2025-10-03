import json
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Tuple, Optional

def parse_log_content(content: str) -> Tuple[Optional[str], Optional[str]]:
    """Identifies and extracts JSON or XML content from a log string."""
    json_content = None
    xml_content = None

    try:
        # Attempt to parse as JSON
        start_index = content.find("{")
        end_index = content.rfind("}")
        if start_index != -1 and end_index != -1:
            json_str = content[start_index : end_index + 1]
            json.loads(json_str)
            json_content = json_str
    except json.JSONDecodeError:
        pass

    try:
        # Attempt to parse as XML
        start_index = content.find("<")
        end_index = content.rfind(">")
        if start_index != -1 and end_index != -1:
            xml_str = content[start_index : end_index + 1]
            ET.fromstring(xml_str)
            xml_content = xml_str
    except ET.ParseError:
        pass

    return json_content, xml_content

def parse_transaction_flow(log_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Parses a list of log entries to extract the transaction flow."""
    flow_steps = []
    for entry in log_data:
        message = entry.get("message", "")
        if "INFO  OPENGW_MESSAGE_LOG -" in message:
            content_part = message.split("INFO  OPENGW_MESSAGE_LOG -", 1)[1].strip()
            json_content, xml_content = parse_log_content(content_part)

            step = {
                "timestamp": entry.get("timestamp"),
                "raw_content": content_part,
                "has_json": bool(json_content),
                "json_content": json_content,
                "has_xml": bool(xml_content),
                "xml_content": xml_content,
            }
            flow_steps.append(step)

    return flow_steps

