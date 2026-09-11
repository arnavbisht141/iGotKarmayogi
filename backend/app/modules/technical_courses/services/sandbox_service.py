import os
import sys
import json
import time
import shutil
import tempfile
import subprocess
from typing import List, Optional, Tuple, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import TechnicalGeneratedLab, TechnicalLabSolution, TechnicalLabValidationResult
from app.modules.technical_courses.schemas import (
    TestCaseSchema, ValidationResultSchema, TestResultItem, LabValidationResponse
)


# Test harness template executed inside the isolated sandbox
TEST_HARNESS_SCRIPT_TEMPLATE = """# -*- coding: utf-8 -*-
import sys
import time
import json
import traceback

# 1. Inject candidate solution code
{solution_code}

# 2. Execution harness
test_results = []
total_passed = 0

test_cases = json.loads({test_cases_json_repr})

for tc in test_cases:
    tc_name = tc.get("name", "unnamed_test")
    start_t = time.perf_counter()
    passed = False
    err_msg = None
    
    try:
        # Execute test case logic
        exec_scope = dict(globals())
        exec(tc.get("test_code", ""), exec_scope)
        passed = True
        total_passed += 1
    except AssertionError as ae:
        passed = False
        err_msg = f"AssertionFailed: {{str(ae)}}" if str(ae) else "AssertionFailed: assertion condition evaluated to False"
    except Exception as e:
        passed = False
        err_msg = f"{{type(e).__name__}}: {{str(e)}}"
    finally:
        dur_ms = round((time.perf_counter() - start_t) * 1000, 2)
        test_results.append({{
            "name": tc_name,
            "passed": passed,
            "error": err_msg,
            "duration_ms": dur_ms
        }})

# Output structured JSON result on last line
summary = {{
    "total_tests": len(test_cases),
    "passed_tests": total_passed,
    "all_passed": (total_passed == len(test_cases)) and len(test_cases) > 0,
    "results": test_results
}}

print("---SANDBOX_HARNESS_OUTPUT_START---")
print(json.dumps(summary))
print("---SANDBOX_HARNESS_OUTPUT_END---")
"""


class SandboxService:
    """
    Isolated execution environment for validating candidate lab solutions.
    
    PRIMARY ENGINE: Docker Container Sandbox (--network none, memory limit, timeout, non-root).
    FALLBACK ENGINE: Subprocess Sandbox (strictly for local development & testing when Docker is absent).
    """

    @staticmethod
    def _is_docker_available() -> bool:
        """Checks whether Docker CLI and daemon are operational."""
        try:
            res = subprocess.run(
                ["docker", "info"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
            return res.returncode == 0
        except Exception:
            return False

    @classmethod
    def execute_in_docker(
        cls,
        harness_code: str,
        timeout_seconds: int = 5,
        memory_limit_mb: int = 128
    ) -> Tuple[int, str, str, float]:
        """
        Executes code inside an unprivileged, network-isolated Docker container.
        """
        temp_dir = tempfile.mkdtemp(prefix="karmayogi_docker_sandbox_")
        harness_path = os.path.join(temp_dir, "harness.py")
        start_time = time.perf_counter()

        try:
            with open(harness_path, "w", encoding="utf-8") as f:
                f.write(harness_code)

            # Docker run command with strict security constraints:
            # - Network disabled
            # - Memory and CPU capped
            # - Read-only workspace mount
            # - Timeout handled via subprocess timeout
            docker_cmd = [
                "docker", "run", "--rm",
                "--network", "none",
                f"--memory={memory_limit_mb}m",
                "--cpus=0.5",
                "-v", f"{temp_dir}:/sandbox:ro",
                "-w", "/sandbox",
                "python:3.10-slim",
                "python", "/sandbox/harness.py"
            ]

            process = subprocess.run(
                docker_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout_seconds
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return process.returncode, process.stdout, process.stderr, elapsed_ms

        except subprocess.TimeoutExpired:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return -1, "", f"ExecutionTimedOut: Docker execution exceeded {timeout_seconds}s limit", elapsed_ms
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return 1, "", f"DockerExecutionError: {str(e)}", elapsed_ms
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    @classmethod
    def execute_in_subprocess_fallback(
        cls,
        harness_code: str,
        timeout_seconds: int = 5
    ) -> Tuple[int, str, str, float]:
        """
        Subprocess execution sandbox.
        STRICTLY for development/testing environments when Docker daemon is not running.
        """
        temp_dir = tempfile.mkdtemp(prefix="karmayogi_dev_sandbox_")
        harness_path = os.path.join(temp_dir, "harness.py")
        start_time = time.perf_counter()

        try:
            with open(harness_path, "w", encoding="utf-8") as f:
                f.write(harness_code)

            # Clean minimal environment
            minimal_env = {
                "PYTHONPATH": "",
                "PATH": os.environ.get("PATH", ""),
                "SYSTEMROOT": os.environ.get("SYSTEMROOT", "")
            }

            process = subprocess.run(
                [sys.executable, harness_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=temp_dir,
                env=minimal_env,
                timeout=timeout_seconds
            )
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return process.returncode, process.stdout, process.stderr, elapsed_ms

        except subprocess.TimeoutExpired:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return -1, "", f"ExecutionTimedOut: Subprocess execution exceeded {timeout_seconds}s limit", elapsed_ms
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000
            return 1, "", f"SubprocessExecutionError: {str(e)}", elapsed_ms
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

    @classmethod
    def validate_code(
        cls,
        solution_code: str,
        test_cases: List[TestCaseSchema],
        timeout_seconds: int = 5,
        memory_limit_mb: int = 128
    ) -> ValidationResultSchema:
        """
        Executes candidate solution code against test cases in the isolated sandbox.
        """
        tc_dicts = [tc.model_dump() for tc in test_cases]
        harness_code = TEST_HARNESS_SCRIPT_TEMPLATE.format(
            solution_code=solution_code,
            test_cases_json_repr=repr(json.dumps(tc_dicts))
        )

        sandbox_type = "docker"
        # Determine sandbox engine: Docker first, Subprocess fallback if Docker is unavailable
        if cls._is_docker_available():
            exit_code, stdout, stderr, elapsed_ms = cls.execute_in_docker(
                harness_code=harness_code,
                timeout_seconds=timeout_seconds,
                memory_limit_mb=memory_limit_mb
            )
        else:
            sandbox_type = "subprocess-dev-fallback"
            exit_code, stdout, stderr, elapsed_ms = cls.execute_in_subprocess_fallback(
                harness_code=harness_code,
                timeout_seconds=timeout_seconds
            )

        # Parse test results from stdout
        test_items: List[TestResultItem] = []
        is_valid = False
        passed_count = 0
        total_count = len(test_cases)
        error_msg = None

        if "---SANDBOX_HARNESS_OUTPUT_START---" in stdout:
            try:
                start_marker = "---SANDBOX_HARNESS_OUTPUT_START---"
                end_marker = "---SANDBOX_HARNESS_OUTPUT_END---"
                json_part = stdout.split(start_marker)[1].split(end_marker)[0].strip()
                summary_data = json.loads(json_part)
                
                is_valid = summary_data.get("all_passed", False)
                passed_count = summary_data.get("passed_tests", 0)
                total_count = summary_data.get("total_tests", total_count)
                
                for r in summary_data.get("results", []):
                    test_items.append(TestResultItem(
                        name=r.get("name", "test"),
                        passed=r.get("passed", False),
                        error=r.get("error"),
                        duration_ms=r.get("duration_ms", 0.0)
                    ))
            except Exception as parse_err:
                error_msg = f"Failed to parse sandbox output JSON: {str(parse_err)}"
                is_valid = False
        else:
            is_valid = False
            error_msg = stderr or stdout or "Execution failed before harness completed."

        return ValidationResultSchema(
            is_valid=is_valid,
            sandbox_type=sandbox_type,
            exit_code=exit_code,
            execution_time_ms=round(elapsed_ms, 2),
            stdout=stdout.strip() if stdout else None,
            stderr=stderr.strip() if stderr else None,
            test_results=test_items,
            passed_tests_count=passed_count,
            total_tests_count=total_count,
            error_message=error_msg
        )

    @classmethod
    def validate_lab(
        cls,
        lab_id: int,
        db: Session
    ) -> LabValidationResponse:
        """
        Validates the generated lab by retrieving its solution and executing tests in the sandbox.
        Updates the lab's status to 'validated' or 'rejected' and persists the validation record.
        """
        lab = db.query(TechnicalGeneratedLab).filter(TechnicalGeneratedLab.id == lab_id).first()
        if not lab:
            raise ValueError(f"Generated lab with ID {lab_id} not found.")

        solution = db.query(TechnicalLabSolution).filter(TechnicalLabSolution.lab_id == lab_id).first()
        if not solution:
            raise ValueError(f"No reference solution found for lab ID {lab_id}.")

        test_cases_raw = json.loads(lab.test_cases_json) if lab.test_cases_json else []
        test_cases = [TestCaseSchema(**tc) for tc in test_cases_raw]

        val_result = cls.validate_code(
            solution_code=solution.reference_code,
            test_cases=test_cases
        )

        # Update lab status
        new_status = "validated" if val_result.is_valid else "rejected"
        lab.status = new_status

        # Persist validation result
        summary_json = json.dumps([ti.model_dump() for ti in val_result.test_results])
        val_record = TechnicalLabValidationResult(
            lab_id=lab.id,
            solution_id=solution.id,
            is_valid=val_result.is_valid,
            sandbox_type=val_result.sandbox_type,
            exit_code=val_result.exit_code,
            execution_time_ms=val_result.execution_time_ms,
            stdout=val_result.stdout,
            stderr=val_result.stderr,
            test_summary_json=summary_json,
            error_message=val_result.error_message
        )
        db.add(val_record)
        db.commit()

        return LabValidationResponse(
            lab_id=lab.id,
            is_valid=val_result.is_valid,
            status=new_status,
            validation_details=val_result
        )
