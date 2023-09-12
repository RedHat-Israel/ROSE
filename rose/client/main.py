import argparse
import importlib.util
import logging

from game import server


def load_driver_module(driver_path):
    """
    Load the driver module from the specified path.

    Arguments:
      file_path (str): The path to the driver module
    Returns:
        Driver module (module)
    Raises:
        Exception if the module cannot be loaded
    """
    spec = importlib.util.spec_from_file_location("driver_module", driver_path)
    driver_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(driver_module)
    return driver_module


def main():
    """
    Main function to initialize and run the driver HTTP server.
    """
    parser = argparse.ArgumentParser(description="Run a ROSE driver HTTP service.")
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8081,
        help="Specify the port number. Default is 8081.",
    )
    parser.add_argument(
        "--listen",
        default="",
        help="Specify the listen address. Default is all interfaces.",
    )
    parser.add_argument(
        "--name",
        default="rose-driver",
        help="Specify the server name for logging purposes. Default is 'rose-driver'.",
    )
    parser.add_argument(
        "-d",
        "--driver",
        default="",
        help="Specify the path to the driver module.",
    )
    parser.add_argument(
        "--log", default="WARNING", help="Set the logging level. E.g. --log DEBUG"
    )

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.log.upper()))

    if args.driver == "":
        print("Error: missing driver command line argument")
        return

    try:
        driver_module = load_driver_module(args.driver)
        server.MyHTTPRequestHandler.server_name = args.name
        server.MyHTTPRequestHandler.drive = driver_module.drive
        server.MyHTTPRequestHandler.driver_name = driver_module.driver_name

        print(f"\nDriver module {args.driver} [driver: {driver_module.driver_name}]")
    except ImportError as e:
        print(e)
        return  # Exit the main function if the module loading fails

    with server.MyTCPServer(
        (args.listen, args.port), server.MyHTTPRequestHandler
    ) as httpd:
        try:
            print(f"Listen      {args.listen}:{args.port}")
            print(f"Server URL  http://127.0.0.1:{args.port}")
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down the server...")
            httpd.shutdown()
            httpd.server_close()


if __name__ == "__main__":
    main()
