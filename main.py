import orjson
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


class Anime(BaseModel):
    title: str
    rating: float
    type: str
    episodes: int
    airing: str
    url: str
    
    @staticmethod
    def from_dict(data: dict):
        record = Anime(**data)
        return record

class Problem(BaseModel):
    detail: str

class Database:
    def __init__(self):
        self._data: list = []

    def load_from_file(self, filename: str):
        with open(filename, "rb") as f:
            data = orjson.loads(f.read())
            for record in data:
                obj = Anime.from_dict(record)
                self._data.append(obj)

    def delete(self, id_anime: int):
        if 0 < id_anime >= len(self._data):
            return
        self._data.pop(id_anime)

    def add(self, anime: Anime):
        self._data.append(anime)

    def get(self, id_anime: int):
        if 0 < id_anime >= len(self._data):
            return
        return self._data[id_anime]

    def get_all(self) -> list[Anime]:
        return self._data

    def update(self, id_anime: int, anime: Anime):
        if 0 < id_anime >= len(self._data):
            return
        self._data[id_anime] = anime

    def count(self) -> int:
        return len(self._data)


db = Database()
db.load_from_file('anime.json')

app = FastAPI(title="Anime Charts", version="1.0", docs_url="/docs")
app.is_shuitdown = False

@app.get("/animes", response_model=list[Anime], description="Vrátí seznam anime")
async def get_animes():
    return db.get_all()

@app.get("/animes/{id_anime}", response_model=Anime)
async def get_anime(id_anime: int):
    return db.get(id_anime)

@app.post("/animes", response_model=Anime, description="Přidání anime do databáze")
async def post_animes(anime: Anime):
    db.add(anime)
    return anime

@app.delete("/movies/{id_anime}", description="Smazání anime z databáze", responses={
    404: {'model': Problem}
})
async def delete_anime(id_anime: int):
    anime = db.get(id_anime)
    if anime is None:
        raise HTTPException(404, "Anime neexistuje")
    db.delete(id_anime)
    return {'status': 'smazáno'}

@app.patch("/movies/{id_anime}", description="Aktualizuje anime do databáze", responses={
    404: {'model': Problem}
})
async def update_anime(id_anime: int, updated_anime: Anime):
    anime = db.get(id_anime)
    if anime is None:
        raise HTTPException(404, "Anime neexistuje")
    db.update(id_anime, updated_anime)
    return {'old': anime, 'new': updated_anime}