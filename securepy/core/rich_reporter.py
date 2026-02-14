from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.tree import Tree
from rich import box

class RichReporter:
    @staticmethod
    def print_dashboard(issues, filename):
        console = Console()
        
        console.print()
        console.print(Panel(
            f"[bold blue]SecurePy Scanner[/bold blue]\nTarget: [u]{filename}[/u]", 
            border_style="blue",
            expand=False
        ))
        
        if not issues:
             console.print("[bold green]✅ No vulnerabilities found![/bold green]")
             return

        # Summary Stats
        high = sum(1 for i in issues if i['severity'] in ['HIGH', 'CRITICAL'])
        med = sum(1 for i in issues if i['severity'] == 'MEDIUM')
        low = sum(1 for i in issues if i['severity'] == 'LOW')

        # Create a Tree structure
        root = Tree(f"🛡️ [bold]Scan Results[/bold] (Total: {len(issues)})")
        
        if high:
            high_branch = root.add(f"[bold red]🚨 Critical / High ({high})[/bold red]")
            for i in issues:
                if i['severity'] in ['HIGH', 'CRITICAL']:
                    high_branch.add(f"[red]{i['id']}[/red]: {i['message']}\n   [dim]Line {i['line']} • Fix: {i['remediation']}[/dim]")

        if med:
            med_branch = root.add(f"[bold yellow]⚠️ Medium ({med})[/bold yellow]")
            for i in issues:
                if i['severity'] == 'MEDIUM':
                    med_branch.add(f"[yellow]{i['id']}[/yellow]: {i['message']}\n   [dim]Line {i['line']} • Fix: {i['remediation']}[/dim]")

        if low:
            low_branch = root.add(f"[bold blue]ℹ️ Low ({low})[/bold blue]")
            for i in issues:
                if i['severity'] == 'LOW':
                    low_branch.add(f"[blue]{i['id']}[/blue]: {i['message']}\n   [dim]Line {i['line']} • Fix: {i['remediation']}[/dim]")

        console.print(root)
        console.print()