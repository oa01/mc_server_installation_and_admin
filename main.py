import os
import shutil
import subprocess
import requests
from inquirer import prompt, List, Path

minecraft_versions = {
    "1.16.5": {
        "Vanilla": "https://piston-data.mojang.com/v1/objects/1b557e7b033b583cd9f66746b7a9ab1ec1673ced/server.jar",
        "Forge": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.16.5-36.2.34/forge-1.16.5-36.2.34-installer.jar"
    },
    "1.20.1": {
        "Vanilla": "https://piston-data.mojang.com/v1/objects/84194a2f286ef7c14ed7ce0090dba59902951553/server.jar",
        "Forge": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.20.1-47.1.0/forge-1.20.1-47.1.0-installer.jar"
    },
    "1.12.2": {
        "Forge": "https://maven.minecraftforge.net/net/minecraftforge/forge/1.12.2-14.23.5.2859/forge-1.12.2-14.23.5.2859-installer.jar",
        "Vanilla": "https://piston-data.mojang.com/v1/objects/886945bfb2b978778c3a0288fd7fab09d315b25f/server.jar"

    },
    "1.8.9": {
        "Vanilla": "https://launcher.mojang.com/v1/objects/b58b2ceb36e01bcd8dbf49c8fb66c55a9f0676cd/server.jar"
    }
}

def download_file(url, destination):
    response = requests.get(url, stream=True)
    with open(destination, 'wb') as file:
        shutil.copyfileobj(response.raw, file)

def main():
    version_choices = [version for version in minecraft_versions]
    version_prompt = [List('version', message="Select Minecraft version:", choices=version_choices)]
    selected_version = prompt(version_prompt)['version']

    type_choices = list(minecraft_versions[selected_version].keys())
    type_prompt = [List('type', message="Select installation type:", choices=type_choices)]
    selected_type = prompt(type_prompt)['type']

    download_url = minecraft_versions[selected_version][selected_type]

    installation_directory_prompt = [Path('directory', message="Enter the installation directory:", default=os.getcwd())]
    installation_directory = prompt(installation_directory_prompt)['directory']
    if not os.path.exists(installation_directory):
        os.makedirs(installation_directory)

    installer_filename = os.path.basename(download_url)
    installer_path = os.path.join(installation_directory, installer_filename)

    download_file(download_url, installer_path)
    print(f"Downloaded {installer_filename}")

    if selected_type == "Forge":
        os.chdir(installation_directory)
        shutil.move(installer_path, os.path.join(installation_directory, installer_filename))
        subprocess.run(["sudo", "java", "-jar", installer_filename, "--installServer"])
        print("Forge installation completed.")
    else:
        print("Vanilla installation completed.")

if __name__ == "__main__":
    main()
