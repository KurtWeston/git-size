"""CLI interface for git-size."""
import json
import click
from pathlib import Path
from rich.console import Console
from .analyzer import GitAnalyzer
from .formatter import format_table, format_size, format_json

console = Console()

@click.group()
@click.version_option()
def cli():
    """Analyze Git repository size and identify bloat."""
    pass

@cli.command()
@click.option('-n', '--limit', default=20, help='Number of files to show')
@click.option('-t', '--threshold', default=0, help='Minimum size in MB')
@click.option('-e', '--extension', multiple=True, help='Filter by extension')
@click.option('-p', '--path', default='.', help='Repository path')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
def top(limit, threshold, extension, path, json_output):
    """Show largest files in repository history."""
    try:
        analyzer = GitAnalyzer(path)
        files = analyzer.get_largest_files(limit, threshold * 1024 * 1024, extension)
        
        if json_output:
            console.print(format_json(files))
        else:
            console.print(format_table(files, 'Top Largest Files'))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()

@cli.command()
@click.option('-n', '--limit', default=15, help='Number of directories to show')
@click.option('-p', '--path', default='.', help='Repository path')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
def dirs(limit, path, json_output):
    """Show largest directories by total file size."""
    try:
        analyzer = GitAnalyzer(path)
        directories = analyzer.get_largest_directories(limit)
        
        if json_output:
            console.print(format_json(directories))
        else:
            console.print(format_table(directories, 'Largest Directories', is_dir=True))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()

@cli.command()
@click.option('-n', '--limit', default=20, help='Number of files to show')
@click.option('-p', '--path', default='.', help='Repository path')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
def deleted(limit, path, json_output):
    """Show deleted files still in repository history."""
    try:
        analyzer = GitAnalyzer(path)
        files = analyzer.get_deleted_files(limit)
        
        if json_output:
            console.print(format_json(files))
        else:
            console.print(format_table(files, 'Deleted Files in History'))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()

@cli.command()
@click.option('-t', '--threshold', default=100, help='Size threshold in MB')
@click.option('-p', '--path', default='.', help='Repository path')
@click.option('--json', 'json_output', is_flag=True, help='Output as JSON')
def lfs(threshold, path, json_output):
    """Suggest files for Git LFS migration."""
    try:
        analyzer = GitAnalyzer(path)
        candidates = analyzer.get_lfs_candidates(threshold * 1024 * 1024)
        
        if json_output:
            console.print(format_json(candidates))
        else:
            console.print(format_table(candidates, f'Git LFS Candidates (>{threshold}MB)'))
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()

@cli.command()
@click.option('-p', '--path', default='.', help='Repository path')
def stats(path):
    """Show repository statistics."""
    try:
        analyzer = GitAnalyzer(path)
        stats = analyzer.get_repo_stats()
        
        console.print("\n[bold]Repository Statistics[/bold]\n")
        console.print(f"Total objects: {stats['object_count']:,}")
        console.print(f"Pack size: {format_size(stats['pack_size'])}")
        console.print(f"Working directory: {format_size(stats['working_size'])}")
        console.print(f"Total commits: {stats['commit_count']:,}")
        console.print(f"Branches: {stats['branch_count']}\n")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise click.Abort()

if __name__ == '__main__':
    cli()