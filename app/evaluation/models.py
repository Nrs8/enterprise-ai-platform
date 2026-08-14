from dataclasses import dataclass



@dataclass
class EvaluationCase:

    id: str

    input: str

    expected: str





@dataclass
class EvaluationResult:

    case_id: str

    input: str

    expected: str

    response: str

    score: float





@dataclass
class EvaluationReport:

    total_cases: int

    passed_cases: int

    failed_cases: int

    accuracy: float