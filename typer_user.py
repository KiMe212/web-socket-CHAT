import os

import requests
import typer

cli = typer.Typer()

url = "http://127.0.0.1:8000"

user_token = "e0016504-6119-410e-995a-b205b55e7aea"


@cli.command()
def signup(name: str, password: str):
    response = requests.post(
        url=url + "/signup", json={"name": name, "password": password}
    )
    status_response = response.status_code
    if status_response == 200:
        print("Success")
    elif status_response == 400:
        print(response.text)


@cli.command()
def login(name: str, password: str):
    response = requests.post(
        url=url + "/login", json={"name": name, "password": password}
    )
    status_response = response.status_code
    if status_response == 200:
        token = response.json()
        print(token)
        print("Success")
    elif status_response == 400:
        print(response.text)


@cli.command()
def logout():
    response = requests.delete(
        url=url + "/logout",
        headers={"Authorization": f"Token {user_token}"},
    )
    status_response = response.status_code
    if status_response == 200:
        print("Success")
    else:
        print(response.text)


@cli.command()
def create_room(name_room: str):
    response = requests.post(
        url=url + "/room",
        json={"name": name_room},
        headers={"Authorization": f"Token {user_token}"},
    )
    status_response = response.status_code
    print(status_response)
    if status_response == 200:
        print("Success")
    # elif status_response == 307:
    #     print("Redirect")
    else:
        print(response.text)


@cli.command()
def delete_room(name_room: str):
    response = requests.delete(
        url=url + "/room",
        json={"name": name_room},
        headers={"Authorization": f"Token {user_token}"},
    )
    status_response = response.status_code
    if status_response == 200:
        print("Success")
    # elif status_response == 307:
    #     print("Redirect")
    else:
        print(response.text)


@cli.command()
def all_rooms():
    response = requests.get(
        url=url + "/room",
    )
    status_response = response.status_code
    if status_response == 200:
        print(response.text)


@cli.command()
def connection(room: str):
    cmd = (
        f"wscat -c 127.0.0.1:8000/ws?room={room} -H 'Authorization: Token {user_token}'"
    )
    os.system(cmd)


if __name__ == "__main__":
    cli()
