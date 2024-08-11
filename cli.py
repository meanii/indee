#! /usr/bin/env python

from indee import configs
from argparse import ArgumentParser

def main() -> None:
    """
    main:
        main function to run the script
    """
    
    parser = ArgumentParser(prog="ive", description="indee video engine")
    
    # input files path
    parser.add_argument("-i", "--input", type=str, help="input file path")
    
    # configs 
    parser.add_argument("-m", "--mode", type=str, help="mode to run the script", choices=["server", "cli"], default="cli")
    parser.add_argument("-c", "--config", type=str, help="config file path")
    
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    args = parser.parse_args()
    
    if args.version:
        print(f"indee video engine version: {configs.version}")
    
    if args.mode == "server":
        pass # TODO: implement server mode, to run as server
    
    # load config if provided, else use default config
    if args.config:
        from indee.settings.config import load_config
        configs.config = load_config(args.config)
    
if __name__ == '__main__':
    main()