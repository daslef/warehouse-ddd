def main() -> None:
    """Warehouse Ddd."""
    from warehouse_ddd_petproject.flask_app import create_app

    app = create_app()
    app.run(debug=True)


if __name__ == "__main__":
    main()  # pragma: no cover
