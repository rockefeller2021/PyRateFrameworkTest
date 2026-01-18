import argparse
import os
import sys
from .core import PyRateRunner
from .logger import log_success, log_info
from .config_loader import ConfigLoader


def init_project():
    """Initialize a new PyRate project with folder structure and examples"""
    import shutil
    import pkg_resources

    folders = ["tests/features", "tests/data", "reports", "evidence"]
    for f in folders:
        os.makedirs(f, exist_ok=True)

    # Create .env file
    with open(".env", "w") as f:
        f.write("BASE_URL=https://jsonplaceholder.typicode.com\n")

    # Create basic demo feature
    with open("tests/features/demo.feature", "w") as f:
        f.write("# @smoke\nGiven url '#(BASE_URL)'\nAnd path 'users/1'\nWhen method get\nThen status 200\n")

    # Copy examples files from package
    try:
        examples_dir = pkg_resources.resource_filename('pyrate', '../examples')
        example_files = [
            'ui_interactions_complete.feature',
            'form_complete.feature',
            'xpath_selectors.feature',
            'descriptive_syntax.feature',
            'SELECTOR_GUIDE.md'
        ]

        for example_file in example_files:
            src = os.path.join(examples_dir, example_file)
            if os.path.exists(src):
                dst = os.path.join("tests/features", example_file)
                shutil.copy(src, dst)
                log_info(f"  ✓ Copiado: {example_file}")
    except Exception as e:
        log_info(f"  ⚠️  No se pudieron copiar ejemplos: {e}")

    # Generate example config file
    ConfigLoader.save_example_config()

    log_success("Proyecto PyRate inicializado 🚀")
    log_info("\n📁 Estructura creada:")
    log_info("  ├── tests/features/  (tus archivos .feature)")
    log_info("  ├── tests/data/      (archivos CSV/JSON)")
    log_info("  ├── reports/         (reportes HTML)")
    log_info("  ├── evidence/        (evidencia de ejecución)")
    log_info("  └── .env             (variables de entorno)")
    log_info("\n📚 Ejemplos incluidos:")
    log_info("  • ui_interactions_complete.feature - Sprint 3 UI commands")
    log_info("  • form_complete.feature - Real-world form handling")
    log_info("  • xpath_selectors.feature - XPath examples")
    log_info("  • descriptive_syntax.feature - Descriptive comments")
    log_info("\n🚀 Siguiente paso:")
    log_info("  pyrate run tests/features/demo.feature")


def main():
    parser = argparse.ArgumentParser(
        description="PyRate Framework CLI - Automation Testing for API and UI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    # Version argument
    parser.add_argument(
        '-v', '--version',
        action='version',
        version='PyRate Framework 1.1.0'
    )

    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("init", help="Crear estructura de proyecto")

    run_parser = subparsers.add_parser("run", help="Ejecutar pruebas")
    run_parser.add_argument("file", help="Archivo .feature o carpeta a ejecutar")
    run_parser.add_argument("-t", "--tags", help="Filtrar por tag (ej: @smoke)", default=None)
    run_parser.add_argument(
        "-c", "--config",
        help="Archivo de configuración YAML personalizado",
        default=None
    )

    args = parser.parse_args()

    # Show help if no command is provided
    if args.command is None:
        parser.print_help()
        sys.exit(0)

    if args.command == "init":
        init_project()
    elif args.command == "run":
        # Load configurations (custom file or defaults)
        try:
            config = ConfigLoader.load(args.config)
            log_info(f"⚙️  Configuración cargada correctamente")
        except Exception as e:
            log_info(f"⚠️  Usando configuración por defecto: {e}")
            config = ConfigLoader.load()

        # Create runner with configuration
        runner = PyRateRunner(tags=args.tags, config=config)

        # Si es un archivo, lo corre directo
        if os.path.isfile(args.file):
            runner.execute_file(args.file)
        # Si eas carpeta, busca todos los .feature
        elif os.path.isdir(args.file):
            for root, dirs, files in os.walk(args.file):
                for file in files:
                    if file.endswith(".feature"):
                        runner.execute_file(os.path.join(root, file))
        else:
            print(f"❌ No encuentro el archivo o carpeta: {args.file}")


if __name__ == "__main__":
    main()