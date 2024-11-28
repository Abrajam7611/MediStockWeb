from django.shortcuts import render, redirect
from django.contrib import messages
from firebase_admin import firestore, initialize_app, credentials
import firebase_admin

# Inicializa la aplicación Firebase si aún no está inicializada.
cred = credentials.Certificate('Clave.json')
if not firebase_admin._apps:
    initialize_app(cred)

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Accede a Firestore para verificar las credenciales.
        db = firestore.client()
        users_ref = db.collection('usuarios')
        user_doc = users_ref.where('email', '==', email).stream()

        user_found = False
        for doc in user_doc:
            user_data = doc.to_dict()
            # Verifica que la contraseña coincida (ajusta esto según tu implementación de hash).
            if user_data.get('password') == password:
                user_found = True
                break

        if user_found:
            messages.success(request, 'Inicio de sesión exitoso.')
            return redirect('inicio')
        else:
            messages.error(request, 'Error de autenticación: Verifica tus credenciales.')

    return render(request, 'login.html')
