import os
from pathlib import Path
import textwrap

from openai import OpenAI

def gather_context() -> str:
    """
    Collect a small, targeted slice of repo context for the model:
    - stegverse_connectivity.md
    - workflows under .github/workflows/
    - README files
    """
    root = Path(".").resolve()
    parts = []

    # Connectivity spec
    conn = root / "stegverse_connectivity.md"
    if conn.exists():
        try:
            parts.append("# File: stegverse_connectivity.md\n" + conn.read_text(errors="ignore")[:4000])
        except Exception:
            pass

    # Workflows
    wf_root = root / ".github" / "workflows"
    if wf_root.exists():
        for wf in sorted(wf_root.glob("*.yml")):
            try:
                txt = wf.read_text(errors="ignore")
                parts.append(f"# File: .github/workflows/{wf.name}\n{txt[:3000]}")
            except Exception:
                pass

    # README files
    for readme in [root / "README.md", root / "README-HCB.md"]:
        if readme.exists():
            try:
                parts.append(f"# File: {readme.name}\n" + readme.read_text(errors="ignore")[:3000])
            except Exception:
                pass

    return "\n\n---\n\n".join(parts)


def main():
    instructions = os.environ.get("INSTRUCTIONS", "").strip()
    if not instructions:
        instructions = "Audit and improve this repo's connectivity based on stegverse_connectivity.md."

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("Missing OPENAI_API_KEY in environment.")

    client = OpenAI(api_key=api_key)

    repo_context = gather_context()

    user_prompt = textwrap.dedent(f"""
    You are StegVerse-AI-001 operating INSIDE the Hybrid-Collab-Bridge repository.

    Your specific mission:
    - Focus ONLY on THIS repo.
    - Follow the connectivity spec in `stegverse_connectivity.md` if present.
    - Improve workflows, naming, and connectivity wiring for StegCore, StegTV, and StegVerse-SCW.
    - Prefer small, safe, incremental edits over large refactors.
    - Never introduce secrets or hard-coded tokens.

    Task from the human:
    {instructions}

    Current repo snapshot (partial, truncated for length):

    {repo_context}
    """)

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a careful, security-focused StegVerse maintainer with commit rights to this repo."},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=900,
    )

    answer = response.choices[0].message.content or "(model returned no content)"
    print("\n===== StegVerse-AI-001 plan / suggestions =====\n")
    print(answer)
    print("\n===== END AI OUTPUT =====\n")

    # NOTE:
    # For now we ONLY print the plan. We do NOT auto-edit files here.
    # Next iteration we can teach this script to parse and apply small patches.
    # The commit step in the workflow will only run if you (or a later helper script)
    # actually modify files before the job completes.

if __name__ == "__main__":
    main()
