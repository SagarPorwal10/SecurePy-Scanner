import sys
import time
import argparse
from rich.progress import Progress, SpinnerColumn, TextColumn
from securepy.core.engine import ScannerEngine
from securepy.core.rich_reporter import RichReporter # Import our new UI

# Import Rules
from securepy.rules.secrets import HardcodedSecretCheck
from securepy.rules.sqli import SQLInjectionCheck
from securepy.rules.dangerous_funcs import DangerousFunctionCheck
from securepy.rules.misconfig import SecurityMisconfigCheck

def main():
    parser = argparse.ArgumentParser(description="SecurePy - Enterprise SAST Scanner")
    parser.add_argument("filename", help="The python file to scan")
    args = parser.parse_args()

    # 1. Initialize Rules
    active_rules = [
        HardcodedSecretCheck(),
        SQLInjectionCheck(),
        DangerousFunctionCheck(),
        SecurityMisconfigCheck()  # <-- Added this!
    ]
    engine = ScannerEngine(active_rules)
    
    # 2. The "Hacker" Loading Animation
    # We use 'rich.progress' to show a fake loading bar while we scan
    issues = []
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True # Disappear when done
    ) as progress:
        task = progress.add_task("[green]Initializing Core Engine...", total=100)
        
        time.sleep(0.5) # Fake delay for dramatic effect
        progress.update(task, advance=30, description=f"[cyan]Parsing AST for {args.filename}...")
        
        # Run the actual scan
        try:
            issues = engine.scan_file(args.filename)
        except Exception as e:
            print(f"[ERROR] Scan failed: {e}")
            sys.exit(1)
            
        time.sleep(0.5)
        progress.update(task, advance=40, description="[red]Analyzing Security Patterns...")
        
        time.sleep(0.5)
        progress.update(task, advance=30, description="[green]Finalizing Report...")

    # 3. Show the Rich Dashboard
    RichReporter.print_dashboard(issues, args.filename)
    
    # Exit code
    if issues:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()