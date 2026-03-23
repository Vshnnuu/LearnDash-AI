from src.train import main as train_main


def run():
    print("Starting training pipeline...\n")
    train_main()
    print("\nPipeline finished successfully.")


if __name__ == "__main__":
    run()