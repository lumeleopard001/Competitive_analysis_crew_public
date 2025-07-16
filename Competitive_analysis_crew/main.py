#!/usr/bin/env python
"""
Main entry point for the Competitive Analysis Crew.

This module provides CLI commands for running, training, replaying, and testing
the competitive analysis crew. It serves as the primary interface for users
to interact with the crew functionality.
"""

import sys
import warnings
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel

from Competitive_analysis_crew.crew import CompetitiveAnalysisCrew

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")
warnings.filterwarnings("ignore", category=UserWarning, module="pydantic")

# Initialize Rich console for better CLI output
console = Console()
app = typer.Typer(help="Competitive Analysis Crew - Enterprise-grade market intelligence automation")


@app.command()
def run():
    """
    Run the competitive analysis crew.
    
    This function initializes and executes the complete competitive analysis workflow,
    including user onboarding, research, report generation, and optional translation.
    """
    try:
        console.print(Panel.fit(
            "[bold blue]Competitive Analysis Crew[/bold blue]\n"
            "Enterprise-grade market intelligence automation",
            border_style="blue"
        ))
        
        # Initialize and run the crew
        crew_instance = CompetitiveAnalysisCrew()
        result = crew_instance.crew().kickoff()
        
        console.print("\n[bold green]✓ Analysis completed successfully![/bold green]")
        return result
        
    except Exception as e:
        console.print(f"[bold red]✗ Error occurred while running the crew:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def train(
    n_iterations: int = typer.Argument(..., help="Number of training iterations"),
    filename: str = typer.Argument(..., help="Filename to save training results")
):
    """
    Train the crew for a given number of iterations.
    
    This command runs the crew multiple times to improve its performance
    through iterative learning and optimization.
    """
    try:
        console.print(f"[bold yellow]Training crew for {n_iterations} iterations...[/bold yellow]")
        
        crew_instance = CompetitiveAnalysisCrew()
        crew_instance.crew().train(n_iterations=n_iterations, filename=filename)
        
        console.print(f"[bold green]✓ Training completed! Results saved to {filename}[/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error occurred while training the crew:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def replay(task_id: str = typer.Argument(..., help="Task ID to replay from")):
    """
    Replay the crew execution from a specific task.
    
    This command allows you to restart the crew execution from a particular
    task, useful for debugging or continuing from a specific point.
    """
    try:
        console.print(f"[bold yellow]Replaying crew from task: {task_id}[/bold yellow]")
        
        crew_instance = CompetitiveAnalysisCrew()
        crew_instance.crew().replay(task_id=task_id)
        
        console.print("[bold green]✓ Replay completed successfully![/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error occurred while replaying the crew:[/bold red] {e}")
        raise typer.Exit(1)


@app.command()
def test(
    n_iterations: int = typer.Argument(..., help="Number of test iterations"),
    model_name: str = typer.Argument(..., help="OpenAI model name to test with")
):
    """
    Test the crew execution and return the results.
    
    This command runs comprehensive tests on the crew to validate
    its functionality and performance with different configurations.
    """
    try:
        console.print(f"[bold yellow]Testing crew with {n_iterations} iterations using {model_name}...[/bold yellow]")
        
        crew_instance = CompetitiveAnalysisCrew()
        crew_instance.crew().test(n_iterations=n_iterations, openai_model_name=model_name)
        
        console.print("[bold green]✓ Testing completed successfully![/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error occurred while testing the crew:[/bold red] {e}")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
