"""
Agent 1 Pydantic Schemas - Design to Astro Code Generator
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class ColorToken(BaseModel):
    name: str = Field(..., description="Semantic color token name (e.g. primary-dark)")
    hex: str = Field(..., description="Hex code of the color (e.g. #0B1B3D)")
    usage: str = Field(..., description="Intended usage: header, hero background, accent CTA, text")


class TypographyToken(BaseModel):
    element: str = Field(..., description="Target HTML tag or role: h1, h2, h3, body, nav, button")
    font_family: str = Field(default="Inter, sans-serif")
    size: str = Field(..., description="CSS font size (e.g. 2.5rem or 40px)")
    weight: str = Field(default="600")
    line_height: str = Field(default="1.2")


class SectionSpec(BaseModel):
    id: str = Field(..., description="Unique slug for section (e.g. hero, sectors, stats)")
    name: str = Field(..., description="Human-readable title (e.g. Regional Sectors)")
    component_name: str = Field(..., description="Astro component name (e.g. Sectors.astro)")
    description: str = Field(..., description="Structural and functional description of the section")
    estimated_height_ratio: float = Field(default=0.2, description="Approximate vertical ratio of overall page")
    data_keys: List[str] = Field(default_factory=list, description="Keys in structured data file backing this section")


class DesignAnalysisResult(BaseModel):
    project_name: str = Field(default="RDGCC Corporate Portal")
    brand_identity: str = Field(..., description="Summary of aesthetic, tone, and visual guidelines")
    colors: List[ColorToken] = Field(default_factory=list)
    typography: List[TypographyToken] = Field(default_factory=list)
    sections: List[SectionSpec] = Field(default_factory=list)
    layout_type: str = Field(default="corporate-portal", description="Overall layout paradigm")
    assumptions_and_limitations: List[str] = Field(default_factory=list)


class AstroComponentCode(BaseModel):
    filename: str = Field(..., description="Base filename (e.g. Header.astro)")
    path: str = Field(..., description="Relative path in project (e.g. src/components/Header.astro)")
    content: str = Field(..., description="Complete Astro component code")
    is_layout: bool = Field(default=False)
    description: Optional[str] = None


class SanitySchemaDefinition(BaseModel):
    schema_name: str = Field(..., description="Name of the schema type (e.g. homepage, sector)")
    title: str = Field(..., description="Human readable title in Sanity Studio")
    fields: List[Dict[str, Any]] = Field(default_factory=list)
    schema_code: str = Field(..., description="JavaScript / TypeScript schema definition for Sanity")


class AstroProjectManifest(BaseModel):
    project_id: str
    version: int = Field(default=1)
    project_name: str = Field(default="RDGCC Generated Portal")
    output_directory: str
    components: List[AstroComponentCode] = Field(default_factory=list)
    structured_content_file: str = Field(..., description="Content of src/data/homepage.js")
    sanity_schemas: List[SanitySchemaDefinition] = Field(default_factory=list)
    global_css: str = Field(..., description="Content of src/styles/global.css")
    package_json: str
    astro_config: str
    build_valid: bool = Field(default=True)
    validation_errors: List[str] = Field(default_factory=list)
    assumptions: List[str] = Field(default_factory=list)


class DesignInputRequest(BaseModel):
    file_path: Optional[str] = None
    figma_url: Optional[str] = None
    project_name: Optional[str] = "RDGCC Corporate Website"
    demo_mode: bool = False
