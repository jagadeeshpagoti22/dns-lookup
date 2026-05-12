"""
ⒸAngelaMos | 2026
output.py

Rich terminal output formatting for DNS results

Handles all visual presentation for query, reverse, trace, batch, and
WHOIS results. Uses Rich tables, panels, and tree structures with color
coding per record type. Also provides JSON serialization used when the
--json flag is passed from the CLI.

Key exports:
  console - Shared Rich Console instance imported by cli.py
  print_results_table - Renders DNS records as a color-coded rounded table
  print_reverse_result - Renders PTR lookup output with hostname table
  print_trace_result - Renders the DNS resolution path as a Rich tree
  print_batch_results - Renders a summary table for multiple domain results
  results_to_json - Serializes one or more DNSResult objects to a JSON string
  trace_to_json - Serializes a TraceResult to a JSON string

Connects to:
  resolver.py - imports DNSResult, TraceResult, RecordType for type annotations
  cli.py - all print_* functions and JSON serializers called in command handlers
"""

from __future__ import annotations

import json
from typing import Any

from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.tree import Tree

from dnslookup.resolver import DNSResult, RecordType, TraceResult

console = Console()

RECORD_COLORS: dict[RecordType, str] = {
    RecordType.A: "green",
    RecordType.AAAA: "cyan",
    RecordType.MX: "magenta",
    RecordType.NS: "bright_blue",
    RecordType.TXT: "yellow",
    RecordType.CNAME: "red",
    RecordType.SOA: "white",
    RecordType.PTR: "bright_cyan",
}

BORDER_STYLE = "grey50"
HEADER_STYLE = "bold white"
TITLE_STYLE = "bold white"
ACCENT_STYLE = "cyan"
DIM_STYLE = "dim"


def get_record_color(record_type: RecordType) -> str:
    """Get the color for a record type."""
    return RECORD_COLORS.get(record_type, "white")


def format_ttl(ttl: int) -> str:
    """Format TTL in human-readable form."""
    if ttl >= 86400:
        return f"{ttl // 86400}d"
    if ttl >= 3600:
        return f"{ttl // 3600}h"
    if ttl >= 60:
        return f"{ttl // 60}m"
    return f"{ttl}s"


def _section_header(icon: str, title: str, subject: str, subtitle: str | None = None) -> None:
    """Print a consistent, professional section header."""
    header = Text()
    header.append(f"{icon} ", style="bold")
    header.append(title, style=TITLE_STYLE)
    header.append(" • ", style="dim")
    header.append(subject, style=f"bold {ACCENT_STYLE}")

    body = Text()
    body.append(f"{icon} ", style="bold")
    body.append(title, style=TITLE_STYLE)
    body.append(" • ", style="dim")
    body.append(subject, style=f"bold {ACCENT_STYLE}")

    if subtitle:
        body.append("\n")
        body.append(subtitle, style="dim")

    console.print()
    console.print(
        Panel(
            body,
            border_style=BORDER_STYLE,
            box=box.ROUNDED,
            padding=(0, 1),
            expand=False,
        )
    )


def print_header(domain: str, icon: str = ":globe_showing_americas:") -> None:
    """Print a styled header for DNS lookup."""
    _section_header(icon, "DNS Lookup", domain, "Professional DNS results")


def print_results_table(result: DNSResult) -> None:
    """Display DNS results in a clean table."""
    if not result.records:
        console.print(
            Panel(
                f"[yellow]No records found for [bold]{result.domain}[/bold][/yellow]",
                title="[bold yellow]No Results[/bold yellow]",
                border_style="yellow",
                expand=False,
                box=box.ROUNDED,
                padding=(0, 1),
            )
        )
        return

    table = Table(
        box=box.SIMPLE_HEAVY,
        border_style=BORDER_STYLE,
        header_style=HEADER_STYLE,
        show_lines=False,
        expand=False,
        pad_edge=False,
        row_styles=["", "dim"],
    )

    table.add_column("Type", width=8, no_wrap=True)
    table.add_column("Record", overflow="fold")
    table.add_column("TTL", justify="right", style=DIM_STYLE, width=8, no_wrap=True)

    for record in result.records:
        color = get_record_color(record.record_type)
        value = record.value

        if record.priority is not None:
            value = f"{value} [dim](priority {record.priority})[/dim]"

        table.add_row(
            f"[{color}]{record.record_type}[/{color}]",
            value,
            format_ttl(record.ttl),
        )

    console.print(
        Panel(
            table,
            title="[bold]DNS Records[/bold]",
            border_style=BORDER_STYLE,
            box=box.ROUNDED,
            expand=False,
            padding=(0, 1),
        )
    )


def print_summary(result: DNSResult) -> None:
    """Print a compact professional summary after results."""
    stats = Table.grid(expand=False, padding=(0, 2))
    stats.add_column(justify="left")
    stats.add_column(justify="left")

    record_count = len(result.records)
    time_str = f"{result.query_time_ms:.0f}ms"

    status = (
        f"[green]✓[/green] [bold]{record_count}[/bold] record(s) found"
        if record_count > 0
        else "[yellow]⚠[/yellow] No records found"
    )

    stats.add_row("Status", status)
    stats.add_row("Query time", f"[cyan]{time_str}[/cyan]")

    if result.nameserver:
        stats.add_row("Server", f"[bold]{result.nameserver}[/bold]")

    if result.domain:
        stats.add_row("Domain", f"[bold]{result.domain}[/bold]")

    console.print(
        Panel(
            stats,
            border_style=BORDER_STYLE,
            title="[bold]Summary[/bold]",
            box=box.ROUNDED,
            expand=False,
            padding=(0, 1),
        )
    )
    console.print()


def print_errors(result: DNSResult) -> None:
    """Print any errors that occurred."""
    if result.errors:
        error_table = Table.grid(expand=False, padding=(0, 1))
        error_table.add_column(justify="left")
        for error in result.errors:
            error_table.add_row(f"[red]✗[/red] {error}")
        console.print(
            Panel(
                error_table,
                border_style="red",
                title="[bold red]Errors[/bold red]",
                box=box.ROUNDED,
                expand=False,
                padding=(0, 1),
            )
        )


def print_reverse_result(result: DNSResult) -> None:
    """Display reverse DNS lookup results."""
    _section_header(":mag:", "Reverse Lookup", result.domain, "IP to hostname mapping")

    if result.records:
        table = Table(
            title="[bold]PTR Records[/bold]",
            box=box.SIMPLE_HEAVY,
            border_style=BORDER_STYLE,
            row_styles=["", "dim"],
            show_header=True,
            header_style=HEADER_STYLE,
            expand=False,
            pad_edge=False,
        )
        table.add_column("IP Address", style="cyan", no_wrap=True)
        table.add_column("Hostname", style="green", overflow="fold")
        table.add_column("TTL", justify="right", style=DIM_STYLE, width=8, no_wrap=True)

        for record in result.records:
            table.add_row(
                result.domain,
                record.value,
                format_ttl(record.ttl),
            )

        console.print(
            Panel(
                table,
                border_style=BORDER_STYLE,
                box=box.ROUNDED,
                expand=False,
                padding=(0, 1),
            )
        )
        print_summary(result)
    else:
        print_errors(result)
        console.print(
            Panel(
                f"[yellow]No PTR record found for [bold]{result.domain}[/bold][/yellow]",
                border_style="yellow",
                title="[bold yellow]No Result[/bold yellow]",
                box=box.ROUNDED,
                expand=False,
                padding=(0, 1),
            )
        )
        console.print()


def print_trace_result(result: TraceResult) -> None:
    """Display DNS trace as a tree visualization."""
    _section_header(":compass:", "DNS Trace", result.domain, "Resolution path from root to authoritative servers")

    if result.error:
        console.print(
            Panel(
                f"[red]✗[/red] {result.error}",
                border_style="red",
                title="[bold red]Trace Failed[/bold red]",
                box=box.ROUNDED,
                expand=False,
                padding=(0, 1),
            )
        )
        console.print()
        return

    tree = Tree("[bold]DNS Resolution Path[/bold]", guide_style="grey50")

    zone_nodes: dict[str, Any] = {}

    for hop in result.hops:
        if hop.zone not in zone_nodes:
            if hop.zone == ".":
                zone_display = "[bold yellow]Root zone[/bold yellow]"
            elif hop.zone.endswith("."):
                zone_display = f"[bold yellow]{hop.zone}[/bold yellow]"
            else:
                zone_display = f"[bold yellow]{hop.zone}.[/bold yellow]"

            zone_node = tree.add(zone_display)
            zone_nodes[hop.zone] = zone_node
        else:
            zone_node = zone_nodes[hop.zone]

        server_style = "green" if hop.is_authoritative else "cyan"
        server_branch = zone_node.add(
            f"[{server_style}]→ {hop.server}[/{server_style}] [dim]({hop.server_ip})[/dim]"
        )
        server_branch.add(f"[dim]{hop.response}[/dim]")

    console.print(
        Panel(
            tree,
            border_style=BORDER_STYLE,
            box=box.ROUNDED,
            expand=False,
            padding=(0, 1),
        )
    )

    if result.final_answer:
        console.print(
            Panel(
                f"[green]✓[/green] Resolution complete: [bold green]{result.final_answer}[/bold green]",
                border_style="green",
                box=box.ROUNDED,
                expand=False,
                padding=(0, 1),
            )
        )

    hop_count = len(result.hops)
    console.print(f"[dim]Total hops: {hop_count}[/dim]")
    console.print()


def print_batch_progress_header(total: int) -> None:
    """Print header for batch operations."""
    _section_header(":package:", "Batch Lookup", f"{total} domains", "Bulk DNS results")


def print_batch_results(results: list[DNSResult]) -> None:
    """Display batch lookup results in a summary table."""
    table = Table(
        title="[bold]Batch Results[/bold]",
        box=box.SIMPLE_HEAVY,
        border_style=BORDER_STYLE,
        row_styles=["", "dim"],
        header_style=HEADER_STYLE,
        expand=False,
        pad_edge=False,
    )

    table.add_column("Domain", style="cyan", min_width=25, overflow="fold")
    table.add_column("A", justify="center", width=15)
    table.add_column("MX", justify="center", width=5)
    table.add_column("NS", justify="center", width=5)
    table.add_column("Time", justify="right", style=DIM_STYLE, width=8, no_wrap=True)

    for result in results:
        a_records = [r for r in result.records if r.record_type == RecordType.A]
        mx_count = len([r for r in result.records if r.record_type == RecordType.MX])
        ns_count = len([r for r in result.records if r.record_type == RecordType.NS])

        a_value = a_records[0].value if a_records else "[dim]-[/dim]"
        mx_value = str(mx_count) if mx_count else "[dim]-[/dim]"
        ns_value = str(ns_count) if ns_count else "[dim]-[/dim]"

        table.add_row(
            result.domain,
            a_value,
            mx_value,
            ns_value,
            f"{result.query_time_ms:.0f}ms",
        )

    console.print(
        Panel(
            table,
            border_style=BORDER_STYLE,
            box=box.ROUNDED,
            expand=False,
            padding=(0, 1),
        )
    )

    total_records = sum(len(r.records) for r in results)
    total_time = sum(r.query_time_ms for r in results)
    console.print(
        Panel(
            f"[green]✓[/green] [bold]{len(results)}[/bold] domains · [bold]{total_records}[/bold] total records · [cyan]{total_time:.0f}ms[/cyan]",
            border_style=BORDER_STYLE,
            title="[bold]Batch Summary[/bold]",
            box=box.ROUNDED,
            expand=False,
            padding=(0, 1),
        )
    )
    console.print()


def results_to_json(results: list[DNSResult] | DNSResult) -> str:
    """Convert results to JSON string."""
    if isinstance(results, DNSResult):
        results = [results]

    data = []
    for result in results:
        record_data = [
            {
                "type": r.record_type.value,
                "value": r.value,
                "ttl": r.ttl,
                "priority": r.priority,
            }
            for r in result.records
        ]

        data.append(
            {
                "domain": result.domain,
                "records": record_data,
                "errors": result.errors,
                "query_time_ms": round(result.query_time_ms, 2),
                "nameserver": result.nameserver,
            }
        )

    if len(data) == 1:
        return json.dumps(data[0], indent=2)

    return json.dumps(data, indent=2)


def trace_to_json(result: TraceResult) -> str:
    """Convert trace result to JSON string."""
    data = {
        "domain": result.domain,
        "hops": [
            {
                "zone": hop.zone,
                "server": hop.server,
                "server_ip": hop.server_ip,
                "response": hop.response,
                "is_authoritative": hop.is_authoritative,
            }
            for hop in result.hops
        ],
        "final_answer": result.final_answer,
        "error": result.error,
    }

    return json.dumps(data, indent=2)
