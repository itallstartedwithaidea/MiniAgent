"""MiniAgent CLI entry point."""

import sys


def main():
    if len(sys.argv) < 2:
        print("MiniAgent — The Cowork Agent for Everything")
        print("")
        print("Commands:")
        print("  miniagent chat           — Terminal chat")
        print("  miniagent serve          — OpenAI-compatible API server")
        print("  miniagent train          — Train a model")
        print("  miniagent eval           — Run benchmarks")
        print("  miniagent download-data  — Download training datasets")
        return

    cmd = sys.argv[1]
    sys.argv = sys.argv[1:]  # Shift args

    if cmd == "chat":
        from miniagent.chat import main as chat_main
        chat_main()
    elif cmd == "serve":
        from scripts.serve_openai_api import main as serve_main
        serve_main()
    elif cmd == "eval":
        from eval.advertising_bench import main as eval_main
        eval_main()
    elif cmd == "download-data":
        from scripts.download_data import main as dl_main
        dl_main()
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
