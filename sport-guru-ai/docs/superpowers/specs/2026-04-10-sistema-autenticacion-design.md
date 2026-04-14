# Especificación: Sistema de Autenticación SportGuru AI

**Fecha:** 2026-04-10  
**Estado:** Aprobado  
**Enfoque seleccionado:** Supabase Auth (Opción B: Google + Email/Password)

---

## 1. Resumen Ejecutivo

Implementar un sistema de autenticación funcional basado en Supabase Auth que permita a los usuarios registrarse e iniciar sesión mediante Google OAuth o Email/Password. El sistema debe capturar el número de teléfono para el CRM y proteger el acceso a picks premium.

---

## 2. Requisitos Funcionales

### RF-001: Métodos de Autenticación
- El sistema debe soportar login mediante Google OAuth
- El sistema debe soportar registro/login mediante Email y Password
- Las contraseñas deben tener mínimo 8 caracteres

### RF-002: Flujo de Captura de Teléfono (CRM)
- Después del primer login exitoso, se debe solicitar el número de teléfono
- El teléfono debe guardarse en la tabla `profiles`
- Este paso es obligatorio para completar el registro

### RF-003: Gestión de Sesión
- La sesión debe persistir mediante cookies HTTP-only
- El token debe renovarse automáticamente
- El usuario debe poder cerrar sesión

### RF-004: Protección de Contenido
- Los picks premium deben estar protegidos
- Usuarios no autenticados deben ver el modal de login al intentar acceder
- Los picks gratuitos son visibles sin autenticación

---

## 3. Arquitectura Técnica

### 3.1 Componentes del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                     CLIENTE (Browser)                        │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐        │
│  │  AuthModal   │  │AuthContext   │  │  Middleware  │        │
│  │   (UI)       │  │  (Estado)    │  │ (Protección) │        │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘        │
└─────────┼────────────────┼────────────────┼──────────────────┘
          │                │                │
          └────────────────┼────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│                    SUPABASE AUTH                             │
│  ┌──────────────────────────────────────────────┐             │
│  │  • OAuth Providers (Google)                  │             │
│  │  • Email/Password Auth                       │             │
│  │  • Session Management (JWT)                  │             │
│  └──────────────────────┬───────────────────────┘             │
│                         │                                    │
│  ┌──────────────────────▼───────────────────────┐             │
│  │           POSTGRESQL DATABASE                  │             │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐   │             │
│  │  │  users   │  │ profiles │  │  picks   │   │             │
│  │  │  (auth)  │  │(public)  │  │(public)  │   │             │
│  │  └──────────┘  └──────────┘  └──────────┘   │             │
│  └──────────────────────────────────────────────┘             │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 Estructura de Archivos

```
src/
├── lib/
│   ├── supabase/
│   │   ├── client.ts          # Cliente Supabase para Browser
│   │   ├── server.ts          # Cliente Supabase para Server
│   │   └── middleware.ts      # Helper de middleware
│   └── auth/
│       └── callback/
│           └── route.ts       # Endpoint OAuth callback
├── components/
│   ├── AuthModal.tsx          # Modal con lógica de auth
│   ├── AuthContext.tsx        # Proveedor de contexto
│   └── LoginButton.tsx        # Botón reutilizable
├── app/
│   ├── auth/
│   │   └── callback/
│   │       └── page.tsx       # Página de callback
│   └── api/
│       └── auth/
│           └── phone/
│               └── route.ts   # Guardar teléfono
└── middleware.ts              # Middleware de Next.js
```

---

## 4. Diseño de Datos

### 4.1 Tablas Existentes (ya en supabase_schema.sql)

```sql
-- Tabla auth.users (gestionada por Supabase)
-- Tabla profiles (extensión de usuarios)
CREATE TABLE profiles (
    id UUID REFERENCES auth.users NOT NULL PRIMARY KEY,
    phone_number TEXT,
    email TEXT,
    full_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger para crear perfil automáticamente
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, email, full_name)
  VALUES (
    new.id, 
    new.email, 
    new.raw_user_meta_data->>'full_name'
  );
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### 4.2 Modificaciones Necesarias

- Añadir columna `phone_verified` boolean a profiles
- Crear índice en `phone_number` para búsquedas CRM

---

## 5. Flujo de Usuario

### 5.1 Registro con Google OAuth

```
┌──────────┐     ┌──────────────┐     ┌────────────────┐
│  Usuario │────▶│ Click "Google" │────▶│ Supabase OAuth │
└──────────┘     └──────────────┘     └───────┬────────┘
                                               │
┌──────────┐     ┌──────────────┐     ┌──────▼────────┐
│ Dashboard│◀────│   Callback    │◀────│  Google Auth  │
│ (logueado)    │   (guarda     │      │               │
│               │    sesión)     │      │               │
└──────────┘    └──────────────┘      └───────────────┘
                         │
                         ▼
              ┌────────────────────┐
              │  ¿Teléfono existe? │
              └────────┬───────────┘
                       │
              ┌────────┴────────┐
              ▼                 ▼
       ┌──────────────┐  ┌─────────────┐
       │   Mostrar    │  │    Ir a     │
       │ Modal Teléf  │  │  Dashboard  │
       └──────────────┘  └─────────────┘
```

### 5.2 Registro con Email/Password

```
┌──────────┐     ┌──────────────┐     ┌────────────────┐
│  Usuario │────▶│ Ingresa Email │────▶│ Supabase Auth  │
│          │     │   + Password  │      │                │
└──────────┘     └──────────────┘     └───────┬────────┘
                                               │
                                       ┌───────▼────────┐
                                       │ Email de       │
                                       │ Confirmación   │
                                       └───────┬────────┘
                                               │
┌──────────┐     ┌──────────────┐     ┌──────▼────────┐
│ Dashboard│◀────│   Confirmar   │◀────│  Click en     │
│(logueado)│     │   Callback    │     │  email         │
│          │     │  + Pedir Tel  │     │                │
└──────────┘     └──────────────┘     └───────────────┘
```

---

## 6. API y Endpoints

### 6.1 Endpoints de Supabase (automáticos)

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/auth/v1/signup` | POST | Registro email/password |
| `/auth/v1/token` | POST | Login email/password |
| `/auth/v1/authorize` | GET | Iniciar OAuth Google |
| `/auth/v1/callback` | GET | Callback OAuth |
| `/auth/v1/logout` | POST | Cerrar sesión |

### 6.2 Endpoints Personalizados

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/api/auth/phone` | POST | Guardar número de teléfono |
| `/api/auth/check` | GET | Verificar sesión activa |

---

## 7. UI/UX

### 7.1 Estados del AuthModal

1. **Login Principal**: Botones Google, Email, Teléfono
2. **Registro Email**: Formulario email + password + confirmar
3. **Login Email**: Formulario email + password
4. **Captura Teléfono**: Input teléfono (después de auth exitoso)

### 7.2 Estados de Carga y Error

- Loading spinner durante OAuth
- Mensajes de error claros (credenciales inválidas, email existente)
- Validación de email en tiempo real
- Validación de teléfono (mínimo 10 dígitos)

---

## 8. Seguridad

### 8.1 Medidas Implementadas

- Cookies HTTP-only para tokens
- CSRF protection (incluido en Supabase)
- Row Level Security (RLS) en tablas sensibles
- Rate limiting en intentos de login
- Validación de dominios en OAuth

### 8.2 Configuración de CORS

- Permitir solo origen de producción
- localhost:3000 para desarrollo

---

## 9. Dependencias

```json
{
  "dependencies": {
    "@supabase/supabase-js": "^2.49.4",
    "@supabase/auth-helpers-nextjs": "^0.10.0"
  }
}
```

---

## 10. Variables de Entorno

```bash
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=eyJ...
SUPABASE_SERVICE_ROLE_KEY=eyJ...

# OAuth Google (Opcional - solo para producción)
GOOGLE_CLIENT_ID=xxx
GOOGLE_CLIENT_SECRET=xxx
```

---

## 11. Criterios de Aceptación

- [ ] Usuario puede registrarse con Google OAuth
- [ ] Usuario puede registrarse con Email/Password
- [ ] Usuario puede iniciar sesión con ambos métodos
- [ ] Sistema solicita teléfono después del primer login
- [ ] Teléfono se guarda en tabla profiles
- [ ] Picks premium están protegidos (requieren auth)
- [ ] Usuario puede cerrar sesión
- [ ] Sesión persiste después de recargar página
- [ ] Middleware protege rutas /premium/*

---

## 12. Notas de Implementación

1. El flujo de teléfono debe ser obligatorio pero no bloquear la sesión
2. Usar `createClientComponentClient` para componentes cliente
3. Usar `createServerComponentClient` para Server Components
4. Implementar `middleware.ts` para proteger rutas dinámicamente
5. Mantener compatibilidad con el esquema SQL existente

---

**Aprobado por:** Usuario  
**Fecha de aprobación:** 2026-04-10
