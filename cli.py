import click

@click.group()
def cli():
    pass

@click.command()
@click.option('--website_add', help='Enter the website to be added')
@click.argument("website_add")
def add_site(website_add):
    """
    Reads the sites.txt file, adds new website to the file.
    If no file existing, creates sites.txt file and then
    adds new website to the file.
    
    """
    try:
        with open("sites.txt", "a", encoding="utf-8") as add_file:
            add_file.write(str(website_add + '\n'))
            print("Website added to the text file")
    except FileNotFoundError:
        with open("sites.txt", "a", encoding="utf-8") as add_file:
            add_file.write(str(website_add + '\n'))
            print("Website added to the text file")

@click.command()
@click.option('--website_del', help='Enter the website to be deleted')
@click.argument("website_del")
def delete_site(website_del):
    """
    Opens the sites.txt, reads each line of file.
    Finds whether data is present in the text file, 
    -> if True(there is data in the file), remove the specific website from sites.txt file.
    -> or else(no data in the file), prints website not present.
    If No file present, prints no file created.
    
    """
    try:
        with open("sites.txt", "r", encoding="utf-8") as sites_file:
            web_data = sites_file.readlines()
        with open("sites.txt", "w", encoding="utf-8") as sites_file:
            if web_data:
                for data in web_data:
                    if data.strip("\n") != website_del:
                        sites_file.write(data)
                print('Website deleted from text file')
            else:
                print('Website not present in text file')
    except FileNotFoundError:
        print('No file created')

cli.add_command(add_site)
cli.add_command(delete_site)

# def main():
#     """
#     main function

#     """
#     add_site()
#     # cli.add_command(add_site)
#     # cli.add_command(delete_site)

if __name__ == "__main__":
    cli()