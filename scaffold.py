import os

repo_dir = r"c:\Users\arhaa\OneDrive\poc1\psse-agentic-ai"

directories = [
    "app/orchestrator",
    "app/cli",
    "app/intent",
    "app/topology",
    "app/ir",
    "app/validation",
    "app/layout",
    "app/psse",
    "app/hitl",
    "app/verification",
    "app/artifacts",
    "app/logging",
    "app/utils",
    "outputs/runs/stage0",
    "tests/golden",
    "tests/topology",
    "tests/validation",
    "tests/layout",
    "tests/psse",
    "docs"
]

files = {
    "app/__init__.py": '"""Root app module."""',
    "app/orchestrator/__init__.py": '"""Orchestrator module."""',
    "app/orchestrator/orchestrator.py": '"""Placeholder for future orchestrator."""',
    "app/cli/__init__.py": '"""CLI module."""',
    "app/intent/__init__.py": '"""Intent parsing module."""',
    "app/intent/extractor.py": '"""Placeholder for intent extractor."""',
    "app/intent/prompt_templates.py": '"""Placeholder for prompt templates."""',
    "app/intent/schema.py": '"""Placeholder for intent schema."""',
    "app/topology/__init__.py": '"""Topology module."""',
    "app/topology/planner.py": '"""Placeholder for topology planner."""',
    "app/topology/templates.py": '"""Placeholder for topology templates."""',
    "app/topology/numbering.py": '"""Placeholder for topology numbering logic."""',
    "app/topology/graph_builder.py": '"""Placeholder for topology graph builder."""',
    "app/ir/__init__.py": '"""IR module."""',
    "app/ir/topology_ir.py": '"""Placeholder for topology IR."""',
    "app/ir/component_models.py": '"""Placeholder for IR component models."""',
    "app/ir/serializers.py": '"""Placeholder for IR serializers."""',
    "app/validation/__init__.py": '"""Validation module."""',
    "app/validation/validator.py": '"""Placeholder for validator."""',
    "app/validation/checks.py": '"""Placeholder for validation checks."""',
    "app/validation/validation_models.py": '"""Placeholder for validation models."""',
    "app/layout/__init__.py": '"""Layout module."""',
    "app/layout/engine.py": '"""Placeholder for layout engine."""',
    "app/layout/routing.py": '"""Placeholder for routing logic."""',
    "app/layout/collision.py": '"""Placeholder for collision detection."""',
    "app/layout/svg_export.py": '"""Placeholder for SVG export."""',
    "app/psse/__init__.py": '"""PSSE module."""',
    "app/psse/diagram.py": '"""Placeholder for diagram placement."""',
    "app/psse/powerflow.py": '"""Placeholder for advanced powerflow."""',
    "app/hitl/__init__.py": '"""HITL module."""',
    "app/hitl/approval.py": '"""Placeholder for HITL approval."""',
    "app/verification/__init__.py": '"""Verification module."""',
    "app/verification/verifier.py": '"""Placeholder for verifier."""',
    "app/verification/diagnostics.py": '"""Placeholder for diagnostics."""',
    "app/artifacts/__init__.py": '"""Artifacts module."""',
    "app/artifacts/artifact_manager.py": '"""Placeholder for artifact manager."""',
    "app/artifacts/exporters.py": '"""Placeholder for artifact exporters."""',
    "app/logging/__init__.py": '"""Logging module."""',
    "app/logging/logger.py": '"""Placeholder for structured logger."""',
    "app/logging/execution_trace.py": '"""Placeholder for execution trace."""',
    "app/utils/__init__.py": '"""Utils module."""',
    "app/utils/exceptions.py": '"""Placeholder for exceptions."""',
    "app/utils/constants.py": '"""Placeholder for constants."""',
    "app/utils/helpers.py": '"""Placeholder for helpers."""',
    "tests/__init__.py": '"""Tests module."""',
    "docs/architecture.md": "<!-- Architecture document placeholder -->",
    "docs/ir_schema.md": "<!-- IR Schema document placeholder -->",
    "docs/decisions.md": "<!-- Decisions document placeholder -->"
}

for d in directories:
    os.makedirs(os.path.join(repo_dir, d), exist_ok=True)

for rel_path, content in files.items():
    full_path = os.path.join(repo_dir, rel_path)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content + "\\n")

print("Scaffolding complete.")
