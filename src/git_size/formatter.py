"""Output formatting utilities."""
import json
from rich.table import Table
from rich.console import Console

def format_size(bytes_size):
    """Convert bytes to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} PB"

def format_table(data, title, is_dir=False):
    """Format data as a rich table."""
    table = Table(title=title, show_header=True, header_style="bold magenta")
    
    if is_dir:
        table.add_column("Directory", style="cyan")
        table.add_column("Total Size", justify="right", style="green")
        
        for item in data:
            table.add_row(item['path'], format_size(item['size']))
    else:
        table.add_column("File Path", style="cyan")
        table.add_column("Size", justify="right", style="green")
        table.add_column("SHA", style="yellow")
        
        for item in data:
            sha = item.get('sha', item.get('commit', 'N/A'))
            table.add_row(item['path'], format_size(item['size']), sha)
    
    return table

def format_json(data):
    """Format data as JSON string."""
    formatted_data = []
    for item in data:
        formatted_item = item.copy()
        formatted_item['size_human'] = format_size(item['size'])
        formatted_data.append(formatted_item)
    
    return json.dumps(formatted_data, indent=2)