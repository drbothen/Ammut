from enum import Enum

class TargetType(str, Enum):
    """Enumeration of different target types for intelligent analysis"""
    WEB_APPLICATION = "web_application"
    NETWORK_HOST = "network_host"
    API_ENDPOINT = "api_endpoint"
    CLOUD_SERVICE = "cloud_service"
    MOBILE_APP = "mobile_app"
    BINARY_FILE = "binary_file"
    IOT = "iot"
    UNKNOWN = "unknown"

class TechnologyStack(str, Enum):
    """Common technology stacks for targeted testing"""
    APACHE = "apache"
    NGINX = "nginx"
    IIS = "iis"
    NODEJS = "nodejs"
    PHP = "php"
    PYTHON = "python"
    JAVA = "java"
    DOTNET = "dotnet"
    WORDPRESS = "wordpress"
    DRUPAL = "drupal"
    JOOMLA = "joomla"
    REACT = "react"
    ANGULAR = "angular"
    VUE = "vue"
    UNKNOWN = "unknown"

class AttackPhase(str, Enum):
    RECONNAISSANCE = "reconnaissance"
    SCANNING = "scanning"
    GAINING_ACCESS = "gaining_access"
    MAINTAINING_ACCESS = "maintaining_access"
    COVERING_TRACKS = "covering_tracks"

class AttackStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

class ToolCategory(str, Enum):
    SCANNER = "scanner"
    EXPLOITATION = "exploitation"
    RECON = "recon"
    BRUTEFORCE = "bruteforce"
    WEB = "web"
    NETWORK = "network"
    CLOUD = 'cloud'

class OperatingSystem(str, Enum):
    LINUX = "linux"
    WINDOWS = "windows"
    MACOS = "macos"
    UNKNOWN = "unknown"

class Framework(str, Enum):
    DJANGO = "django"
    FLASK = "flask"
    RAILS = "rails"
    NODEJS = "nodejs"
    SPRING = "spring"
    UNKNOWN = "unknown"

class CloudProvider(str, Enum):
    AWS = "aws"
    GCP = "gcp"
    AZURE = "azure"

class PayloadType(str, Enum):
    RANDOM = "random"
    CUSTOM = "custom"
    UNKNOWN = "unknown"


class ErrorType(str, Enum):
    """Enumeration of different error types for intelligent handling"""
    TIMEOUT = "timeout"
    PERMISSION_DENIED = "permission_denied"
    NETWORK_UNREACHABLE = "network_unreachable"
    RATE_LIMITED = "rate_limited"
    TOOL_NOT_FOUND = "tool_not_found"
    INVALID_PARAMETERS = "invalid_parameters"
    RESOURCE_EXHAUSTED = "resource_exhausted"
    AUTHENTICATION_FAILED = "authentication_failed"
    TARGET_UNREACHABLE = "target_unreachable"
    PARSING_ERROR = "parsing_error"
    UNKNOWN = "unknown"


class RecoveryAction(str, Enum):
    """Types of recovery actions that can be taken"""
    RETRY_WITH_BACKOFF = "retry_with_backoff"
    RETRY_WITH_REDUCED_SCOPE = "retry_with_reduced_scope"
    SWITCH_TO_ALTERNATIVE_TOOL = "switch_to_alternative_tool"
    ADJUST_PARAMETERS = "adjust_parameters"
    ESCALATE_TO_HUMAN = "escalate_to_human"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    ABORT_OPERATION = "abort_operation"
