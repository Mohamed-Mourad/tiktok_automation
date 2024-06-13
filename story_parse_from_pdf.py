from pypdf import PdfReader

def parse_pdf(file_path):
    # Open the PDF file
    with open(file_path, 'rb') as file:
        reader = PdfReader(file)
        num_pages = reader.get_num_pages()

        content = ""
        for page_num in range(num_pages):
            page = reader.get_page(page_num)
            content += page.extract_text()

    # Split content into lines
    lines = content.split("\n")

    # Initialize variables to store chapters and sections
    chapters = {}
    current_chapter = None
    current_section = None

    for line in lines:
        line = line.strip()

        if line.startswith("Chapter"):
            # Extract chapter name and number
            chapter_parts = line.split(":")
            chapter_number = chapter_parts[0].split()[1]
            chapter_name = chapter_parts[1].strip().replace(" ", "_")
            current_chapter = f"Chapter_{chapter_number}_{chapter_name}"
            chapters[current_chapter] = {}

            # Reset current_section for new chapter
            current_section = None

        elif line.startswith("Section") and current_chapter:
            # Extract section name and number
            section_parts = line.split(":")
            section_number = section_parts[0].split()[1]
            section_name = section_parts[1].strip().replace(" ", "_")
            current_section = f"Section_{section_number}_{section_name}"
            chapters[current_chapter][current_section] = ""

        elif current_chapter and current_section:
            # Add paragraphs to the current section
            chapters[current_chapter][current_section] += line + " "

    # Trim excess whitespace from sections
    for chapter in chapters:
        for section in chapters[chapter]:
            chapters[chapter][section] = chapters[chapter][section].strip()

    return chapters

# Path to the PDF file
file_path = 'First Contact Sections.pdf'
Odyssey_Meets_Aelyrians = parse_pdf(file_path)

# Printing the result
for chapter, sections in Odyssey_Meets_Aelyrians.items():
    print(f"{chapter}:")
    for section, content in sections.items():
        print(f"  {section}: {content[:20]}...")  # Print first 100 characters of each section for brevity
