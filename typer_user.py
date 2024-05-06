# import subprocess

import requests
import typer
from websockets import connect

cli = typer.Typer()

url = "http://127.0.0.1:8000"


token = {}


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
        headers={"Authorization": "Token 6d565122-ba07-42c4-9b71-844092e49e66"},
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
        headers={"Authorization": "Token a47dde21-0f6c-4a7f-ae57-d35a6c43b759"},
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
        headers={"Authorization": "Token a47dde21-0f6c-4a7f-ae57-d35a6c43b759"},
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
        headers={"Authorization": "Token a47dde21-0f6c-4a7f-ae57-d35a6c43b759"},
    )
    status_response = response.status_code
    if status_response == 200:
        print(response.text)


@cli.command()
def connection(room: str):
    async def get_websocket():
        uri = (
            "ws://localhost:8000/ws?room="
            + room
            + " -H 'Authorization: Token a47dde21-0f6c-4a7f-ae57-d35a6c43b759'"
        )  # Подставьте свой URI
        async with connect(uri) as websocket:
            async for message in websocket:
                typer.echo(f"Received message: {message}")

    typer.run(get_websocket)


if __name__ == "__main__":
    cli()
