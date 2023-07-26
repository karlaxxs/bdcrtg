from fastapi import FastAPI
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configurar los orígenes permitidos (* permite todos los orígenes)
origins = ["*"]

# Agregar el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variable para almacenar los datos en forma de diccionario
usuarios = {}

# Modelo de datos para la creación de usuarios
class Usuario(BaseModel):
    nombre: str
    contra_correcta: int
    tipo_token: int
    token1:str
    token2:str
    token3:str

# Ruta para crear un nuevo usuario
@app.post("/usuarios")
def crear_usuario(usuario: Usuario):
    # Verificar si el usuario ya existe por su nombre
    if usuario.nombre in usuarios:
        # Actualizar los datos del usuario existente
        usuarios[usuario.nombre]["datos"] = usuario
        return {"message": "Usuario actualizado exitosamente", "usuario_id": usuarios[usuario.nombre]["id"]}
    else:
        # Generar un ID único para el usuario
        usuario_id = len(usuarios) + 1
        # Agregar el usuario al diccionario
        usuarios[usuario.nombre] = {"id": usuario_id, "datos": usuario}
        return {"message": "Usuario creado exitosamente", "usuario_id": usuario_id}


# Ruta para obtener un usuario por nombre
@app.get("/usuarios/{nombre}")
def obtener_usuario_por_nombre(nombre: str):
    for key, value in usuarios.items():
        if value["datos"].nombre == nombre:
            return {"usuario_id": value["id"], "datos": value["datos"]}
    return {"error": "Usuario no encontrado"}

# Ruta para actualizar un usuario por nombre
@app.put("/usuarios/{nombre}")
def actualizar_usuario_por_nombre(nombre: str, usuario: Usuario):
    for key, value in usuarios.items():
        if value["datos"].nombre == nombre:
            usuarios[key]["datos"] = usuario
            return {"message": "Usuario actualizado exitosamente"}
    return {"error": "Usuario no encontrado"}

# Ruta para eliminar un usuario por nombre
@app.delete("/usuarios/{nombre}")
def eliminar_usuario_por_nombre(nombre: str):
    for key, value in usuarios.items():
        if value["datos"].nombre == nombre:
            del usuarios[key]
            return {"message": "Usuario eliminado exitosamente"}
    return {"error": "Usuario no encontrado"}
