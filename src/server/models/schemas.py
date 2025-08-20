from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime
from .enums import TargetType, AttackPhase, AttackStatus, TechnologyStack, PayloadType, ErrorType, RecoveryAction

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True

class TargetProfile(BaseSchema):
    """Comprehensive target analysis profile for intelligent decision making"""
    target: str
    target_type: TargetType = TargetType.UNKNOWN
    ip_addresses: List[str] = Field(default_factory=list)
    open_ports: List[int] = Field(default_factory=list)
    services: Dict[int, str] = Field(default_factory=dict)
    technologies: List[TechnologyStack] = Field(default_factory=list)
    cms_type: Optional[str] = None
    cloud_provider: Optional[str] = None
    security_headers: Dict[str, str] = Field(default_factory=dict)
    ssl_info: Dict[str, Any] = Field(default_factory=dict)
    subdomains: List[str] = Field(default_factory=list)
    endpoints: List[str] = Field(default_factory=list)
    attack_surface_score: float = 0.0
    risk_level: str = "unknown"
    confidence_score: float = 0.0

class AttackStep(BaseSchema):
    """Individual step in an attack chain"""
    tool: str
    parameters: Dict[str, Any]
    expected_outcome: str
    success_probability: float
    execution_time_estimate: int  # seconds
    dependencies: List[str] = Field(default_factory=list)

class AttackChain(BaseSchema):
    """Represents a sequence of attacks for maximum impact"""
    target_profile: TargetProfile
    steps: List[AttackStep] = Field(default_factory=list)
    success_probability: float = 0.0
    estimated_time: int = 0
    required_tools: List[str] = Field(default_factory=list)
    risk_level: str = "unknown"

class ToolEffectiveness(BaseSchema):
    tool_name: str
    target_type: TargetType
    effectiveness_score: float = Field(..., ge=0.0, le=1.0)
    notes: Optional[str] = None

class AttackPattern(BaseSchema):
    pattern_id: str
    name: str
    target_type: TargetType
    phases: List[AttackPhase]
    recommended_tools: List[str]

class UrlRequest(BaseSchema):
    url: str = Field(..., description="The target URL for the operation")

class CommandRequest(BaseSchema):
    command: str = Field(..., description="The command for the operation")

class FileRequest(BaseSchema):
    path: str = Field(..., description="The path to the file or directory")

class FileContentRequest(FileRequest):
    content: str = Field(..., description="The content to write to the file")

class PayloadRequest(BaseSchema):
    payload_type: PayloadType = Field(PayloadType.RANDOM, description="The type of payload to generate")
    size_kb: int = Field(1, ge=1, le=10240, description="The size of the payload in kilobytes")
    custom_char: Optional[str] = Field(None, max_length=1, description="A custom character to use for the payload")

class VulnerabilityCardRequest(BaseSchema):
    title: str
    cve: str
    severity: str
    summary: str
    recommendation: str

class SummaryReportRequest(BaseSchema):
    title: str
    summary_points: List[str]
    metrics: Dict[str, Any]

class ToolOutputRequest(BaseSchema):
    tool_name: str
    output: str

class SelectToolRequest(BaseSchema):
    target_profile: TargetProfile
    phase: str

class GetAttackPatternRequest(BaseSchema):
    target_type: TargetType

class OptimizeParametersRequest(BaseSchema):
    tool_name: str
    target_profile: TargetProfile

class BugBountyScanRequest(BaseSchema):
    url: str
    tools: List[str]


class RecoveryStrategy(BaseSchema):
    """Recovery strategy with configuration"""
    action: RecoveryAction
    parameters: Dict[str, Any]
    max_attempts: int
    backoff_multiplier: float
    success_probability: float
    estimated_time: int  # seconds


class ErrorContext(BaseSchema):
    """Context information for error handling decisions"""
    tool_name: str
    target: str
    parameters: Dict[str, Any]
    error_type: ErrorType
    error_message: str
    attempt_count: int
    timestamp: datetime
    stack_trace: str
    system_resources: Dict[str, Any]
    exit_code: Optional[int] = None
    previous_errors: List['ErrorContext'] = Field(default_factory=list)


class TechnologyDetectionRequest(BaseSchema):
    """Request model for technology detection"""
    headers: Optional[Dict[str, str]] = None
    content: Optional[str] = None
    ports: Optional[List[int]] = None


class RateLimitDetectionRequest(BaseSchema):
    """Request model for rate limit detection"""
    response_text: str
    status_code: int
    headers: Optional[Dict[str, str]] = None


class RateLimitDetectionResponse(BaseSchema):
    """Response model for rate limit detection"""
    detected: bool
    confidence: float
    indicators: List[str]
    recommended_profile: str


class TimingAdjustmentRequest(BaseSchema):
    """Request model for timing adjustment"""
    current_params: Dict[str, Any]
    profile: str


class FailureAnalysisRequest(BaseSchema):
    """Request model for failure analysis"""
    error_output: str
    exit_code: int


class FailureAnalysisResponse(BaseSchema):
    """Response model for failure analysis"""
    failure_type: str
    confidence: float
    recovery_strategies: List[str]
    alternative_tools: List[str]


class CTFChallenge(BaseModel):
    """Model for a CTF challenge."""
    name: str = Field(..., description="The name of the challenge.")
    category: str = Field(..., description="The category of the challenge (e.g., web, crypto)." )
    description: str = Field(..., description="A description of the challenge.")
    target: Optional[str] = Field(None, description="The target for the challenge (e.g., URL, IP address).")


class ChallengeStep(BaseModel):
    """Model for a single step in a challenge solution workflow."""
    step: int
    action: str
    success: bool
    output: str
    tools_used: List[str]
    execution_time: float
    artifacts: List[str]


class ManualGuidance(BaseModel):
    """Model for manual guidance steps."""
    action: str
    description: str


class ChallengeSolution(BaseModel):
    """Model for the result of an automated challenge solve attempt."""
    challenge_id: str
    status: str
    automated_steps: List[ChallengeStep]
    manual_steps: List[ManualGuidance]
    confidence: float
    estimated_completion: int
    artifacts: List[str]
    flag_candidates: List[str]
    next_actions: List[str]
    flag: Optional[str] = None
    error: Optional[str] = None
