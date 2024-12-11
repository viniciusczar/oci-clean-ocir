import oci

# Configure the OCI client based on the ~/.oci/config file
config = oci.config.from_file()
artifacts_client = oci.artifacts.ArtifactsClient(config)

def get_repositories_with_images_over_limit(compartment_id, limit=10):
    """
    Searches for repositories in the Oracle Container Registry with more than 'limit' images.
    
    Args:
        compartment_id (str): OCID of the compartment where the repositories are located.
        limit (int): Limit of images to filter repositories.

    Returns:
        List[Dict]: List of repositories with more than 'limit' images.
    """
    repositories = []
    response = artifacts_client.list_container_repositories(compartment_id=compartment_id)

    for repo in response.data.items:  # Access response items
        # Count the images in the repository
        images_response = artifacts_client.list_container_images(
            repository_id=repo.id,
            compartment_id=compartment_id  # Adding the required argument
        )
        image_count = len(images_response.data.items)  # Access response items

        if image_count > limit:
            repositories.append({
                'name': repo.display_name,
                'image_count': image_count,
                'repository_id': repo.id
            })

    return repositories

if __name__ == "__main__":
    # Replace with the OCID of your compartment
    COMPARTMENT_ID = "ocid1.compartment.oc1..aaaaaa5azinlfvynq"

    # Image limit per repository
    IMAGE_LIMIT = 10

    repos_with_images = get_repositories_with_images_over_limit(COMPARTMENT_ID, IMAGE_LIMIT)

    print("Repositories with more than 10 images:")
    for repo in repos_with_images:
        print(f"- {repo['name']} ({repo['image_count']} imagens)")
