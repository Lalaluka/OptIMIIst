import os
import click
from rich.console import Console
from rich.progress import Progress
import pm4py

from .core import optimiist

console = Console()

@click.group()
def cli():
    """OptIMIIst - Process Mining CLI Tool."""
    pass

@cli.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file', type=click.Path())
@click.option('--filter/--no-filter', default=True, help='Apply filtering in the OptIMIIst algorithm')
def process(input_file, output_file, filter):
    """Process an event log and generate a Petri net.
    
    INPUT_FILE: Path to XES event log file
    OUTPUT_FILE: Path to save the resulting PNML file
    """
    console.print(f"[bold]Processing event log:[/bold] {input_file}")
    console.print(f"[bold]Filter enabled:[/bold] {filter}")
    
    with Progress() as progress:
        task = progress.add_task("[green]Loading event log...", total=3)
        
        # Load the event log
        if input_file.lower().endswith('.xes') or input_file.lower().endswith('.xes.gz'):
            log = pm4py.read_xes(input_file)
        else:
            console.print("[bold red]Error:[/bold red] Unsupported file format. Please provide an XES or XES.GZ file.")
            return
        
        progress.update(task, advance=1, description="[green]Discovering Petri net...")
        
        # Apply the OptIMIIst algorithm
        petri_net, initial_marking, final_marking = optimiist(log, filter)
        
        progress.update(task, advance=1, description="[green]Saving Petri net...")
        
        # Save the Petri net as PNML
        pm4py.write_pnml(petri_net, initial_marking, final_marking, output_file)
        
        progress.update(task, advance=1, description="[green]Process completed!")
    
    console.print(f"[bold green]Success![/bold green] Petri net saved to: {output_file}")

def main():
    cli()

if __name__ == '__main__':
    main()
