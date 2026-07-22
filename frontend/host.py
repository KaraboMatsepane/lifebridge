from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

personas = [
    {
    "id":1,
    "name": "Karabo",
    "role": "policyholder",
    "deceased_flag": False},

    {
    "id":2,
    "name": "Sinoxolo",
    "role": "policyholder",
    "deceased_flag": True},

    {
    "id":3,
    "name": "Thobeka",
    "role": "beneficiary",
    "deceased_flag": False},

    {
    "id":4,
    "name": "Tshepiso",
    "role": "beneficiary",
    "deceased_flag": False}
    ]

@app.get("/", response_class=HTMLResponse)
def choose_persona():
    html = """
    <h1>Lifebridge host</h1>
    <h2>Choose a persona:</h2>
    """

    for user in personas:
        name          = user.get("name")
        role          = user.get("role")
        deceased_flag = user.get("deceased_flag")
        id            = user.get("id")

        html += f"""
        <p>
            {name}<br>
            {role}<br>
            Deceased_flag: {str(deceased_flag)}<br>
        </p>
        
        <form action="/mint" method="post">
            <input
                type="hidden"
                name="persona_id"
                value="{id}"
            >
            
            <button>Log in as {name}</button>
        </form>
        """

    return html