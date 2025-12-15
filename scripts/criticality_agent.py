#!/usr/bin/env python3
"""
Criticality Management Agent

Automated agent for managing project criticalities:
- Analyzes CRITICITA.md
- Creates priority-based execution plan
- Tracks resolution progress
- Generates reports and suggestions

Usage:
    python scripts/criticality_agent.py report          # Generate full report
    python scripts/criticality_agent.py summary         # Quick summary
    python scripts/criticality_agent.py next            # Get next task to work on
    python scripts/criticality_agent.py resolve <id>    # Mark criticality as resolved
    python scripts/criticality_agent.py roadmap         # Generate resolution roadmap
"""

import re
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from enum import Enum
from dataclasses import dataclass, asdict


class Priority(Enum):
    """Criticality priority levels"""
    CRITICAL = ("🔴", "CRITICA", 1)
    HIGH = ("🟡", "MEDIA", 2)
    LOW = ("🟢", "MINORE", 3)
    RESOLVED = ("✅", "RISOLTE", 4)

    def __init__(self, emoji, label, rank):
        self.emoji = emoji
        self.label = label
        self.rank = rank


@dataclass
class Criticality:
    """Represents a single criticality"""
    id: str
    number: int
    title: str
    priority: Priority
    category: str
    files: List[str]
    status: str
    effort_hours: float
    description: str
    impact: str
    solution: str
    blocked: bool = False
    blocker_reason: str = ""

    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        data = asdict(self)
        data['priority'] = self.priority.label
        return data


class CriticalityAgent:
    """
    Agent for managing project criticalities

    Responsibilities:
    - Parse CRITICITA.md file
    - Prioritize criticalities
    - Track resolution progress
    - Generate actionable reports
    """

    def __init__(self, criticita_path: Path = None, state_path: Path = None):
        """
        Initialize agent

        Args:
            criticita_path: Path to CRITICITA.md file
            state_path: Path to state tracking JSON file
        """
        self.project_root = Path(__file__).parent.parent
        self.criticita_path = criticita_path or self.project_root / "CRITICITA.md"
        self.state_path = state_path or self.project_root / ".criticality_state.json"

        self.criticalities: List[Criticality] = []
        self.state: Dict = {}

        self._load_state()
        self._parse_criticita()

    def _load_state(self):
        """Load agent state from JSON file"""
        if self.state_path.exists():
            with open(self.state_path, 'r', encoding='utf-8') as f:
                self.state = json.load(f)
        else:
            self.state = {
                "last_update": None,
                "resolved_today": [],
                "current_focus": None,
                "history": []
            }

    def _save_state(self):
        """Save agent state to JSON file"""
        self.state["last_update"] = datetime.now().isoformat()
        with open(self.state_path, 'w', encoding='utf-8') as f:
            json.dump(self.state, f, indent=2, ensure_ascii=False)

    def _parse_criticita(self):
        """Parse CRITICITA.md file and extract criticalities"""
        if not self.criticita_path.exists():
            print(f"❌ CRITICITA.md not found at {self.criticita_path}")
            return

        content = self.criticita_path.read_text(encoding='utf-8')

        # Parse critical criticalities (🔴)
        self._parse_section(content, "## 🔴 Criticità Critiche (Alta Priorità)", Priority.CRITICAL)

        # Parse medium criticalities (🟡)
        self._parse_section(content, "## 🟡 Criticità Medie (Media Priorità)", Priority.HIGH)

        # Parse low criticalities (🟢)
        self._parse_section(content, "## 🟢 Criticità Minori (Bassa Priorità)", Priority.LOW)

        # Parse resolved criticalities (✅)
        self._parse_resolved_section(content)

    def _parse_section(self, content: str, section_header: str, priority: Priority):
        """Parse a specific criticality section"""
        # Find section - use better delimiter pattern
        # Match until next section header (## followed by emoji) or end of file
        section_match = re.search(
            rf"{re.escape(section_header)}.*?(?=\n## [🔴🟡🟢✅📊📍🚀📦🎯🔗📈📝]|\Z)",
            content,
            re.DOTALL
        )

        if not section_match:
            return

        section_text = section_match.group(0)

        # Find individual criticalities (### N. Title)
        criticality_pattern = r"### (\d+)\.\s+(.+?)\n\s*\n\*\*Severità\*\*:\s+(.+?)\n\*\*Categoria\*\*:\s+(.+?)\n\*\*File Coinvolti\*\*:\s+(.+?)(?:\n|$)"

        for match in re.finditer(criticality_pattern, section_text, re.DOTALL):
            number = int(match.group(1))
            title = match.group(2).strip()
            category = match.group(4).strip()
            files_str = match.group(5).strip()

            # Extract files
            files = [f.strip().strip('`') for f in files_str.split(',')]

            # Extract full description, status, effort
            crit_text = self._extract_criticality_full_text(content, number)

            description = self._extract_field(crit_text, "#### Problema")
            impact = self._extract_field(crit_text, "#### Impatto")
            solution = self._extract_field(crit_text, "#### Soluzione")
            status = self._extract_status(crit_text)
            effort = self._extract_effort(crit_text)
            blocked, blocker = self._extract_blocked_status(crit_text)

            criticality = Criticality(
                id=f"C{number:03d}",
                number=number,
                title=title,
                priority=priority,
                category=category,
                files=files,
                status=status,
                effort_hours=effort,
                description=description,
                impact=impact,
                solution=solution,
                blocked=blocked,
                blocker_reason=blocker
            )

            self.criticalities.append(criticality)

    def _parse_resolved_section(self, content: str):
        """Parse resolved criticalities section"""
        section_match = re.search(
            r"## ✅ Criticità Risolte.*?(?=##|\Z)",
            content,
            re.DOTALL
        )

        if not section_match:
            return

        section_text = section_match.group(0)

        # Find resolved items (### RN. ✅ Title)
        resolved_pattern = r"### (R\d+)\.\s+✅\s+(.+?)\n"

        for match in re.finditer(resolved_pattern, section_text):
            res_id = match.group(1)
            title = match.group(2).strip()

            # Extract original criticality number if mentioned
            number_match = re.search(r"\(#(\d+)\)", title)
            number = int(number_match.group(1)) if number_match else 0

            criticality = Criticality(
                id=res_id,
                number=number,
                title=title,
                priority=Priority.RESOLVED,
                category="Resolved",
                files=[],
                status="✅ RISOLTO",
                effort_hours=0,
                description="",
                impact="",
                solution=""
            )

            self.criticalities.append(criticality)

    def _extract_criticality_full_text(self, content: str, number: int) -> str:
        """Extract full text of a criticality by number"""
        pattern = rf"### {number}\..+?(?=###|\n##|\Z)"
        match = re.search(pattern, content, re.DOTALL)
        return match.group(0) if match else ""

    def _extract_field(self, text: str, field_header: str) -> str:
        """Extract a field from criticality text"""
        pattern = rf"{re.escape(field_header)}\n\n(.+?)(?=\n####|\n---|\Z)"
        match = re.search(pattern, text, re.DOTALL)
        if match:
            return match.group(1).strip()[:200]  # First 200 chars
        return ""

    def _extract_status(self, text: str) -> str:
        """Extract status from criticality text"""
        pattern = r"#### Status:\s+(.+?)(?:\n|$)"
        match = re.search(pattern, text)
        return match.group(1).strip() if match else "❓ UNKNOWN"

    def _extract_effort(self, text: str) -> float:
        """Extract effort estimation in hours"""
        pattern = r"#### Effort:\s+(.+?)(?:\n|$)"
        match = re.search(pattern, text)
        if match:
            effort_text = match.group(1)
            # Try to extract number of hours
            hours_match = re.search(r"(\d+)\s*ore?", effort_text)
            if hours_match:
                return float(hours_match.group(1))
        return 0.0

    def _extract_blocked_status(self, text: str) -> tuple[bool, str]:
        """Check if criticality is blocked"""
        if "🚧 BLOCCATO" in text or "BLOCCATO" in text:
            # Extract blocker reason
            pattern = r"🚧 \*\*BLOCCATO\*\*\s*\((.+?)\)"
            match = re.search(pattern, text)
            reason = match.group(1) if match else "Unknown blocker"
            return True, reason
        return False, ""

    def get_active_criticalities(self) -> List[Criticality]:
        """Get all active (non-resolved) criticalities"""
        return [c for c in self.criticalities if c.priority != Priority.RESOLVED]

    def get_by_priority(self, priority: Priority) -> List[Criticality]:
        """Get criticalities by priority level"""
        return [c for c in self.criticalities if c.priority == priority]

    def get_next_task(self) -> Optional[Criticality]:
        """
        Get next criticality to work on based on:
        1. Not blocked
        2. Highest priority
        3. Lowest effort (for same priority)
        """
        active = self.get_active_criticalities()

        # Filter out blocked
        available = [c for c in active if not c.blocked]

        if not available:
            return None

        # Sort by priority rank (lower = more critical), then by effort
        available.sort(key=lambda c: (c.priority.rank, c.effort_hours))

        return available[0]

    def generate_summary(self) -> str:
        """Generate quick summary of criticalities"""
        active = self.get_active_criticalities()

        critical = len(self.get_by_priority(Priority.CRITICAL))
        high = len(self.get_by_priority(Priority.HIGH))
        low = len(self.get_by_priority(Priority.LOW))
        resolved = len(self.get_by_priority(Priority.RESOLVED))

        blocked = len([c for c in active if c.blocked])

        total_effort = sum(c.effort_hours for c in active if c.effort_hours > 0)

        # Calculate resolution rate safely
        total_crit = len(self.criticalities)
        resolution_rate = (resolved / total_crit * 100) if total_crit > 0 else 0

        summary = f"""
╔════════════════════════════════════════════════════════════╗
║         CRITICALITY MANAGEMENT AGENT - SUMMARY            ║
╚════════════════════════════════════════════════════════════╝

📊 Current Status:
   🔴 Critical:  {critical:2d}
   🟡 High:      {high:2d}
   🟢 Low:       {low:2d}
   ✅ Resolved:  {resolved:2d}
   ════════════════
   📋 Total Active: {len(active)}

⚠️  Blocked: {blocked}
⏱️  Total Effort: {total_effort:.1f} hours

📈 Progress:
   Resolution Rate: {resolution_rate:.1f}%
   Active vs Target: {len(active)}/3 (target)
"""

        next_task = self.get_next_task()
        if next_task:
            summary += f"""
🎯 Next Recommended Task:
   [{next_task.id}] {next_task.priority.emoji} {next_task.title}
   ⏱️  Effort: {next_task.effort_hours}h | 📂 {next_task.category}
"""

        return summary

    def generate_roadmap(self) -> str:
        """Generate resolution roadmap ordered by priority"""
        active = self.get_active_criticalities()

        # Group by priority
        critical = [c for c in active if c.priority == Priority.CRITICAL]
        high = [c for c in active if c.priority == Priority.HIGH]
        low = [c for c in active if c.priority == Priority.LOW]

        roadmap = """
╔════════════════════════════════════════════════════════════╗
║         CRITICALITY RESOLUTION ROADMAP                     ║
╚════════════════════════════════════════════════════════════╝

"""

        phase = 1

        if critical:
            roadmap += f"📍 PHASE {phase}: Critical Issues (URGENT)\n"
            roadmap += "─" * 60 + "\n"
            for c in sorted(critical, key=lambda x: x.effort_hours):
                blocked_mark = "🚧" if c.blocked else "  "
                roadmap += f"{blocked_mark} [{c.id}] {c.title}\n"
                roadmap += f"    ⏱️  {c.effort_hours}h | 📂 {c.category} | {c.status}\n"
                if c.blocked:
                    roadmap += f"    🚧 BLOCKED: {c.blocker_reason}\n"
                roadmap += f"    📁 Files: {', '.join(c.files[:2])}\n\n"
            phase += 1

        if high:
            roadmap += f"\n📍 PHASE {phase}: High Priority\n"
            roadmap += "─" * 60 + "\n"
            for c in sorted(high, key=lambda x: x.effort_hours):
                blocked_mark = "🚧" if c.blocked else "  "
                roadmap += f"{blocked_mark} [{c.id}] {c.title}\n"
                roadmap += f"    ⏱️  {c.effort_hours}h | 📂 {c.category} | {c.status}\n"
                if c.blocked:
                    roadmap += f"    🚧 BLOCKED: {c.blocker_reason}\n"
                roadmap += f"    📁 Files: {', '.join(c.files[:2])}\n\n"
            phase += 1

        if low:
            roadmap += f"\n📍 PHASE {phase}: Low Priority (Nice to Have)\n"
            roadmap += "─" * 60 + "\n"
            for c in sorted(low, key=lambda x: x.effort_hours):
                blocked_mark = "🚧" if c.blocked else "  "
                roadmap += f"{blocked_mark} [{c.id}] {c.title}\n"
                roadmap += f"    ⏱️  {c.effort_hours}h | 📂 {c.category} | {c.status}\n"
                roadmap += f"    📁 Files: {', '.join(c.files[:2])}\n\n"

        total_effort = sum(c.effort_hours for c in active if c.effort_hours > 0)
        roadmap += f"\n💡 Total Estimated Effort: {total_effort:.1f} hours\n"

        return roadmap

    def generate_mapping_table(self) -> str:
        """Generate mapping table: Criticality → Files → Priority → Status"""
        active = self.get_active_criticalities()

        table = """
╔════════════════════════════════════════════════════════════════════════════╗
║                    CRITICALITY MAPPING TABLE                               ║
╚════════════════════════════════════════════════════════════════════════════╝

"""

        # Header
        table += f"{'ID':<8} {'Priority':<10} {'Title':<30} {'Files':<20} {'Status':<15}\n"
        table += "─" * 100 + "\n"

        # Sort by priority then by number
        sorted_crit = sorted(active, key=lambda c: (c.priority.rank, c.number))

        for c in sorted_crit:
            files_str = c.files[0] if c.files else "N/A"
            if len(files_str) > 18:
                files_str = files_str[:15] + "..."

            title_str = c.title[:28] + "..." if len(c.title) > 30 else c.title

            status_str = c.status.replace("**", "")[:13]

            table += f"{c.id:<8} {c.priority.emoji} {c.priority.label:<7} {title_str:<30} {files_str:<20} {status_str:<15}\n"

            # Show additional files if any
            if len(c.files) > 1:
                for extra_file in c.files[1:3]:
                    if len(extra_file) > 18:
                        extra_file = extra_file[:15] + "..."
                    table += f"{'':8} {'':10} {'':30} → {extra_file:<20}\n"

        return table

    def generate_full_report(self) -> str:
        """Generate complete report with all information"""
        report = f"""
{'='*80}
                    CRITICALITY MANAGEMENT AGENT
                         FULL REPORT
                    {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*80}

"""
        report += self.generate_summary()
        report += "\n\n"
        report += self.generate_mapping_table()
        report += "\n\n"
        report += self.generate_roadmap()

        return report

    def mark_resolved(self, crit_id: str, notes: str = ""):
        """Mark a criticality as resolved"""
        # Find criticality
        crit = next((c for c in self.criticalities if c.id == crit_id), None)

        if not crit:
            print(f"❌ Criticality {crit_id} not found")
            return False

        if crit.priority == Priority.RESOLVED:
            print(f"✅ Criticality {crit_id} already resolved")
            return True

        # Update state
        self.state["resolved_today"].append({
            "id": crit_id,
            "title": crit.title,
            "timestamp": datetime.now().isoformat(),
            "notes": notes
        })

        self.state["history"].append({
            "action": "resolve",
            "criticality_id": crit_id,
            "timestamp": datetime.now().isoformat()
        })

        self._save_state()

        print(f"✅ Criticality {crit_id} marked as resolved!")
        print(f"   📝 Remember to update CRITICITA.md manually")

        return True

    def commit_fix(self, crit_id: str, additional_notes: str = ""):
        """
        Smart commit for criticality fix

        Generates commit message, stages files, and commits
        """
        import subprocess

        # Find criticality
        crit = next((c for c in self.criticalities if c.id == crit_id), None)

        if not crit:
            print(f"❌ Criticality {crit_id} not found")
            return False

        if crit.priority == Priority.RESOLVED:
            print(f"⚠️  Criticality {crit_id} already marked as resolved")
            response = input("Continue with commit anyway? (y/n): ").strip().lower()
            if response != 'y':
                print("❌ Commit cancelled")
                return False

        # Show criticality info
        print(f"\n{'='*70}")
        print(f"📝 COMMITTING FIX FOR CRITICALITY")
        print(f"{'='*70}\n")
        print(f"ID:       {crit.id}")
        print(f"Priority: {crit.priority.emoji} {crit.priority.label}")
        print(f"Title:    {crit.title}")
        print(f"Category: {crit.category}")
        print(f"\nFiles involved:")
        for f in crit.files:
            print(f"  📁 {f}")

        # Check git status
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                check=True
            )

            if not result.stdout.strip():
                print("\n⚠️  No changes detected in git working tree")
                print("Make sure you've saved your changes!")
                return False

            print(f"\n📋 Git Status:")
            print(result.stdout)

        except subprocess.CalledProcessError as e:
            print(f"❌ Git error: {e}")
            return False

        # Generate commit message
        commit_msg = self._generate_commit_message(crit, additional_notes)

        print(f"\n💬 Generated Commit Message:")
        print(f"{'─'*70}")
        print(commit_msg)
        print(f"{'─'*70}")

        # Ask for confirmation
        print(f"\n❓ Actions to perform:")
        print(f"   1. Stage files: {', '.join(crit.files[:3])}")
        if len(crit.files) > 3:
            print(f"      ... and {len(crit.files) - 3} more")
        print(f"   2. Commit with generated message")
        print(f"   3. Mark {crit_id} as resolved in agent state")

        response = input(f"\n🚀 Proceed with commit? (y/n): ").strip().lower()

        if response != 'y':
            print("❌ Commit cancelled")
            return False

        # Stage files
        print(f"\n📦 Staging files...")
        try:
            # Stage specified files
            for file in crit.files:
                # Remove backticks if present
                file_clean = file.strip('`')
                try:
                    subprocess.run(
                        ["git", "add", file_clean],
                        capture_output=True,
                        text=True,
                        check=True
                    )
                    print(f"   ✅ Staged: {file_clean}")
                except subprocess.CalledProcessError:
                    print(f"   ⚠️  Could not stage: {file_clean} (file may not exist or have changes)")

            # Also stage CRITICITA.md
            try:
                subprocess.run(
                    ["git", "add", "CRITICITA.md"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                print(f"   ✅ Staged: CRITICITA.md")
            except subprocess.CalledProcessError:
                print(f"   ⚠️  CRITICITA.md not staged (no changes or doesn't exist)")

        except Exception as e:
            print(f"❌ Error staging files: {e}")
            return False

        # Commit
        print(f"\n💾 Creating commit...")
        try:
            result = subprocess.run(
                ["git", "commit", "-m", commit_msg],
                capture_output=True,
                text=True,
                check=True
            )
            print(f"✅ Commit created successfully!")
            print(result.stdout)

        except subprocess.CalledProcessError as e:
            print(f"❌ Commit failed: {e}")
            print(e.stderr)
            return False

        # Mark as resolved
        self.mark_resolved(crit_id, additional_notes or "Committed fix")

        # Show updated summary
        print(f"\n{'='*70}")
        print(f"📊 UPDATED STATUS")
        print(f"{'='*70}")
        print(self.generate_summary())

        print(f"\n✅ SUCCESS! Don't forget to:")
        print(f"   1. Push changes: git push")
        print(f"   2. Update CRITICITA.md (move {crit_id} to Risolte section)")
        print(f"   3. Get next task: python scripts/criticality_agent.py next")

        return True

    def _generate_commit_message(self, crit: Criticality, additional_notes: str = "") -> str:
        """Generate conventional commit message"""
        # Determine commit type based on category
        category_to_type = {
            "Security": "security",
            "Deployment": "build",
            "Quality Assurance": "test",
            "Functionality": "feat",
            "Database Management": "feat",
            "User Experience": "feat",
            "Code Quality": "refactor",
            "Observability": "chore",
            "Configuration": "chore",
            "Distribution": "build",
        }

        commit_type = category_to_type.get(crit.category, "fix")

        # Priority emoji
        priority_marker = {
            Priority.CRITICAL: "🔴",
            Priority.HIGH: "🟡",
            Priority.LOW: "🟢",
        }.get(crit.priority, "")

        # Main message (short title)
        title = crit.title[:60] + "..." if len(crit.title) > 60 else crit.title

        # Construct message
        message = f"{commit_type}: {priority_marker} Fix {crit.id} - {title}\n\n"

        # Add body
        message += f"Resolves criticality {crit.id} ({crit.priority.label})\n"
        message += f"Category: {crit.category}\n\n"

        if crit.description:
            message += f"{crit.description[:200]}...\n\n"

        if additional_notes:
            message += f"Notes: {additional_notes}\n\n"

        # Add files changed
        message += f"Files modified:\n"
        for f in crit.files[:5]:
            message += f"- {f}\n"
        if len(crit.files) > 5:
            message += f"... and {len(crit.files) - 5} more\n"

        # Footer
        message += f"\n🤖 Generated with Criticality Management Agent"

        return message


def main():
    """Main entry point"""
    agent = CriticalityAgent()

    if len(sys.argv) < 2:
        print("Usage: python scripts/criticality_agent.py [command]")
        print("\nCommands:")
        print("  report           - Generate full report")
        print("  summary          - Quick summary")
        print("  roadmap          - Resolution roadmap")
        print("  mapping          - Criticality mapping table")
        print("  next             - Get next task to work on")
        print("  commit <id> [notes] ⭐ - Smart commit (stage + commit + resolve)")
        print("  resolve <id> [notes]   - Mark criticality as resolved (no commit)")
        print("\n⭐ = Recommended for daily workflow")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "report":
        print(agent.generate_full_report())

    elif command == "summary":
        print(agent.generate_summary())

    elif command == "roadmap":
        print(agent.generate_roadmap())

    elif command == "mapping":
        print(agent.generate_mapping_table())

    elif command == "next":
        next_task = agent.get_next_task()
        if next_task:
            print(f"\n🎯 Next Recommended Task:\n")
            print(f"ID:       {next_task.id}")
            print(f"Priority: {next_task.priority.emoji} {next_task.priority.label}")
            print(f"Title:    {next_task.title}")
            print(f"Category: {next_task.category}")
            print(f"Effort:   {next_task.effort_hours} hours")
            print(f"Status:   {next_task.status}")
            print(f"\nFiles to modify:")
            for f in next_task.files:
                print(f"  📁 {f}")
            if next_task.description:
                print(f"\nDescription:\n{next_task.description[:300]}...")
        else:
            print("✅ No tasks available or all are blocked!")

    elif command == "resolve":
        if len(sys.argv) < 3:
            print("Usage: resolve <criticality_id> [notes]")
            sys.exit(1)

        crit_id = sys.argv[2]
        notes = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        agent.mark_resolved(crit_id, notes)

    elif command == "commit":
        if len(sys.argv) < 3:
            print("Usage: commit <criticality_id> [additional_notes]")
            sys.exit(1)

        crit_id = sys.argv[2]
        additional_notes = " ".join(sys.argv[3:]) if len(sys.argv) > 3 else ""
        agent.commit_fix(crit_id, additional_notes)

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
