#!/usr/bin/env python3
"""
Simple test to show the updated Project Directory step with remote option.
"""

print("\n" + "=" * 80)
print("DEMO: Updated Step 2 - Project Directory")
print("=" * 80)
print("\nThis is how Step 2 now appears to users:\n")

# Simulate the step
print("Step 2: Project Directory 🔧")
print("─" * 80)
print("Choose project location:")
print("  1. Local directory (default)")
print("  2. Remote directory (Raspberry Pi via Cloudflare tunnel)")
print("Select location [1/2] (1): ", end="")

choice = input()
if not choice:
    choice = "1"

print()

if choice == "1":
    print("Default local location: ~/Projects/my_project")
    print("Press Enter to accept the default or type a new path:")
    print("> ", end="")
    path = input()
    if not path:
        path = "~/Projects/my_project"
    print(f"\n✅ Local directory selected: {path}")

elif choice == "2":
    print("Remote Directory Setup")
    print("Remote host: manjarodell-to-pi (via Cloudflare tunnel)")
    print("Default remote location: /home/mail2mick/Projects/my_project")
    print("Use default remote path? [Y/n]: ", end="")

    use_default = input()
    if use_default.lower() != "n":
        remote_path = "/home/mail2mick/Projects/my_project"
    else:
        print("Enter custom remote path (e.g., /home/mail2mick/custom/path): ", end="")
        remote_path = input()

    print("\n✅ Remote directory configured:")
    print(f"  Path: {remote_path}")
    print("  Access: SSH via Cloudflare tunnel")
    print("\nNote: Ensure your Cloudflare tunnel is active for remote operations.")
    print(
        f"\nInternal representation: sftp://mail2mick@manjarodell-to-pi:8850{remote_path}"
    )

print("\n" + "=" * 80)
print(
    "This step now provides a clear choice between local and remote project locations!"
)
print("=" * 80)
