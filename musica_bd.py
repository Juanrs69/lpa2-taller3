"""
Script para poblar la base de datos con datos iniciales.
Añade 5 usuarios y 10 canciones con algunos favoritos de ejemplo.
"""

from sqlmodel import Session, select

from app.database import create_db_and_tables, engine
from app.models import Cancion, Favorito, Usuario


def poblar_usuarios(session: Session) -> list[Usuario]:
    """Crear 5 usuarios de ejemplo."""
    usuarios = [
        Usuario(nombre="Juan Alejandro Ramirez", correo="juan.ramirez@musica.com"),
        Usuario(nombre="María García López", correo="maria.garcia@musica.com"),
        Usuario(nombre="Carlos Rodríguez", correo="carlos.rodriguez@musica.com"),
        Usuario(nombre="Ana Martín", correo="ana.martin@musica.com"),
        Usuario(nombre="Luis Fernando Gómez", correo="luis.gomez@musica.com"),
    ]

    for usuario in usuarios:
        session.add(usuario)

    session.commit()

    # Refresh para obtener los IDs
    for usuario in usuarios:
        session.refresh(usuario)

    print(f"✅ Creados {len(usuarios)} usuarios")
    return usuarios


def poblar_canciones(session: Session) -> list[Cancion]:
    """Crear 10 canciones de ejemplo."""
    canciones = [
        Cancion(
            titulo="Bohemian Rhapsody",
            artista="Queen",
            album="A Night at the Opera",
            duracion=355,
            año=1975,
            genero="Rock",
        ),
        Cancion(
            titulo="Hotel California",
            artista="Eagles",
            album="Hotel California",
            duracion=391,
            año=1976,
            genero="Rock",
        ),
        Cancion(
            titulo="Imagine",
            artista="John Lennon",
            album="Imagine",
            duracion=183,
            año=1971,
            genero="Rock",
        ),
        Cancion(
            titulo="Billie Jean",
            artista="Michael Jackson",
            album="Thriller",
            duracion=294,
            año=1982,
            genero="Pop",
        ),
        Cancion(
            titulo="Like a Rolling Stone",
            artista="Bob Dylan",
            album="Highway 61 Revisited",
            duracion=369,
            año=1965,
            genero="Folk Rock",
        ),
        Cancion(
            titulo="Smells Like Teen Spirit",
            artista="Nirvana",
            album="Nevermind",
            duracion=301,
            año=1991,
            genero="Grunge",
        ),
        Cancion(
            titulo="What's Going On",
            artista="Marvin Gaye",
            album="What's Going On",
            duracion=232,
            año=1971,
            genero="Soul",
        ),
        Cancion(
            titulo="Purple Haze",
            artista="Jimi Hendrix",
            album="Are You Experienced",
            duracion=167,
            año=1967,
            genero="Rock",
        ),
        Cancion(
            titulo="Good Vibrations",
            artista="The Beach Boys",
            album="Smiley Smile",
            duracion=218,
            año=1966,
            genero="Pop",
        ),
        Cancion(
            titulo="Respect",
            artista="Aretha Franklin",
            album="I Never Loved a Man the Way I Love You",
            duracion=147,
            año=1967,
            genero="Soul",
        ),
    ]

    for cancion in canciones:
        session.add(cancion)

    session.commit()

    # Refresh para obtener los IDs
    for cancion in canciones:
        session.refresh(cancion)

    print(f"✅ Creadas {len(canciones)} canciones")
    return canciones


def poblar_favoritos(
    session: Session, usuarios: list[Usuario], canciones: list[Cancion]
):
    """Crear algunos favoritos de ejemplo."""
    favoritos = [
        # Juan le gustan las clásicas del rock
        Favorito(
            id_usuario=usuarios[0].id, id_cancion=canciones[0].id
        ),  # Bohemian Rhapsody
        Favorito(
            id_usuario=usuarios[0].id, id_cancion=canciones[1].id
        ),  # Hotel California
        Favorito(id_usuario=usuarios[0].id, id_cancion=canciones[7].id),  # Purple Haze
        # María prefiere soul y pop
        Favorito(id_usuario=usuarios[1].id, id_cancion=canciones[3].id),  # Billie Jean
        Favorito(
            id_usuario=usuarios[1].id, id_cancion=canciones[6].id
        ),  # What's Going On
        Favorito(id_usuario=usuarios[1].id, id_cancion=canciones[9].id),  # Respect
        # Carlos es fan de los clásicos
        Favorito(id_usuario=usuarios[2].id, id_cancion=canciones[2].id),  # Imagine
        Favorito(
            id_usuario=usuarios[2].id, id_cancion=canciones[4].id
        ),  # Like a Rolling Stone
        # Ana le gusta el grunge y rock alternativo
        Favorito(
            id_usuario=usuarios[3].id, id_cancion=canciones[5].id
        ),  # Smells Like Teen Spirit
        Favorito(id_usuario=usuarios[3].id, id_cancion=canciones[7].id),  # Purple Haze
        # Luis tiene gustos variados
        Favorito(
            id_usuario=usuarios[4].id, id_cancion=canciones[8].id
        ),  # Good Vibrations
        Favorito(
            id_usuario=usuarios[4].id, id_cancion=canciones[0].id
        ),  # Bohemian Rhapsody
    ]

    for favorito in favoritos:
        session.add(favorito)

    session.commit()
    print(f"✅ Creados {len(favoritos)} favoritos")


def verificar_datos(session: Session):
    """Verificar que los datos se crearon correctamente."""
    # Contar usuarios
    usuarios_count = len(session.exec(select(Usuario)).all())
    print(f"📊 Total usuarios en BD: {usuarios_count}")

    # Contar canciones
    canciones_count = len(session.exec(select(Cancion)).all())
    print(f"📊 Total canciones en BD: {canciones_count}")

    # Contar favoritos
    favoritos_count = len(session.exec(select(Favorito)).all())
    print(f"📊 Total favoritos en BD: {favoritos_count}")

    # Mostrar algunos ejemplos
    print("\n🎵 Algunas canciones:")
    canciones = session.exec(select(Cancion).limit(3)).all()
    for cancion in canciones:
        print(f"  - {cancion.titulo} por {cancion.artista} ({cancion.año})")

    print("\n👥 Algunos usuarios:")
    usuarios = session.exec(select(Usuario).limit(3)).all()
    for usuario in usuarios:
        print(f"  - {usuario.nombre} ({usuario.correo})")


def main():
    """Función principal para poblar la base de datos."""
    print("🚀 Iniciando población de la base de datos...")

    # Crear tablas si no existen
    create_db_and_tables()
    print("✅ Tablas creadas/verificadas")

    with Session(engine) as session:
        # Verificar si ya hay datos
        existing_usuarios = session.exec(select(Usuario)).all()
        if existing_usuarios:
            print(f"⚠️  Ya existen {len(existing_usuarios)} usuarios en la BD")
            respuesta = input("¿Deseas continuar y añadir más datos? (s/n): ")
            if respuesta.lower() != "s":
                print("❌ Operación cancelada")
                return

        # Poblar datos
        usuarios = poblar_usuarios(session)
        canciones = poblar_canciones(session)
        poblar_favoritos(session, usuarios, canciones)

        # Verificar resultados
        print("\n📋 Resumen de datos creados:")
        verificar_datos(session)

        print("\n🎉 ¡Base de datos poblada exitosamente!")
        print("🌐 Puedes probar la API en: http://127.0.0.1:8000/docs")


if __name__ == "__main__":
    main()
