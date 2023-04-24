from shiny import ui, App, module


@module.ui
def home_ui():
	return  ui.page_fluid(
        ui.markdown(
		"""
        # Welcome!

        This is **markdown** and here is some `code`:

        ```python
        print('Welcome to shiny for Python!')
        ```
        """
              
		)
	)

@module.server
def home_server(input, output, session):
    ...