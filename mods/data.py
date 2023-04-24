from shiny import ui, App, module, reactive, render
import asyncio
import seaborn as sns
import pandas as pd

SLEEP_TIME = 5

@module.ui
def data_ui():
	return  ui.layout_sidebar(
		ui.panel_sidebar(
			ui.input_action_button("get_data", "Get Data!"),
			ui.output_ui("choose_movie"),
		),
		ui.panel_main(
			ui.output_text_verbatim("info"),
			ui.output_table("table")
		)
	)


@module.server
def data_server(input, output, session):

	df = pd.read_csv('data/movies.csv', sep=',')

	# reactive values
	rv_df = reactive.Value()
	rv_message = reactive.Value("")

	@output
	@render.ui
	@reactive.event(input.get_data)
	def choose_movie():
		return ui.TagList(
			ui.input_select("movie", label="Movie", choices=list(df['Title'].unique())),
			ui.output_text_verbatim("selected_movie")
		)

	@output
	@render.text
	def selected_movie():
		return f"Selected: {input.movie()}"


	# Slow function
	async def get_data():
		rv_df.set(pd.read_csv('data/movies.csv', sep=',', nrows=1000))
		for i in range(500_000):
			print(i)
		return rv_df.get()


	@output
	@render.text
	@reactive.Calc
	def message():
		return str(rv_message())


	@output
	@render.table
	@reactive.event(input.get_data) # Take a dependency on the button
	async def table():

		task = asyncio.create_task(get_data())
		ui.notification_show("Getting data...", type="message", duration=None, close_button=False)

		# messge user
		df = await task
		ui.notification_show("Data is gereed!", type="message", duration=None, close_button=False)
		
		numeric_cols = ['Rating']
		return (
			df.style.set_table_attributes(
				'class="dataframe shiny-table table w-auto"'
			)
			.hide(axis="index")
			.format(
				{
					# "isba_nr": "{0:0.1f}",
					# "bill_depth_mm": "{0:0.1f}",
					# "flipper_length_mm": "{0:0.0f}",
					# "body_mass_g": "{0:0.0f}",
				}
			)
			.set_table_styles([
					dict(selector="th", props=[("text-align", "right")]),
					dict(
						selector="tr>td",
						props=[
							("padding-top", "0.1rem"),
							("padding-bottom", "0.1rem"),
						],
					),
			]) # type: ignore
			.highlight_min(color="silver", subset=numeric_cols)
			.highlight_max(color="yellow", subset=numeric_cols)
		)
