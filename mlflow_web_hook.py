import mlflow
import yaml
import requests
import os

if __name__ == "__main__":
        
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    model_name = config["model_name"]

    mlflow.set_tracking_uri(config["tracking_uri"])

    # Create an MLflow client
    client = mlflow.tracking.MlflowClient()

    # Get the latest version of the model in the 'Production' stage
    latest_version = client.get_latest_versions(model_name, stages=['Production'])

    if not latest_version:
        raise Exception("No model found in production.")

    # Get the version number of the latest model
    latest_version_number = int(latest_version[0].version)

    # Get the model URI
    #model_uri = client.get_model_uri(model_name, latest_version_number) #model_uri is no longer necessary

    # Get the version number from the previous run
    previous_version_number = config.get("latest_version")

    # If the version number has changed, update the config file and print a message
    if latest_version_number != previous_version_number:
        config["latest_version"] = latest_version_number
        #config["model_uri"] = model_uri  # Model URI is no longer necessary
        with open("config.yaml", "w") as file:
            yaml.safe_dump(config, file)
        print(f"New model in production: {model_name} version {latest_version_number}")

        # Trigger a GitHub Actions workflow
        response = requests.post(
            "https://api.github.com/repos/Lohith-GL/llmops-initial/dispatches",
            headers={
                "Accept": "application/vnd.github.everest-preview+json",
                "Authorization": f"token {os.environ['PERSONAL_TOKEN']}"
            },
            json={
                "event_type": "new-model-version",
                "client_payload": {
                    "version": latest_version_number
                }
            }
        )
        response.raise_for_status()