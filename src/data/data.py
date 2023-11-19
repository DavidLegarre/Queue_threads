from datetime import datetime, timedelta

# Get the current time
dt = datetime.now()

# Perform calculations with timedelta to get different times
dt2 = dt + timedelta(seconds=20)
dt3 = dt2 + timedelta(seconds=30)

dt_ = dt.strftime("%H:%M:%S")
dt2_ = dt2.strftime("%H:%M:%S")
dt3_ = dt3.strftime("%H:%M:%S")

client = [("cliente", dt_, "Hola soy el cliente"), ("cliente", dt3_, "Adios")]

agent = [("agente", dt2_, "Hola soy el agente")]

client_style = """
background-color: lightblue;
padding: 8px;
border-radius: 8px;
"""

agent_style = """
background-color: green;
padding: 8px;
border-radius: 8px;
"""

input_style = """
background-color: yellow;
padding: 8px;
border-radius: 8px;
"""

companion_style = """
background-color: cyan;
padding: 8px;
border-radius: 8px;
"""

companion = [(dt_, "Hola, soy el GPT"), (dt2_, "Recomiendo xxx"), (dt3_, "Adios GPT")]
