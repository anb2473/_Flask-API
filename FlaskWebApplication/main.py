# Start Website

from Website import create_app

app = create_app()

if __name__ == '__main__':
    # Turn debug off for a real application
    app.run(debug=True)
