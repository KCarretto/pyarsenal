import argparse
import getpass

from pyclient import ArsenalClient

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('username')
    args = parser.parse_args()

    client = None
    if ArsenalClient.api_key_exists('.arsenal_key'):
        client = ArsenalClient(
            api_key_file='.arsenal_key'
        )
    else:
        username = input("Username: ")
        password = getpass("Password: ")
        client = ArsenalClient(
            username=username,
            password=password,
        )


    print('Creating user {}'.format(args.username))
    client.create_user(args.username, 'PleaseChangeThis!-1234')

    client.add_role_member('attacker', args.username)
    client.add_role_member('manage-self', args.username)
    client.add_role_member('spectator', args.username)
    client.add_role_member('logger', args.username)

if __name__ == '__main__':
    main()
