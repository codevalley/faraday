#!/usr/bin/env python3
"""Demo script showing smart interactive mode detection."""

import subprocess
import sys
import os
from pathlib import Path


def run_command(cmd, env_vars=None, input_data=None):
    """Run a command and return the result."""
    env = os.environ.copy()
    if env_vars:
        env.update(env_vars)
    
    result = subprocess.run(
        cmd,
        cwd=Path(__file__).parent,
        capture_output=True,
        text=True,
        env=env,
        input=input_data
    )
    return result


def demo_smart_interactive():
    """Demonstrate smart interactive mode detection."""
    print("🧠 Smart Interactive Mode Detection Demo\n")
    
    print("1. 🎯 Normal terminal usage (would start interactive):")
    print("   Command: faraday")
    print("   Result: Auto-starts interactive mode because:")
    print("   ✓ Running in terminal")
    print("   ✓ No command specified")
    print("   ✓ Not in CI environment")
    print("   ✓ Not piped/redirected")
    print()
    
    print("2. 🚫 Disabled with flag:")
    result = run_command(["poetry", "run", "faraday", "--no-interactive"])
    print("   Command: faraday --no-interactive")
    print("   Result: Shows help instead of interactive")
    print(f"   Output: {result.stdout.split(chr(10))[0]}")
    print()
    
    print("3. 🔧 Disabled with environment variable:")
    result = run_command(
        ["poetry", "run", "faraday"], 
        env_vars={"FARADAY_NO_INTERACTIVE": "1"}
    )
    print("   Command: FARADAY_NO_INTERACTIVE=1 faraday")
    print("   Result: Shows help instead of interactive")
    print(f"   Output: {result.stdout.split(chr(10))[0]}")
    print()
    
    print("4. 📝 JSON output (auto-disables interactive):")
    result = run_command(["poetry", "run", "faraday", "--json", "version"])
    print("   Command: faraday --json version")
    print("   Result: JSON output, no interactive mode")
    print(f"   Output: {result.stdout.strip()}")
    print()
    
    print("5. 🔗 Piped input (auto-disables interactive):")
    result = run_command(
        ["poetry", "run", "faraday", "thoughts", "--help"],
        input_data="some input"
    )
    print("   Command: echo 'input' | faraday thoughts --help")
    print("   Result: Normal CLI behavior, no interactive")
    print(f"   Output: {result.stdout.split(chr(10))[0]}")
    print()
    
    print("6. ✅ Specific commands still work normally:")
    result = run_command(["poetry", "run", "faraday", "thoughts", "list", "--help"])
    print("   Command: faraday thoughts list --help")
    print("   Result: Shows command help, no interactive")
    print(f"   Output: {result.stdout.split(chr(10))[0]}")
    print()
    
    print("7. 🎮 Explicit interactive still works:")
    print("   Command: faraday interactive")
    print("   Result: Always starts interactive mode")
    print("   (This command always works regardless of detection)")
    print()
    
    print("📋 Summary of Smart Detection Rules:")
    print("   Interactive mode auto-starts when:")
    print("   ✓ No specific command given (just 'faraday')")
    print("   ✓ Running in a terminal (not piped/redirected)")
    print("   ✓ Not requesting JSON output")
    print("   ✓ Not in CI environment")
    print("   ✓ Not disabled via flag or environment variable")
    print("   ✓ Not disabled in user configuration")
    print()
    
    print("   Otherwise, shows help or executes the specific command.")
    print()
    
    print("🎯 This gives users the best of both worlds:")
    print("   • Friendly interactive experience by default")
    print("   • Full scriptability when needed")
    print("   • No breaking changes to existing workflows")


def demo_configuration():
    """Show how users can configure the behavior."""
    print("\n⚙️  Configuration Options:\n")
    
    print("Users can control this behavior in several ways:")
    print()
    
    print("1. 🏃 One-time disable:")
    print("   faraday --no-interactive")
    print()
    
    print("2. 🌍 Environment variable:")
    print("   export FARADAY_NO_INTERACTIVE=1")
    print("   faraday  # Will show help instead")
    print()
    
    print("3. ⚙️  Configuration file:")
    print("   faraday config set ui.auto_interactive false")
    print("   # Now 'faraday' will always show help")
    print()
    
    print("4. 🔄 Re-enable:")
    print("   faraday config set ui.auto_interactive true")
    print("   # Back to smart interactive mode")
    print()
    
    print("5. 🎯 Force interactive:")
    print("   faraday interactive  # Always works")


if __name__ == "__main__":
    demo_smart_interactive()
    demo_configuration()
    
    print("\n✨ Smart interactive mode provides the perfect balance!")
    print("   New users get a friendly experience, power users keep full control.")