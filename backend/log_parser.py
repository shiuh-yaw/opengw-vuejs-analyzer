import json
import xml.dom.minidom
from typing import List, Dict, Any, Tuple, Optional
import re

# Internal modules
from psp_database import identify_psp

def beautify_json(content: str) -> str:
    """Pretty-prints a JSON string."""
    try:
        return json.dumps(json.loads(content), indent=2)
    except (json.JSONDecodeError, TypeError):
        return content

def beautify_xml(content: str) -> str:
    """Pretty-prints an XML string."""
    try:
        dom = xml.dom.minidom.parseString(content)
        return dom.toprettyxml(indent="  ")
    except Exception:
        return content

def parse_content_block(block_str: str) -> Tuple[Optional[str], Optional[str]]:
    """Identifies if a block of text is JSON or XML."""
    block_str = block_str.strip()
    json_content = None
    xml_content = None

    if (block_str.startswith("{") and block_str.endswith("}")) or \
       (block_str.startswith("[") and block_str.endswith("]")):
        try:
            json.loads(block_str)
            json_content = block_str
        except json.JSONDecodeError:
            pass

    if block_str.startswith("<") and block_str.endswith(">"):
        try:
            xml.dom.minidom.parseString(block_str)
            xml_content = block_str
        except Exception:
            pass

    return json_content, xml_content

def parse_input_into_blocks(raw_content: str) -> List[Dict[str, Any]]:
    """
    Parses raw text content into blocks, identifies PSPs, and pretty-prints JSON/XML.
    """
    blocks_content = re.findall(r"\[(.*?)\]", raw_content, re.DOTALL)
    
    parsed_blocks = []
    for i, block_str in enumerate(blocks_content):
        json_content, xml_content = parse_content_block(block_str)
        
        content_type = "text"
        beautified_content = block_str.strip()
        if json_content:
            content_type = "json"
            beautified_content = beautify_json(json_content)
        elif xml_content:
            content_type = "xml"
            beautified_content = beautify_xml(xml_content)

        # Identify PSP
        psp = identify_psp(block_str)

        block_data = {
            "id": i + 1,
            "raw_content": block_str.strip(),
            "type": content_type,
            "beautified_content": beautified_content,
            "psp": psp,
        }
        parsed_blocks.append(block_data)
        
    return parsed_blocks

