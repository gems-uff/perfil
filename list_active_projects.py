from datetime import datetime
import populate_database
from database.entities.researcher import Researcher

def main():
    session = populate_database.main()
    researchers = session.query(Researcher).all()

    for researcher in researchers:
        print(f'\n{researcher.name}')
        for membership in researcher.memberships:
            project = membership.project
            if project.end_year == "":
                print(f'- {datetime.now().year - project.start_year} anos no projeto "{project.name}"')

if __name__ == "__main__":
    main()
