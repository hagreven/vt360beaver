import sys
import os

# Path to the repository

# Directory where audio files are pushed
AUDIO_FOLDER = "media/"

# Directory where new HTML files will be created
HTML_FOLDER = "pages/"

# Path to README.md
README_PATH = "README.md"

# Functions

def update_readme(filename, html_filename):
    """Update the readme file to link to a file's html audio page"""

    # Read the contents of README.md
    with open(README_PATH, "r") as readme_file:
        readme_content = readme_file.readlines()
    
    # Find the line number where to insert the link in the ## Audios section
    audios_start_index = -1
    audios_end_index = -1
    for i, line in enumerate(readme_content):
        if line.strip() == "## Audios":
            audios_start_index = i
        elif audios_start_index != -1 and line.startswith("#"):
            audios_end_index = i - 1
            break
    
    # If the ## Audios section is found, insert the link
    if audios_start_index != -1:
        # Construct the link
        link_text = os.path.splitext(filename)[0].replace('_', ' ')
        link_markdown = f"[{link_text}]({HTML_FOLDER + html_filename})"
        # Insert the link below the ## Audios section
        readme_content.insert(audios_end_index, f"* {link_markdown}\n")
        # Write the updated contents back to README.md
        with open(README_PATH, "w") as readme_file:
            readme_file.writelines(readme_content)
        print(f"Add link to {html_filename} in README.md ✔")
    else:
        print("Section '## Audios' not found in README.md. Link was not added.")

def create_html_pages():
    """Create html audio pages for all files pushed to a specific folder"""
        
    # Get the list of files
    files = []
    
    for filename in os.listdir(AUDIO_FOLDER):
        # Check if the path is a file (not a directory)
        if os.path.isfile(os.path.join(AUDIO_FOLDER, filename)):
            # Print the filename
            files.append(filename)
    
    # Loop through each new file
    for file in files:
        # Check if the file is in the pushed folder
        # Get the filename without the path
        filename = os.path.basename(file)
        
        # Create the corresponding HTML filename
        html_filename = os.path.splitext(filename)[0] + ".html"

        # Only update if the file is new
        if not html_filename in os.listdir(HTML_FOLDER):
        
            # Create HTML page with an audio element
            audio_html = f'''<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width; height=device-height;">
        <link rel="stylesheet" href="resource://content-accessible/TopLevelVideoDocument.css">
        <script type="text/javascript" src="chrome://global/content/TopLevelVideoDocument.js"></script>
        <title>{os.path.splitext(filename)[0].replace('_', ' ')}</title>
    </head>
    <body>
        <video autoplay controls style="height: 40px; width: 100%">
            <source src="./../media/{filename}" type="audio/mpeg">
            Your browser does not support the audio element.
        </video>
    </body>
</html>'''
            
            # Write the HTML content to a new file in the HTML folder
            with open(os.path.join(HTML_FOLDER, html_filename), "w") as html_file:
                html_file.write(audio_html)
            
            print(f"Create HTML page for {filename} ✔")
        
            update_readme(filename, html_filename)
        else:
            print(f"{filename} is already published ✔")

# Main Script
if __name__ == "__main__":
    print("Starting to link audios...")
    create_html_pages()
    print("Done!")