import sys, argparse, time

# imports

def main(argv: list[str]) -> int:

    parser = argparse.ArgumentParser(description="Music Library ffmpeg converter")
    parser.add_argument("--log",action="store_true",help="Use argument to log operations to .txt output")

    args = parser.parse_args(argv[1:])

    print("\n"+"="*25+"Music library converter tool"+"="*25+"\n")
    time.sleep(1)
    
    # placeholder

if __name__ == "__main__" :
    main(sys.argv)