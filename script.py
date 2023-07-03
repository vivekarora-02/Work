import argparse
import json
import os
import requests


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def calculate_total_cost(data, num_guests):
    per_guest_price = int(data['cost_per_head'])
    total_cost = per_guest_price * num_guests
    return total_cost


def display_agenda(data):
    agenda = data['agenda']
    print("Full Agenda:")
    for item in agenda:
        print(item)


def download_images(data, folder):
    agenda = data['agenda']
    for item in agenda:
        image_url = item.get('image')
        if image_url:
            if not image_url.startswith('http'):
                image_url = 'http://' + image_url  # Add the schema if missing
            image_name = os.path.basename(image_url)
            image_file_path = os.path.join(folder, image_name)
            image_file_path += ".jpeg"  # Add the file extension
            # Create the directory if it doesn't exist
            os.makedirs(folder, exist_ok=True)
            response = requests.get(image_url)
            with open(image_file_path, 'wb') as image_file:
                image_file.write(response.content)
            print("Downloaded image: " + image_file_path)


def main():
    parser = argparse.ArgumentParser(description='JSON File Loader')
    parser.add_argument('file_path', type=str, help='Path to the JSON file')
    parser.add_argument('num_guests', type=int, help='Number of guests')
    parser.add_argument('--display_agenda', action='store_true',
                        help='Display the full agenda')
    parser.add_argument('--download_images', action='store_true',
                        help='Download images in the agenda')

    args = parser.parse_args()

    file_path = args.file_path
    num_guests = args.num_guests
    display_agenda_flag = args.display_agenda
    download_images_flag = args.download_images

    json_data = load_json_file(file_path)

    total_cost = calculate_total_cost(json_data, num_guests)
    print("Total cost for {} guests: ${}".format(num_guests, total_cost))

    if display_agenda_flag:
        display_agenda(json_data)

    if download_images_flag:
        folder = 'images'
        os.makedirs(folder, exist_ok=True)
        download_images(json_data, folder)


if __name__ == '__main__':
    main()
