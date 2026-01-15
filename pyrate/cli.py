import argparse
import os
import sys
from .core import PyRateRunner
from .logger import log_success, log_info
from .config_loader import ConfigLoader


def init_project():
    folders = ["tests/features", "tests/data", "reports"]
    for f in folders:
        os.makedirs(f, exist_ok=True)

    with open(".env", "w") as f:
        f.write("BASE_URL=https://jsonplaceholder.typicode.com")

    with open("tests/features/demo.feature", "w") as f:
        f.write("# @smoke\nGiven url '#(BASE_URL)'\nAnd path 'users/1'\nWhen method get\nThen status 200")
    
    # Generate example config file
    ConfigLoader.save_example_config()

    log_success("Proyecto PyRate inicializado 🚀")


def main():
    parser = argparse.ArgumentParser(
        description="PyRate Framework CLI - Automation Testing for API and UI",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Version argument
    parser.add_argument(
        '-v', '--version', 
        action='version', 
        version='PyRate Framework 1.0.2'
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
        # Load configuration (custom file or defaults)
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
        # Si es carpeta, busca todos los .feature
        elif os.path.isdir(args.file):
            for root, dirs, files in os.walk(args.file):
                for file in files:
                    if file.endswith(".feature"):
                        runner.execute_file(os.path.join(root, file))
        else:
            print(f"❌ No encuentro el archivo o carpeta: {args.file}")


if __name__ == "__main__":
    main()