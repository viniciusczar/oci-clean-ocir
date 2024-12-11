import oci

# Configure the OCI client based on the ~/.oci/config file
config = oci.config.from_file()
artifacts_client = oci.artifacts.ArtifactsClient(config)

def get_repository_id_by_name(compartment_id, repository_name):
    """
    Gets the OCID of the repository by name.
    
    Args:
        compartment_id (str): OCID of the compartment.
        repository_name (str): Name of the repository.

    Returns:
        str: OCID of the repository, or None if not found.
    """
    response = artifacts_client.list_container_repositories(
        compartment_id=compartment_id,
        display_name=repository_name
    )
    repositories = response.data.items
    if repositories:
        return repositories[0].id
    return None

def delete_old_images(repository_id, compartment_id, retain_count=10):
    """
    Deletes all images from a repository except the most recent 'retain_count' ones.

    Args:
        repository_id (str): OCID of the repository.
        compartment_id (str): OCID of the compartment.
        retain_count (int): Number of images to be retained.
    """
    try:
        
        # Validates that the repository exists
        repo_details = artifacts_client.get_container_repository(repository_id).data
        print(f"Processing repository: {repo_details.display_name} ({repository_id})")

        # List all images in the repository, ordered by creation date
        images_response = artifacts_client.list_container_images(
            repository_id=repository_id,
            compartment_id=compartment_id,
            sort_by="TIMECREATED",
            sort_order="DESC"
        )

        images = images_response.data.items
        if len(images) <= retain_count:
            print(f"Repository {repo_details.display_name} already have {len(images)} or fewer images. Nothing to delete.")
            return

        # Identify old images to delete
        images_to_delete = images[retain_count:]
        print(f"Deleting {len(images_to_delete)} images in repository {repo_details.display_name}...")

        # Delete images
        for image in images_to_delete:
            try:
                artifacts_client.delete_container_image(image.id)
                print(f"Image {image.display_name} deleted success.")
            except oci.exceptions.ServiceError as e:
                print(f"Error deleting image {image.display_name}: {str(e)}")

    except oci.exceptions.ServiceError as e:
        print(f"Error processing repository{repository_id}: {e.message}")

def process_repository_list(file_path, compartment_id, retain_count=10):
    """
    Processes a list of repositories from a file and applies image deletion logic.

    Args:
        file_path (str): Path to the file containing the repository names.
        compartment_id (str): OCID of the compartment.
        retain_count (int): Number of images to be kept in each repository.
    """
    with open(file_path, "r") as file:
        repository_names = [line.strip() for line in file.readlines()]

    for repository_name in repository_names:
        print(f"Fetching OCID for the repository: {repository_name}")
        repository_id = get_repository_id_by_name(compartment_id, repository_name)

        if repository_id:
            delete_old_images(repository_id, compartment_id, retain_count)
        else:
            print(f"Repository {repository_name} not found in compartment {compartment_id}.")

if __name__ == "__main__":
    # Replace with actual values
    COMPARTMENT_ID = "ocid1.compartment.oc1..aaaaaa5azinlfvynq"
    FILE_PATH = "repositories.txt"  # Path to file with repository names
    RETAIN_COUNT = 10  # Number of images to keep

    process_repository_list(FILE_PATH, COMPARTMENT_ID, RETAIN_COUNT)
