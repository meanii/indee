#! /usr/bin/env python

from indee import configs, logger
from indee.cli import IndeeCli

from argparse import ArgumentParser

def main() -> None:
    """
    main:
        main function to run the script
    """
    parser = ArgumentParser(prog="ive", description="indee video engine")
    
    # configs flags, to run in server mode, or cli mode
    parser.add_argument("-m", "--mode", type=str, help="mode to run the script", choices=["server", "cli"], default="cli")
    parser.add_argument("-c", "--config", type=str, help="config file path")
    
    # input flags, to provide input file path
    parser.add_argument("-i", "--input", type=str, help="input file path")
    
    # extra flags, to show version
    parser.add_argument("-v", "--version", action="store_true", help="show version")
    args = parser.parse_args()
    
    logger.info(f'indee video engine started with mode: {args.mode}')
    logger.info(f'indee-video-engine version: {configs.config.version}')
    
    if args.version:
        print(f"indee video engine version: {configs.config.version}")
    
    # load config if provided, else use default config
    if args.config:
        from indee.settings.config import load_config
        configs.config = load_config(args.config)
    
    if args.mode == "server":
        pass # TODO: implement server mode, to run as server
    
    if args.mode == "cli":
        cli = IndeeCli(configs.config, args)
        cli.run()
    
if __name__ == '__main__':
    main()