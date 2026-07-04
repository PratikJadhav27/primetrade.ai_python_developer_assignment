import typer
from typing import Optional
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Load environment variables from .env file
load_dotenv()

from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price
from bot.orders import place_order
from bot.logging_config import logger

app = typer.Typer(help="Binance Futures Testnet Trading Bot CLI")
console = Console()

@app.command()
def trade(
    symbol: str = typer.Option(..., "--symbol", "-s", help="Trading symbol, e.g., BTCUSDT", callback=validate_symbol),
    side: str = typer.Option(..., "--side", "-S", help="Order side: BUY or SELL", callback=validate_side),
    order_type: str = typer.Option(..., "--type", "-t", help="Order type: MARKET, LIMIT, STOP_MARKET", callback=validate_order_type),
    quantity: float = typer.Option(..., "--quantity", "-q", help="Quantity to trade", callback=validate_quantity),
    price: Optional[float] = typer.Option(None, "--price", "-p", help="Price (required for LIMIT)"),
    stop_price: Optional[float] = typer.Option(None, "--stop-price", "-sp", help="Stop Price (required for STOP_MARKET)")
):
    """
    Place a new order on Binance Futures Testnet.
    """
    # Cross-parameter validation
    try:
        validate_price(price=price, order_type=order_type, stop_price=stop_price)
    except typer.BadParameter as e:
        console.print(f"[bold red]Validation Error:[/bold red] {e}")
        raise typer.Exit(code=1)

    # Summary table before placing order
    summary_table = Table(title="Order Request Summary", show_header=True, header_style="bold magenta")
    summary_table.add_column("Parameter", style="cyan")
    summary_table.add_column("Value", style="green")
    
    summary_table.add_row("Symbol", symbol)
    summary_table.add_row("Side", side)
    summary_table.add_row("Type", order_type)
    summary_table.add_row("Quantity", str(quantity))
    if price:
        summary_table.add_row("Price", str(price))
    if stop_price:
        summary_table.add_row("Stop Price", str(stop_price))
        
    console.print(summary_table)

    with console.status("[bold yellow]Sending order to Binance Testnet...[/bold yellow]"):
        try:
            response = place_order(
                symbol=symbol,
                side=side,
                order_type=order_type,
                quantity=quantity,
                price=price,
                stop_price=stop_price
            )
            
            # Print success response
            console.print("\n[bold green]✅ Order placed successfully![/bold green]")
            
            result_table = Table(title="Order Response Details", show_header=True, header_style="bold blue")
            result_table.add_column("Field", style="cyan")
            result_table.add_column("Value", style="green")
            
            # Extract key details from response
            details_to_show = ["orderId", "status", "symbol", "side", "type", "executedQty", "avgPrice"]
            for field in details_to_show:
                if field in response:
                    result_table.add_row(field, str(response[field]))
                    
            console.print(result_table)
            
        except Exception as e:
            console.print(Panel.fit(f"[bold red]Order Failed:[/bold red]\n{str(e)}", title="Error", border_style="red"))
            raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
