from src import create_app, DevConfig, ProdConfig


# Create a Flask application instance using the development configuration.
app = create_app(DevConfig)

if __name__ == '__main__':
    # Run the application.
    app.run()
