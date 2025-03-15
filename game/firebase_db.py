import firebase_admin
from firebase_admin import credentials, db

FIREBASE_CREDENTIALS = {
    "type": "service_account",
    "project_id": "tetrisgame-64c45",
    "private_key_id": "994f3206664f7330c0f75c333074ff48d43f30d4",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQC0WmhnErerYGmR\nmEYFRk2bERJCWsIUXuu1RfHwRf9+Og2dfiZ14oWLil4Jqnp8fLF98aVsBfkuyHWn\nLg33D47Azkb7nInimdft28s1b8rrtAji5JjzJQMwobcUlK+nD8PNA5IevnnEy13S\npDsltoUKEpVxtU/L9Xk+sMzM18o6tenH1oOIaMlsFTj36oNdwE32KISHA9cikZQs\n6UuS+/X/Bh+9l2Er5oomKVxIoLSnin7CTS3gAZ9jAu5ULhh/gCDCdqgkrow9PRco\nkrLspkHBnTX1A/GPHWMjZU+FRM65Pd+vP/lIIJfInDIdpkxzyleeIOibsTocCgOe\nrwqyQ/OFAgMBAAECggEAAICa91e72r0AdkccDmvOD6J2/RsHHN4dBN3k9cdTVgNT\nFXv40lqKU2OHVDp2r/rIVmJr4UnmXvBW5/UOu8z98XQLPXkUmj5VXDFNsHOqanv1\n8i0MVWsMn/m0JDLI097znuvSYAY/gEiUiMYFb/S0i9z8fRSLj4G6yXp3fsX5tBTb\nh7ZDHyJa/6F2XUoLVxG1a+2o7HXaWQ0ObKwYImtEdWANfEwbYynNQ1mKSxPP1Wkl\nJGP2ziRsQCtDaV20HxI1xgcVRDOFalx8RVY0w31KJqlohkVbSG0iNVgOFySV6DlE\n4+gqlgM+SDjHCE0lskzaG+R8gPRuQ0imEYsE57h9cQKBgQD2MAbftmZAX+y1IhHM\n0VaRXkJHwkZiifMYWFAU9Vubom6SxQiKy0QDjRRMwJGSFKlkawxTJVKRUYYIYGPJ\nSbsvuWtP4W/9fHWSX1qhCCrQDn5f4Z1My/5JO+/QJC6mLvLdNvTuwDPIj9A+01bf\n7hCq/nLhLlhYBDF9u114jjAU9QKBgQC7iqPE68Z39UjYmwFpDKj+8WVJtkItR+ha\nIkM9VBH5rfup7fsM+IZxEdIJr+D7apdns3MQkh3H5E/64Fiqie/KfN6eMSviAeri\nFOiOSahVOtr7RHCYTiRPt0TtiYIRzxykZ85ht35zjomK/BZZ3+Yduz4gVNPqRs77\n1m8pv/TKUQKBgF6J/OnF8qg/7fd0+N7teM/kIZHK8hp/HSI5L6+MtTwj+VBVZ71c\n52Zxs9zxijVNx+rvDNGVIIr7gnwO/+LZdI+UJbiMOuRd+gxWn8f9CevR1Qfe7PgD\n0kevQ51rd5qLpun6Y76Xgos/ZtnpcJAXrMDta5I7qONL4PGGlRNpjt9NAoGAAMLd\nS01Rrub19rsaVFzSysYcDSKKPjjOfp8o+rS+pe7I2LW4kSLpGMhju9pU5XBXUPpv\nex+8szUABhqnAXox2PaMyMOWVAKB+4zuLLWr0zy76s0qT9PxXcl2pCgsuPnIOfqZ\n4dem0b1AXaoMRS0dd/1skSEHAypqaKdEKD05NyECgYEAi3jAlP4oY71T9e3NcRLB\naelI4QsR7Y3pkinCrEvKbSNl1MUfPvQSRuWlnAmhQn09DXBhBxlF3H7CRAETCN3G\nbDIfxAOPTlrJ8FDATFHfxicnCSnr/D+7Pg85YXUsZ8dTDW2EcFxlCe0vyQDaOF9T\nEnQ1yuXI41z0cVS8KX3Dyuw=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-blqi9@tetrisgame-64c45.iam.gserviceaccount.com",
    "client_id": "107199534857823320207",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-blqi9%40tetrisgame-64c45.iam.gserviceaccount.com",
    "universe_domain": "googleapis.com"}

class FirebaseTetrisDB:
    def __init__(self):
        try:
            # Inicialización de Firebase
            cred = credentials.Certificate(FIREBASE_CREDENTIALS)
            firebase_admin.initialize_app(cred, {
                'databaseURL': 'https://tetrisgame-64c45-default-rtdb.firebaseio.com/'
            })
            self.db_ref = db.reference('users')  # Nodo de usuarios
            print("Firebase Realtime Database initialized successfully!")
        except Exception as e:
            raise RuntimeError(f"Error initializing Firebase: {str(e)}")

    def create_user(self, username):
        """Crea un usuario nuevo con un nombre único, y puntaje inicial."""

        # Verificar si el usuario ya existe
        if self.db_ref.child(username).get() is not None:
            return f"El nombre de usuario '{username}' ya está en uso. Intenta con otro."

        # Crear usuario
        self.db_ref.child(username).set({
            'username': username,
            'high_score': 0
        })
        return f"Usuario '{username}' creado exitosamente."

    def login(self, username, password):
        user = self.db_ref.child(username).get()
        if user is None:
            return "Usuario no encontrado."

        return f"Inicio de sesión exitoso. ¡Bienvenido {username}!"

    def update_high_record(self, username, new_score):
        user = self.db_ref.child(username).get()

        current_high_record = user['high_score']
        if new_score > current_high_record:
            self.db_ref.child(username).update({'high_score': new_score})

    def update_leaderboard(self):
        users = self.db_ref.get()

        leaderboard = []
        for username, user_data in users.items():
            score = user_data['high_score']
            leaderboard.append({'name': username, 'high_score': score})

        leaderboard_sorted = sorted(leaderboard, key=lambda x: x['high_score'], reverse=True)

        top_5 = leaderboard_sorted[:5]

        leaderboard_dict = {}

        for entry in top_5:
            name = entry['name']
            high_score = entry['high_score']
            leaderboard_dict[name] = high_score

        return leaderboard_dict

