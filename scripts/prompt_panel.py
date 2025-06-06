import argparse
from modules.reasoner_dispatcher import dispatch_to_reasoner


def interactive_panel() -> None:
    print("Mercurius Prompt Panel - digita 'exit' per uscire")
    while True:
        try:
            prompt = input("Prompt> ").strip()
            if prompt.lower() in {"exit", "quit"}:
                break
            if prompt:
                response = dispatch_to_reasoner(prompt)
                print(response)
        except KeyboardInterrupt:
            break


def main() -> None:
    parser = argparse.ArgumentParser(description="Mercurius Prompt Panel")
    parser.add_argument("--prompt", help="Prompt singolo da inviare", default=None)
    args = parser.parse_args()
    if args.prompt:
        print(dispatch_to_reasoner(args.prompt))
    else:
        interactive_panel()


if __name__ == "__main__":
    main()
