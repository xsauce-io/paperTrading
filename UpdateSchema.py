import controller

def main():
    print("Updating Indices")
    controller.update_indices()

    print("Updating Users")
    controller.update_outdated_user()






if __name__ == '__main__':
    main()