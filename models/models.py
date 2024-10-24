from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel


# Define a Pydantic model for handling incoming JSON schema input
class Field(BaseModel):
    name: str
    type: str
    children: Optional[List[Field]] = None  # Allow nested fields


class SchemaInput(BaseModel):
    fields: List[Dict[str, Any]]
