from website import create_app

app = create_app()

if __name__ == '__main__':
    """
    Startowa funkcaj aplikacji Ecommerce.

    Uruchamia aplikację Flask w trybie debug na lokalnym serwerze na porcie 3001.
    """
    app.run(debug=True, host='localhost', port=3001)
