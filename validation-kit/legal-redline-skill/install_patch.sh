#!/bin/bash
# install_patch.sh
# Adds the legal-redline skill to an existing ai-legal-claude install.
# Run AFTER the main install.sh from zubair-trabzada/ai-legal-claude.

set -e

CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
SKILLS_DIR="$CLAUDE_DIR/skills"
SCRIPTS_DIR="$CLAUDE_DIR/scripts"

SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Installing legal-redline skill..."

if [ ! -d "$CLAUDE_DIR" ]; then
    echo "Error: $CLAUDE_DIR does not exist. Run ai-legal-claude/install.sh first."
    exit 1
fi

mkdir -p "$SKILLS_DIR/legal-redline"
mkdir -p "$SCRIPTS_DIR"

cp "$SOURCE_DIR/skills/legal-redline/SKILL.md" "$SKILLS_DIR/legal-redline/SKILL.md"
cp "$SOURCE_DIR/scripts/generate_redline_docx.py" "$SCRIPTS_DIR/generate_redline_docx.py"
chmod +x "$SCRIPTS_DIR/generate_redline_docx.py"

echo "Checking python-docx..."
if ! python3 -c "import docx" 2>/dev/null; then
    echo "Installing python-docx..."
    pip3 install python-docx
fi

echo ""
echo "✓ legal-redline installed."
echo ""
echo "Usage in Claude Code:"
echo "  /legal redline <contract-file>"
echo ""
echo "Example:"
echo "  /legal redline test-contracts/freelancer_contract.md"
