from shiny import App, ui, render
from mods.home import home_ui, home_server
from mods.data import data_ui, data_server
from mods.space.space import space_ui, space_server
from pathlib import Path

ui = ui.page_fluid(
	ui.br(),
	ui.navset_pill(
	# elements ----
	ui.nav("Home", home_ui('home')),
	ui.nav("Data", data_ui('data')),
	ui.nav('space', space_ui('space'))
	)
)

def server(ui, server, session):
	home_server('home')
	data_server('data')
	space_server("space")
    

www_dir = Path(__file__).parent / "www"

app = App(ui, server, static_assets=www_dir)
app.run()