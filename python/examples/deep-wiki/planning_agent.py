import os
from pathlib import Path
from typing import List, Dict, Set
import yaml
import attrs
from read_file import FileReader
from mofa.utils.ai.conn import structor_llm

# =====================
# Data Models using attrs.define
# =====================
@attrs.define
class CodeAnalysis:
    file_path: Path
    dependencies: List[Path]
    purpose: str
    category: str  # one of: "entry", "core", "support", "test"
    functions: List[Dict[str, str]]  # e.g. [{"name": str, "description": str}]

@attrs.define
class SubPlan:
    entry_point: Path
    analysis: CodeAnalysis
    related_files: List[Path]

@attrs.define
class Documentation:
    project_structure: Dict
    core_modules: List[Dict]
    execution_flows: List[Dict]
    architecture_diagram: str

# =====================
# Project Planner Implementation
# =====================
class ProjectPlanner:
    def __init__(self, project_root: Path, max_entry_points: int = 3, max_recursion_depth: int = 3):
        self.project_root = project_root
        self.max_entry_points = max_entry_points
        self.max_recursion_depth = max_recursion_depth
        self.file_reader = FileReader(project_root)
        # Cache of analyzed files to avoid repeated LLM calls.
        self.analyzed_files_cache: Set[Path] = set()

    def get_readme_content(self) -> str:
        """Read the project README content."""
        readme_path = self.project_root / "README.md"
        if readme_path.exists():
            return self.file_reader.read_file_content(readme_path)
        return ""

    def find_entry_points(self) -> List[Path]:
        """
        Identify entry files based on the project file tree and README hints.
        Entry files are typically named "main.py", "app.py", "index.js", etc.
        Returns up to max_entry_points paths.
        """
        file_list = self.file_reader.generate_file_tree(max_depth=3)
        candidates = []
        for f in file_list:
            path = Path(f['path'])
            # Basic matching for typical entry filenames or if the file stem equals its parent directory name.
            if path.name in ["main.py", "app.py", "index.js"]:
                candidates.append(path)
            elif path.stem == path.parent.name:
                candidates.append(path)
        # Optionally, further filter using keywords found in the README content.
        return sorted(candidates)[:self.max_entry_points]

    def analyze_file(self, file_path: Path) -> CodeAnalysis:
        """
        Call LLM to analyze a given file and extract:
         - Dependency file paths (relative to project root)
         - 50-100 words description of its main functionality
         - Important function names with their descriptions
         - Classification (entry, core, support, test)
        """
        code_content = self.file_reader.read_file_content(file_path)
        prompt = f"""
        Based on the project's README and overall structure, please analyze the following code file.
        
        File Path: {file_path}
        Code Snippet:
        {code_content}
        
        Requirements:
        1. List all dependency file paths (relative to the project root).
        2. Provide a 50-100 word description of the file's main functionality.
        3. Identify important functions and explain their roles.
        4. Classify the file as one of: entry, core, support, test.
        """
        response = structor_llm(
            messages=[
                {"role": "system", "content": "You are an expert technical documentation engineer."},
                {"role": "user", "content": prompt}
            ],
            response_model=CodeAnalysis
        )
        return response

    def create_subplan(self, entry_point: Path) -> SubPlan:
        """Generate a subplan for an entry file by analyzing it and collecting its dependency files."""
        analysis = self.analyze_file(entry_point)
        # Convert dependency strings to absolute Paths and filter those that exist.
        related_files = [
            self.project_root / dep 
            for dep in analysis.dependencies 
            if (self.project_root / dep).exists()
        ]
        self.analyzed_files_cache.add(entry_point)
        return SubPlan(entry_point, analysis, related_files)

    def analyze_dependencies(self, plan: SubPlan, current_depth: int = 1):
        """
        Recursively analyze dependency files referenced in the subplan.
        Stops recursion when max_recursion_depth is reached.
        """
        if current_depth > self.max_recursion_depth:
            return
        for fp in plan.related_files:
            if fp not in self.analyzed_files_cache:
                analysis = self.analyze_file(fp)
                self.analyzed_files_cache.add(fp)
                # Create a temporary subplan to recursively analyze new dependencies.
                new_plan = SubPlan(
                    entry_point=fp,
                    analysis=analysis,
                    related_files=[
                        self.project_root / dep 
                        for dep in analysis.dependencies 
                        if (self.project_root / dep).exists()
                    ]
                )
                self.analyze_dependencies(new_plan, current_depth + 1)

    def compile_documentation(self, entry_points: List[Path], subplans: List[SubPlan], analyses: List[CodeAnalysis]) -> Documentation:
        """
        Combine the README, entry points, subplans, and file analysis results into a structured documentation.
        This includes:
          - Project structure (from README and file tree)
          - Core modules with main functionality and classification
          - Execution flows as Mermaid flowcharts
          - An architecture diagram from a main entry point to illustrate code flow and dependencies
        """
        structure = {
            "readme": self.get_readme_content(),
            "entry_points": [str(p) for p in entry_points],
            "modules": self._get_module_structure()
        }
        core_modules = [
            {
                "path": str(a.file_path),
                "purpose": a.purpose,
                "category": a.category
            }
            for a in analyses if a.category in ["entry", "core"]
        ]
        execution_flows = [self._generate_flow_diagram(plan) for plan in subplans]
        architecture_diagram = self._generate_architecture_diagram(subplans[0]) if subplans else ""
        return Documentation(structure, core_modules, execution_flows, architecture_diagram)

    def _get_module_structure(self) -> Dict:
        """Placeholder: Define a detailed module structure here if needed."""
        return {"modules": "Module structure details can be added here."}

    def _generate_flow_diagram(self, plan: SubPlan) -> Dict:
        """
        Generate a Mermaid flowchart for a subplan.
        Shows the main entry file and its related dependency files.
        """
        lines = ["flowchart TD"]
        lines.append(f"    {plan.entry_point.stem}[{plan.entry_point.name}]")
        for fp in plan.related_files:
            lines.append(f"    {plan.entry_point.stem} --> {fp.stem}[{fp.name}]")
        return {"entry_point": str(plan.entry_point), "flow": "\n".join(lines)}

    def _generate_architecture_diagram(self, plan: SubPlan) -> str:
        """
        Generate an architecture diagram from a main entry file.
        This diagram illustrates the main code explanation and the flow of function calls and dependencies.
        """
        lines = ["graph TD"]
        lines.append(f"    subgraph {plan.entry_point.stem}_Architecture")
        lines.append(f"        {plan.entry_point.stem}[Main: {plan.entry_point.name}]")
        for fp in plan.related_files:
            lines.append(f"        {fp.stem}[{fp.name}]")
            lines.append(f"        {plan.entry_point.stem} --> {fp.stem}")
        lines.append("    end")
        return "\n".join(lines)

    def generate_full_plan(self) -> Documentation:
        """
        Main planning flow:
         1. Identify entry files from the project structure and README.
         2. For each entry file, generate a subplan using LLM analysis.
         3. Recursively analyze dependency files referenced in each subplan.
         4. Compile all analysis results into a structured documentation.
        """
        entry_points = self.find_entry_points()
        subplans = [self.create_subplan(ep) for ep in entry_points]
        for plan in subplans:
            self.analyze_dependencies(plan)
        # Gather analysis results from the entry files.
        all_analyses = [self.analyze_file(ep) for ep in entry_points]
        return self.compile_documentation(entry_points, subplans, all_analyses)


# =====================
# Usage Example
# =====================
if __name__ == "__main__":
    project_path = Path("/Users/chenzi/chenzi/project/zcbc/mofa/python/examples/deep-wiki")
    planner = ProjectPlanner(project_path)
    documentation = planner.generate_full_plan()
    
    # Save the generated documentation to a YAML file.
    with open("project_docs.yaml", "w", encoding="utf-8") as f:
        yaml.dump({
            "project_structure": documentation.project_structure,
            "core_modules": documentation.core_modules,
            "execution_flows": documentation.execution_flows,
            "architecture_diagram": documentation.architecture_diagram
        }, f, allow_unicode=True)