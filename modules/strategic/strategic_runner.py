"""CLI per eseguire il modulo StrategicBrain."""
import argparse
from pathlib import Path

from .strategic_brain import StrategicBrain


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Strategic Brain goals")
    parser.add_argument("goals", nargs="?", default="goals.txt", help="File dei goal o singolo obiettivo")
    args = parser.parse_args()

    brain = StrategicBrain()

    if Path(args.goals).is_file():
        brain.load_goals(args.goals)
    else:
        brain.goal_manager.add_goal(args.goals)

    results = brain.run()
    for res in results:
        print(res)


if __name__ == "__main__":
    main()
