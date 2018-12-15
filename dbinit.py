import os
import sys

import psycopg2 as dbapi2


INIT_STATEMENTS = [
    "CREATE TABLE IF NOT EXISTS DUMMY (NUM INTEGER)",
    "INSERT INTO DUMMY VALUES (42)",
	"ALTER TABLE users DROP CONSTRAINT users_pkey",
	"ALTER TABLE problems DROP CONSTRAINT problems_pkey",
	"ALTER TABLE messsages DROP CONSTRAINT messages_pkey",
	"ALTER TABLE users DROP CONSTRAINT users_pkey",
	"ALTER TABLE users DROP CONSTRAINT users_clannumber_fkey",
	"ALTER TABLE problems DROP CONSTRAINT messages_problem_id_fkey",
	"ALTER TABLE problems DROP CONSTRAINT problems_user_id_fkey",
	"ALTER TABLE messsages DROP CONSTRAINT  messages_clan_id_fkey",
	"ALTER TABLE messsages DROP CONSTRAINT  messages_replyof_fkey",
	"ALTER TABLE messsages DROP CONSTRAINT  messages_user_id_fkey",
	"ALTER TABLE clans DROP CONSTRAINT clans_headofclan_fkey",
	"DROP TABLE problems",
	"DROP TABLE users",
	"DROP TABLE messages",
	"DROP clans"
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
        cursor.close()


if __name__ == "__main__":
    url = os.getenv("DATABASE_URL")
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    initialize(url)
