import asyncio
import websockets
import json

class DerivEngine:
    def __init__(self):
        self.url = "wss://ws.derivws.com/websockets/v3?app_id=1089"
        self.digits_history = []
        self.neglect_counts = {i: 0 for i in range(10)}
        self.signal = "WAITING"

    async def connect(self, symbol="R_100"):
        async with websockets.connect(self.url) as websocket:
            await websocket.send(json.dumps({"ticks": symbol, "subscribe": 1}))
            while True:
                data = json.loads(await websocket.recv())
                if "tick" in data:
                    price = float(data["tick"]["quote"])
                    digit = int(str(price)[-1])
                    self.update(digit)

    def update(self, digit):
        self.digits_history.append(digit)
        if len(self.digits_history) > 50: self.digits_history.pop(0)
        for i in range(10):
            self.neglect_counts[i] = 0 if i == digit else self.neglect_counts[i] + 1
        
        last_3 = self.digits_history[-3:] if len(self.digits_history) >= 3 else []
        if all(d < 3 for d in last_3) and len(last_3) == 3:
            self.signal = "SLAYER SIGNAL: OVER 2"
        else:
            self.signal = "SCANNING"
