import psycopg2
import time

def query_pokemon_from_db(north, south, west, east):
    # 1. open connection
    conn = psycopg2.connect(host = "pokemon1.cozbedhsxp0j.us-west-2.rds.amazonaws.com",
                            port = 5432,
                            database="pokemon1", 
                            user="pokemon1", 
                            password="pokemon1")

    # 2. Execute SQL
    # SELECT pokemon_id, expire, latitude, longitude FROM pokemon_map WHERE latitude < 41 AND latitude>40.99 AND longitude > -73.99 AND longitude < -73.98;
    with conn.cursor() as cur:
        cur.execute("SELECT pokemon_id, expire, latitude, longitude" + 
                    " FROM pokemon_map " + 
                    " WHERE latitude < %s " + 
                    " AND latitude > %s " + 
                    " AND longitude > %s " + 
                    " AND longitude < %s " +
                    " AND expire > %s " + 
                    " LIMIT 100;",
                    (north, south, west, east, time.time() * 1000))
        items = cur.fetchall();
        pokemons = []
        for item in items:
            pokemon = {"latitude": item[2], 
                       "expire": item[1] / 1000, 
                       "longitude": item[3], 
                       "pokemon_id": item[0]}
            pokemons.append(pokemon)

    conn.close()
    return pokemons

if __name__ == "__main__":
    print query_pokemon_from_db(41, 40.99, -73.99, -73.98)
