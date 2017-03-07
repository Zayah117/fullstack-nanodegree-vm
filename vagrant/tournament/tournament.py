#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        db = psycopg2.connect("dbname=tournament")
        cursor = db.cursor()
        return db, cursor
    except:
        print("Could not connect to database")

def deleteMatches():
    """Remove all the match records from the database.""" 
    conn, cur = connect()
    cur.execute("""TRUNCATE TABLE matches CASCADE;""")
    conn.commit()
    conn.close()

def deletePlayers():
    """Remove all the player records from the database."""
    conn, cur = connect()
    cur.execute("""TRUNCATE TABLE players CASCADE;""")
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn, cur = connect()
    cur.execute("""SELECT COUNT(*) FROM players;""")
    count = cur.fetchall()
    conn.close()
    return count[0][0]


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    conn, cur = connect()
    QUERY = """INSERT INTO players (name) VALUES (%s);"""
    cur.execute(QUERY, (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn, cur = connect()
    cur.execute("""SELECT players.id, players.name, COUNT(matches.winner) as wins, COUNT(matches.winner + matches.loser) as matches FROM players LEFT JOIN matches on players.id = matches.winner GROUP BY players.id;""")
    rows = cur.fetchall()
    conn.close()
    return rows


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    conn, cur = connect()

    QUERY = """UPDATE players SET matches = matches + 1 WHERE id = %s or id = %s"""
    cur.execute(QUERY, (str(winner), str(loser)))

    QUERY = """UPDATE players SET wins = wins + 1 WHERE id = %s"""
    cur.execute(QUERY, (str(winner),))

    conn.commit()
    conn.close()
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    conn, cur = connect()
    cur.execute("""SELECT id, name FROM players ORDER BY wins DESC""")

    players = cur.fetchall()
    my_tuple = ()
    for i in range(len(players)):
        if i % 2 == 0:
            my_tuple = my_tuple + (players[i] + players[i + 1],)

    conn.close()

    return my_tuple