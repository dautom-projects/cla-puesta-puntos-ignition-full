# Project Library: project.users
# Funciones de gestion de usuarios PAPO
# - Consultas multi-source (ClariosAD + papo_db_users)
# - CRUD sobre papo_db (texto plano)

USER_SOURCES = ["ClariosAD", "papo_db_users"]
SUPERVISOR_ROLE = "Supervisor_PAPO"
DS = "papo_db"


# =====================================================
# CONSULTAS (multi-source: ClariosAD + papo_db_users)
# =====================================================

def get_supervisors_by_area(lineRole):
    """Obtiene la lista de supervisores de un area especifica.
    
    Filtra usuarios que tengan AMBOS roles:
      - Supervisor_PAPO (rol funcional)
      - El rol de area pasado como parametro (NFR, ENSAMBLE, RECICLADO, OREC)
    
    Consulta ambos User Sources (ClariosAD + papo_db_users) y deduplica
    por username (no por nombre completo, para evitar duplicados por
    diferencias de tildes/capitalizacion).
    
    Args:
        lineRole (str): nombre del rol de area (ENSAMBLE, RECICLADO, OREC, NFR)
    
    Returns:
        list[str]: nombres completos ordenados alfabeticamente.
                   Lista vacia si lineRole es None/vacio o si hay error.
    """
    logger = system.util.getLogger("dautom.users.get_supervisors_by_area")
    
    if not lineRole:
        logger.warn("get_supervisors_by_area called with empty lineRole")
        return []
    
    supervisorMap = {}
    
    for userSource in USER_SOURCES:
        try:
            allUsers = system.user.getUsers(userSource)
        except Exception as e:
            logger.warn("Could not query user source '{}': {}".format(userSource, str(e)))
            continue
        
        for user in allUsers:
            userRoles = list(user.getRoles())
            
            if SUPERVISOR_ROLE in userRoles and lineRole in userRoles:
                username = user.get("username")
                
                if username in supervisorMap:
                    continue
                
                firstName = user.get("firstname")
                lastName = user.get("lastname")
                
                if firstName and lastName:
                    fullName = "{} {}".format(firstName, lastName)
                elif firstName:
                    fullName = firstName
                elif lastName:
                    fullName = lastName
                else:
                    fullName = username
                
                supervisorMap[username] = fullName
    
    return sorted(supervisorMap.values())


def get_users_by_roles(requiredRoles, matchAll=True):
    """Obtiene usuarios que cumplen un conjunto de roles.
    
    Util si necesitas filtros mas flexibles (ej: operarios de un area,
    o supervisores que tambien sean MANTTO, etc).
    
    Args:
        requiredRoles (list[str]): lista de roles a buscar
        matchAll (bool): True = el usuario debe tener TODOS los roles (AND)
                         False = el usuario debe tener AL MENOS UNO (OR)
    
    Returns:
        list[dict]: cada dict tiene {username, firstname, lastname, fullname, roles, source}
                    Ordenado alfabeticamente por fullname.
    """
    logger = system.util.getLogger("dautom.users.get_users_by_roles")
    
    if not requiredRoles:
        return []
    
    requiredSet = set(requiredRoles)
    result = {}
    
    for userSource in USER_SOURCES:
        try:
            allUsers = system.user.getUsers(userSource)
        except Exception as e:
            logger.warn("Could not query user source '{}': {}".format(userSource, str(e)))
            continue
        
        for user in allUsers:
            userRoles = set(list(user.getRoles()))
            
            if matchAll:
                matches = requiredSet.issubset(userRoles)
            else:
                matches = bool(requiredSet & userRoles)
            
            if matches:
                username = user.get("username")
                if username in result:
                    continue
                
                firstName = user.get("firstname") or ""
                lastName = user.get("lastname") or ""
                fullName = (firstName + " " + lastName).strip() or username
                
                result[username] = {
                    "username": username,
                    "firstname": firstName,
                    "lastname": lastName,
                    "fullname": fullName,
                    "roles": sorted(list(userRoles)),
                    "source": userSource
                }
    
    return sorted(result.values(), key=lambda u: u["fullname"])


# =====================================================
# CRUD (solo papo_db_users)
# =====================================================

def crear_usuario(username, password, firstname, lastname, email, roles, badge=None):
    """Crea un usuario nuevo en PAPO con sus roles.
    
    Args:
        username (str): username unico
        password (str): clave en texto plano
        firstname (str): primer nombre
        lastname (str): primer apellido
        email (str|None): correo o None
        roles (list[str]): lista de nombres de rol (ej: ["Operator", "NFR"])
        badge (str|None): UID NFC, None por ahora
    Returns:
        dict: {"success": bool, "userID": int|None, "error": str|None}
    """
    tx = system.db.beginTransaction(DS, system.db.READ_COMMITTED, 30000)
    try:
        exists = system.db.runPrepQuery(
            "SELECT COUNT(*) AS n FROM dbo.users WHERE Username = ?",
            [username], DS, tx
        )
        if exists[0]["n"] > 0:
            raise Exception("Username '" + username + "' ya existe")

        system.db.runPrepUpdate(
            """INSERT INTO dbo.users
               (Username, Password, FirstName, LastName, Email, Enabled, Badge)
               VALUES (?, ?, ?, ?, ?, 1, ?)""",
            [username, password, firstname, lastname, email, badge], DS, tx
        )

        user_row = system.db.runPrepQuery(
            "SELECT ID FROM dbo.users WHERE Username = ?",
            [username], DS, tx
        )
        user_id = user_row[0]["ID"]

        for role_name in roles:
            n = system.db.runPrepUpdate(
                """INSERT INTO dbo.user_roles (UserID, RoleID)
                   SELECT ?, ID FROM dbo.roles WHERE RoleName = ?""",
                [user_id, role_name], DS, tx
            )
            if n == 0:
                raise Exception("Rol '" + role_name + "' no existe")

        system.db.commitTransaction(tx)
        return {"success": True, "userID": user_id, "error": None}

    except Exception as e:
        system.db.rollbackTransaction(tx)
        return {"success": False, "userID": None, "error": str(e)}
    finally:
        system.db.closeTransaction(tx)


def deshabilitar_usuario(username):
    """Soft-delete: marca Enabled=0. Conserva historial.
    
    Args:
        username (str): username a deshabilitar
    Returns:
        bool: True si se deshabilito, False si el usuario no existia
    """
    n = system.db.runPrepUpdate(
        "UPDATE dbo.users SET Enabled = 0 WHERE Username = ?",
        [username], DS
    )
    return n > 0


def habilitar_usuario(username):
    """Re-habilita un usuario previamente deshabilitado.
    
    Args:
        username (str): username a habilitar
    Returns:
        bool: True si se habilito, False si el usuario no existia
    """
    n = system.db.runPrepUpdate(
        "UPDATE dbo.users SET Enabled = 1 WHERE Username = ?",
        [username], DS
    )
    return n > 0


def cambiar_password(username, new_password):
    """Cambia la clave de un usuario.
    
    Args:
        username (str): username
        new_password (str): nueva clave en texto plano
    Returns:
        bool: True si se cambio, False si el usuario no existia
    """
    n = system.db.runPrepUpdate(
        "UPDATE dbo.users SET Password = ? WHERE Username = ?",
        [new_password, username], DS
    )
    return n > 0


def asignar_rol(username, role_name):
    """Asigna un rol adicional a un usuario existente.
    
    Args:
        username (str): username
        role_name (str): nombre del rol (ej: "Supervisor_PAPO")
    Returns:
        dict: {"success": bool, "error": str|None}
    """
    try:
        n = system.db.runPrepUpdate(
            """INSERT INTO dbo.user_roles (UserID, RoleID)
               SELECT u.ID, r.ID
               FROM dbo.users u, dbo.roles r
               WHERE u.Username = ? AND r.RoleName = ?
                 AND NOT EXISTS (
                     SELECT 1 FROM dbo.user_roles ur2
                     WHERE ur2.UserID = u.ID AND ur2.RoleID = r.ID
                 )""",
            [username, role_name], DS
        )
        if n == 0:
            return {"success": False, "error": "Usuario o rol no existe, o el usuario ya tiene ese rol"}
        return {"success": True, "error": None}
    except Exception as e:
        return {"success": False, "error": str(e)}


def quitar_rol(username, role_name):
    """Quita un rol de un usuario.
    
    Args:
        username (str): username
        role_name (str): nombre del rol a quitar
    Returns:
        bool: True si se quito, False si no tenia ese rol
    """
    n = system.db.runPrepUpdate(
        """DELETE FROM dbo.user_roles
           WHERE UserID = (SELECT ID FROM dbo.users WHERE Username = ?)
             AND RoleID = (SELECT ID FROM dbo.roles WHERE RoleName = ?)""",
        [username, role_name], DS
    )
    return n > 0


def obtener_usuario(username):
    """Obtiene la info completa de un usuario incluyendo sus roles.
    
    Args:
        username (str): username
    Returns:
        dict|None: {ID, Username, FirstName, LastName, Email, Enabled, Badge, Roles}
                   None si no existe
    """
    rows = system.db.runPrepQuery(
        """SELECT ID, Username, FirstName, LastName, Email, Enabled, Badge
           FROM dbo.users WHERE Username = ?""",
        [username], DS
    )
    if len(rows) == 0:
        return None
    user = {
        "ID": rows[0]["ID"],
        "Username": rows[0]["Username"],
        "FirstName": rows[0]["FirstName"],
        "LastName": rows[0]["LastName"],
        "Email": rows[0]["Email"],
        "Enabled": bool(rows[0]["Enabled"]),
        "Badge": rows[0]["Badge"],
        "Roles": []
    }
    role_rows = system.db.runPrepQuery(
        """SELECT r.RoleName
           FROM dbo.roles r
           INNER JOIN dbo.user_roles ur ON ur.RoleID = r.ID
           WHERE ur.UserID = ?""",
        [user["ID"]], DS
    )
    user["Roles"] = [r["RoleName"] for r in role_rows]
    return user


# =====================================================
# Ejemplos de uso:
# =====================================================
#
# # ----- Consultas -----
#
# # Dropdown de supervisores de un area
# supervisores = project.users.get_supervisors_by_area("ENSAMBLE")
# self.custom.supervisorOption = supervisores
#
# # Todos los operarios de OREC
# ops = project.users.get_users_by_roles(["Operator", "OREC"])
# for u in ops:
#     print(u["fullname"] + " (" + u["source"] + ")")
#
# # Cualquiera con rol MANTTO o EHS1
# tecnicos = project.users.get_users_by_roles(["MANTTO", "EHS1"], matchAll=False)
#
# # ----- CRUD -----
#
# # Crear usuario
# resultado = project.users.crear_usuario(
#     username="mlopezt",
#     password="7820",
#     firstname="Maria",
#     lastname="Lopez",
#     email="maria.lopez@clarios.com",
#     roles=["Operator", "OREC"]
# )
# if resultado["success"]:
#     print("Usuario creado con ID " + str(resultado["userID"]))
# else:
#     print("Error: " + resultado["error"])
#
# # Cambiar password
# project.users.cambiar_password("mlopezt", "9999")
#
# # Asignar/quitar roles
# project.users.asignar_rol("mlopezt", "Supervisor_PAPO")
# project.users.quitar_rol("mlopezt", "Supervisor_PAPO")
#
# # Habilitar / deshabilitar
# project.users.deshabilitar_usuario("mlopezt")
# project.users.habilitar_usuario("mlopezt")
#
# # Consultar
# u = project.users.obtener_usuario("barbolf")
# if u:
#     print(u["FirstName"] + " " + u["LastName"] + " - Roles: " + str(u["Roles"]))