# Implementación: Sistema de Autenticación Supabase

> **Para agentes:** Usar superpowers:subagent-driven-development o superpowers:executing-plans. Los pasos usan checkbox (`- [ ]`) para tracking.

**Objetivo:** Implementar autenticación funcional con Google OAuth y Email/Password usando Supabase Auth, con captura de teléfono para CRM y protección de picks premium.

**Arquitectura:** Usar Supabase Auth para gestión de sesiones, cookies HTTP-only para persistencia, React Context para estado global, y middleware de Next.js para protección de rutas. El flujo incluye detección de usuarios nuevos para solicitar teléfono antes de completar el acceso.

**Stack:** Next.js 16 + React 19 + TypeScript + Supabase + Tailwind CSS

---

## Fase 0: Setup Inicial

### Task 0.1: Instalar dependencias de Supabase

**Archivos:**
- Modificar: `package.json`

- [ ] **Paso 1: Instalar paquetes de Supabase**

```bash
cd sport-guru-ai
npm install @supabase/supabase-js @supabase/auth-helpers-nextjs
npm install @supabase/auth-helpers-react
```

- [ ] **Paso 2: Verificar instalación**

```bash
cat package.json | grep -A 5 '"dependencies"'
```

**Esperado:** Debe mostrar `@supabase/supabase-js` y `@supabase/auth-helpers-nextjs` en la lista.

- [ ] **Paso 3: Commit**

```bash
git add package.json package-lock.json
git commit -m "deps: instalar Supabase Auth helpers"
```

---

### Task 0.2: Configurar variables de entorno

**Archivos:**
- Crear: `.env.local`
- Modificar: `.gitignore` (si es necesario)

- [ ] **Paso 1: Crear archivo de variables de entorno**

```bash
touch .env.local
```

- [ ] **Paso 2: Agregar template de variables**

```bash
cat > .env.local << 'EOF'
# Supabase Configuration
NEXT_PUBLIC_SUPABASE_URL=tu_proyecto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu_anon_key_aqui
SUPABASE_SERVICE_ROLE_KEY=tu_service_role_key_aqui

# OAuth Google (opcional - para producción)
NEXT_PUBLIC_GOOGLE_CLIENT_ID=
GOOGLE_CLIENT_SECRET=
EOF
```

- [ ] **Paso 3: Verificar que .gitignore excluye .env.local**

```bash
grep -E "^\.env\." .gitignore || echo ".env.local" >> .gitignore
```

- [ ] **Paso 4: Commit**

```bash
git add .env.local .gitignore
git commit -m "config: agregar template de variables de entorno para Supabase"
```

---

## Fase 1: Configuración de Supabase

### Task 1.1: Crear cliente Supabase para Browser

**Archivos:**
- Crear: `src/lib/supabase/client.ts`

- [ ] **Paso 1: Crear directorio**

```bash
mkdir -p src/lib/supabase
```

- [ ] **Paso 2: Escribir el archivo del cliente**

```typescript
// src/lib/supabase/client.ts
import { createBrowserClient } from '@supabase/auth-helpers-nextjs'

// Cliente de Supabase para componentes del browser
export const supabaseClient = createBrowserClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
)

// Helper para obtener el cliente en componentes cliente
export function getSupabaseClient() {
  return supabaseClient
}
```

- [ ] **Paso 3: Commit**

```bash
git add src/lib/supabase/client.ts
git commit -m "feat(supabase): crear cliente para browser"
```

---

### Task 1.2: Crear cliente Supabase para Server

**Archivos:**
- Crear: `src/lib/supabase/server.ts`

- [ ] **Paso 1: Escribir el archivo del servidor**

```typescript
// src/lib/supabase/server.ts
import { createServerClient } from '@supabase/auth-helpers-nextjs'
import { cookies } from 'next/headers'
import { NextRequest, NextResponse } from 'next/server'

// Cliente de Supabase para Server Components
export function createClient() {
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return cookies().get(name)?.value
        },
        set(name: string, value: string, options: any) {
          cookies().set(name, value, options)
        },
        remove(name: string, options: any) {
          cookies().set(name, '', { ...options, maxAge: 0 })
        },
      },
    }
  )
}

// Helper para middleware
export async function updateSession(request: NextRequest) {
  const response = NextResponse.next()
  
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: any) {
          response.cookies.set(name, value, options)
        },
        remove(name: string, options: any) {
          response.cookies.set(name, '', { ...options, maxAge: 0 })
        },
      },
    }
  )

  // Refrescar sesión si existe
  await supabase.auth.getSession()
  
  return response
}

// Verificar si hay sesión activa
export async function getSession() {
  const supabase = createClient()
  const { data: { session } } = await supabase.auth.getSession()
  return session
}

// Verificar si el usuario está autenticado
export async function getUser() {
  const supabase = createClient()
  const { data: { user } } = await supabase.auth.getUser()
  return user
}
```

- [ ] **Paso 2: Commit**

```bash
git add src/lib/supabase/server.ts
git commit -m "feat(supabase): crear cliente para server y helpers de auth"
```

---

### Task 1.3: Crear Middleware de Autenticación

**Archivos:**
- Crear: `src/middleware.ts`

- [ ] **Paso 1: Crear middleware de Next.js**

```typescript
// src/middleware.ts
import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { updateSession } from './lib/supabase/server'

// Rutas que requieren autenticación
const PROTECTED_ROUTES = ['/premium', '/checkout', '/profile']

export async function middleware(request: NextRequest) {
  // Actualizar sesión en cookies
  const response = await updateSession(request)
  
  const { pathname } = request.nextUrl
  
  // Verificar si la ruta está protegida
  const isProtected = PROTECTED_ROUTES.some(route => 
    pathname.startsWith(route)
  )
  
  if (isProtected) {
    // Obtener sesión de cookies
    const supabaseSession = request.cookies.get('sb-access-token')
    
    if (!supabaseSession) {
      // Redirigir al login con return URL
      const loginUrl = new URL('/', request.url)
      loginUrl.searchParams.set('auth', 'required')
      loginUrl.searchParams.set('returnTo', pathname)
      return NextResponse.redirect(loginUrl)
    }
  }
  
  return response
}

// Configurar matcher para rutas
export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
```

- [ ] **Paso 2: Commit**

```bash
git add src/middleware.ts
git commit -m "feat(auth): implementar middleware de protección de rutas"
```

---

## Fase 2: Contexto de Autenticación

### Task 2.1: Crear AuthContext

**Archivos:**
- Crear: `src/components/AuthContext.tsx`

- [ ] **Paso 1: Crear el contexto de autenticación**

```typescript
// src/components/AuthContext.tsx
'use client'

import React, { createContext, useContext, useEffect, useState } from 'react'
import { Session, User } from '@supabase/supabase-js'
import { supabaseClient } from '../lib/supabase/client'

interface AuthContextType {
  user: User | null
  session: Session | null
  isLoading: boolean
  signInWithGoogle: () => Promise<void>
  signInWithEmail: (email: string, password: string) => Promise<void>
  signUpWithEmail: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
  needsPhone: boolean
  setNeedsPhone: (value: boolean) => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<Session | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [needsPhone, setNeedsPhone] = useState(false)

  useEffect(() => {
    // Obtener sesión inicial
    supabaseClient.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setUser(session?.user ?? null)
      setIsLoading(false)
    })

    // Escuchar cambios de auth
    const { data: { subscription } } = supabaseClient.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session)
        setUser(session?.user ?? null)
      }
    )

    return () => subscription.unsubscribe()
  }, [])

  const signInWithGoogle = async () => {
    const { error } = await supabaseClient.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    })
    if (error) throw error
  }

  const signInWithEmail = async (email: string, password: string) => {
    const { error } = await supabaseClient.auth.signInWithPassword({
      email,
      password,
    })
    if (error) throw error
  }

  const signUpWithEmail = async (email: string, password: string) => {
    const { error } = await supabaseClient.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      },
    })
    if (error) throw error
  }

  const signOut = async () => {
    const { error } = await supabaseClient.auth.signOut()
    if (error) throw error
    setNeedsPhone(false)
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        session,
        isLoading,
        signInWithGoogle,
        signInWithEmail,
        signUpWithEmail,
        signOut,
        needsPhone,
        setNeedsPhone,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
```

- [ ] **Paso 2: Commit**

```bash
git add src/components/AuthContext.tsx
git commit -m "feat(auth): crear contexto de autenticación con Supabase"
```

---

### Task 2.2: Integrar AuthProvider en Layout

**Archivos:**
- Modificar: `src/app/layout.tsx`

- [ ] **Paso 1: Actualizar el layout raíz**

```typescript
// src/app/layout.tsx
import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "../components/AuthContext";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "SportGuru AI - Predicciones Deportivas",
  description: "Predicciones deportivas basadas en IA y análisis de datos",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="es"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
```

- [ ] **Paso 2: Commit**

```bash
git add src/app/layout.tsx
git commit -m "feat(auth): integrar AuthProvider en layout raíz"
```

---

## Fase 3: Página de Callback OAuth

### Task 3.1: Crear ruta de callback

**Archivos:**
- Crear: `src/app/auth/callback/page.tsx`
- Crear: `src/app/auth/callback/route.ts`

- [ ] **Paso 1: Crear estructura de directorios**

```bash
mkdir -p src/app/auth/callback
```

- [ ] **Paso 2: Crear el componente de callback**

```typescript
// src/app/auth/callback/page.tsx
'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuth } from '../../../components/AuthContext'

export default function AuthCallback() {
  const router = useRouter()
  const { user, isLoading } = useAuth()

  useEffect(() => {
    if (!isLoading) {
      if (user) {
        // Verificar si necesita teléfono
        checkUserProfile(user.id)
      } else {
        // Error en autenticación
        router.push('/?auth=error')
      }
    }
  }, [user, isLoading, router])

  const checkUserProfile = async (userId: string) => {
    try {
      const response = await fetch('/api/user/profile')
      const data = await response.json()
      
      if (data.phone_number) {
        // Tiene teléfono, ir al dashboard
        router.push('/')
      } else {
        // Necesita agregar teléfono
        router.push('/?auth=phone_required')
      }
    } catch (error) {
      router.push('/?auth=error')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-[#0A0A0B]">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#D4AF37] mx-auto mb-4"></div>
        <p className="text-gray-400">Verificando sesión...</p>
      </div>
    </div>
  )
}
```

- [ ] **Paso 3: Commit**

```bash
git add src/app/auth/callback/
git commit -m "feat(auth): crear página de callback OAuth"
```

---

## Fase 4: API Routes

### Task 4.1: Crear API para obtener perfil

**Archivos:**
- Crear: `src/app/api/user/profile/route.ts`

- [ ] **Paso 1: Crear directorios**

```bash
mkdir -p src/app/api/user/profile
```

- [ ] **Paso 2: Crear endpoint GET**

```typescript
// src/app/api/user/profile/route.ts
import { NextResponse } from 'next/server'
import { createClient } from '../../../../lib/supabase/server'

export async function GET() {
  try {
    const supabase = createClient()
    
    // Verificar sesión
    const { data: { user }, error: authError } = await supabase.auth.getUser()
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'No autenticado' },
        { status: 401 }
      )
    }
    
    // Obtener perfil
    const { data: profile, error: profileError } = await supabase
      .from('profiles')
      .select('*')
      .eq('id', user.id)
      .single()
    
    if (profileError) {
      return NextResponse.json(
        { error: 'Perfil no encontrado' },
        { status: 404 }
      )
    }
    
    return NextResponse.json(profile)
  } catch (error) {
    return NextResponse.json(
      { error: 'Error interno del servidor' },
      { status: 500 }
    )
  }
}
```

- [ ] **Paso 3: Commit**

```bash
git add src/app/api/user/profile/
git commit -m "feat(api): crear endpoint para obtener perfil de usuario"
```

---

### Task 4.2: Crear API para guardar teléfono

**Archivos:**
- Crear: `src/app/api/user/phone/route.ts`

- [ ] **Paso 1: Crear directorios**

```bash
mkdir -p src/app/api/user/phone
```

- [ ] **Paso 2: Crear endpoint POST**

```typescript
// src/app/api/user/phone/route.ts
import { NextResponse } from 'next/server'
import { createClient } from '../../../../lib/supabase/server'

export async function POST(request: Request) {
  try {
    const { phone } = await request.json()
    
    // Validar teléfono
    if (!phone || phone.length < 10) {
      return NextResponse.json(
        { error: 'Teléfono inválido' },
        { status: 400 }
      )
    }
    
    const supabase = createClient()
    
    // Verificar sesión
    const { data: { user }, error: authError } = await supabase.auth.getUser()
    
    if (authError || !user) {
      return NextResponse.json(
        { error: 'No autenticado' },
        { status: 401 }
      )
    }
    
    // Actualizar perfil con teléfono
    const { data, error } = await supabase
      .from('profiles')
      .update({ 
        phone_number: phone,
        updated_at: new Date().toISOString()
      })
      .eq('id', user.id)
      .select()
      .single()
    
    if (error) {
      return NextResponse.json(
        { error: 'Error al guardar teléfono' },
        { status: 500 }
      )
    }
    
    return NextResponse.json({ 
      success: true, 
      profile: data 
    })
  } catch (error) {
    return NextResponse.json(
      { error: 'Error interno del servidor' },
      { status: 500 }
    )
  }
}
```

- [ ] **Paso 3: Commit**

```bash
git add src/app/api/user/phone/
git commit -m "feat(api): crear endpoint para guardar teléfono del usuario"
```

---

## Fase 5: Componente AuthModal Mejorado

### Task 5.1: Actualizar AuthModal con lógica real

**Archivos:**
- Modificar: `src/components/AuthModal.tsx`

- [ ] **Paso 1: Reemplazar AuthModal completo**

```typescript
// src/components/AuthModal.tsx
"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Lock, Smartphone, Mail, AlertCircle, X, Eye, EyeOff, Loader2 } from "lucide-react";
import { useAuth } from "./AuthContext";

type AuthStep = "login" | "phone_capture" | "email_login" | "email_register" | "success";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const [step, setStep] = useState<AuthStep>("login");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  
  const { 
    signInWithGoogle, 
    signInWithEmail, 
    signUpWithEmail, 
    user,
    setNeedsPhone 
  } = useAuth();

  const resetForm = () => {
    setPhoneNumber("");
    setEmail("");
    setPassword("");
    setConfirmPassword("");
    setError("");
    setSuccessMessage("");
    setShowPassword(false);
    setStep("login");
  };

  const handleClose = () => {
    resetForm();
    onClose();
  };

  // Login con Google
  const handleGoogleLogin = async () => {
    setIsLoading(true);
    setError("");
    
    try {
      await signInWithGoogle();
      // El redireccionamiento lo maneja Supabase OAuth
    } catch (err: any) {
      setError(err.message || "Error al iniciar sesión con Google");
      setIsLoading(false);
    }
  };

  // Login con Email
  const handleEmailLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    if (!email || !password) {
      setError("Por favor completa todos los campos");
      setIsLoading(false);
      return;
    }

    try {
      await signInWithEmail(email, password);
      // Después de login exitoso, verificar si necesita teléfono
      await checkPhoneRequirement();
    } catch (err: any) {
      setError(err.message || "Credenciales incorrectas");
      setIsLoading(false);
    }
  };

  // Registro con Email
  const handleEmailRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    if (!email || !password || !confirmPassword) {
      setError("Por favor completa todos los campos");
      setIsLoading(false);
      return;
    }

    if (password.length < 8) {
      setError("La contraseña debe tener al menos 8 caracteres");
      setIsLoading(false);
      return;
    }

    if (password !== confirmPassword) {
      setError("Las contraseñas no coinciden");
      setIsLoading(false);
      return;
    }

    try {
      await signUpWithEmail(email, password);
      setSuccessMessage("¡Registro exitoso! Revisa tu email para confirmar.");
      setIsLoading(false);
      setTimeout(() => {
        setStep("email_login");
        setSuccessMessage("");
      }, 3000);
    } catch (err: any) {
      setError(err.message || "Error al registrarse");
      setIsLoading(false);
    }
  };

  // Guardar teléfono
  const handleSubmitPhone = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError("");

    if (phoneNumber.length < 10) {
      setError("Por favor ingresa un número de teléfono válido");
      setIsLoading(false);
      return;
    }

    try {
      const response = await fetch('/api/user/phone', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone: phoneNumber }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Error al guardar teléfono");
      }

      setSuccessMessage("¡Teléfono verificado! Prospecto guardado en CRM.");
      setNeedsPhone(false);
      setIsLoading(false);
      
      setTimeout(() => {
        handleClose();
      }, 2000);
    } catch (err: any) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  // Verificar si el usuario necesita agregar teléfono
  const checkPhoneRequirement = async () => {
    try {
      const response = await fetch('/api/user/profile');
      const data = await response.json();
      
      if (data.phone_number) {
        // Tiene teléfono, cerrar modal
        handleClose();
      } else {
        // Necesita agregar teléfono
        setStep("phone_capture");
        setNeedsPhone(true);
        setIsLoading(false);
      }
    } catch (err) {
      setError("Error al verificar perfil");
      setIsLoading(false);
    }
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={handleClose}
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
          />

          {/* Modal Content */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="relative w-full max-w-md bg-[#121214] border border-white/10 rounded-2xl shadow-2xl p-6 overflow-hidden"
          >
            {/* Adorno superior dorado */}
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-[#D4AF37] to-transparent opacity-50" />
            
            <button
              onClick={handleClose}
              className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
            >
              <X size={20} />
            </button>

            {/* Mensajes de error */}
            {error && (
              <div className="mb-4 p-3 bg-red-500/10 border border-red-500/30 rounded-lg flex items-center gap-2">
                <AlertCircle size={16} className="text-red-400 flex-shrink-0" />
                <p className="text-sm text-red-400">{error}</p>
              </div>
            )}

            {/* Mensajes de éxito */}
            {successMessage && (
              <div className="mb-4 p-3 bg-green-500/10 border border-green-500/30 rounded-lg flex items-center gap-2">
                <CheckCircle2 size={16} className="text-green-400 flex-shrink-0" />
                <p className="text-sm text-green-400">{successMessage}</p>
              </div>
            )}

            {/* PASO 1: Login Principal */}
            {step === "login" && (
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 bg-[#D4AF37]/10 rounded-full flex items-center justify-center mb-4 text-[#D4AF37]">
                  <Lock size={24} />
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">Desbloquea el Pick</h3>
                <p className="text-sm text-gray-400 text-center mb-8">
                  Regístrate gratis para ver el análisis completo o comprar picks premium.
                </p>

                <div className="w-full space-y-3">
                  {/* Google Login */}
                  <button 
                    onClick={handleGoogleLogin}
                    disabled={isLoading}
                    className="w-full py-3 px-4 bg-white hover:bg-gray-100 text-black rounded-lg font-semibold flex items-center justify-center gap-3 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading ? (
                      <Loader2 className="w-5 h-5 animate-spin" />
                    ) : (
                      <svg className="w-5 h-5" viewBox="0 0 24 24">
                        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.07v2.84C3.89 20.5 7.67 23 12 23z" fill="#34A853"/>
                        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.07C1.34 8.52.95 10.2.95 12s.39 3.48 1.12 4.93l3.77-2.84z" fill="#FBBC05"/>
                        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.67 1 3.89 3.5 2.07 7.07l3.77 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                      </svg>
                    )}
                    {isLoading ? 'Conectando...' : 'Continuar con Google'}
                  </button>
                  
                  {/* Email Login */}
                  <button 
                    onClick={() => setStep("email_login")}
                    className="w-full py-3 px-4 bg-[#1A1A1C] border border-white/5 hover:bg-white/5 text-white rounded-lg font-semibold flex items-center justify-center gap-3 transition-colors"
                  >
                    <Mail size={20} />
                    Continuar con Email
                  </button>

                  {/* Divider */}
                  <div className="relative py-2">
                    <div className="absolute inset-0 flex items-center">
                      <div className="w-full border-t border-white/10"></div>
                    </div>
                    <div className="relative flex justify-center text-xs">
                      <span className="px-2 bg-[#121214] text-gray-500">¿No tienes cuenta?</span>
                    </div>
                  </div>

                  {/* Register Link */}
                  <button 
                    onClick={() => setStep("email_register")}
                    className="w-full py-3 px-4 border border-[#D4AF37]/30 text-[#D4AF37] hover:bg-[#D4AF37]/10 rounded-lg font-semibold transition-colors"
                  >
                    Crear Cuenta Nueva
                  </button>
                </div>
              </div>
            )}

            {/* PASO 2: Email Login Form */}
            {step === "email_login" && (
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex flex-col"
              >
                <button 
                  onClick={() => setStep("login")}
                  className="text-left text-sm text-gray-400 hover:text-white mb-4 flex items-center gap-1"
                >
                  ← Volver
                </button>

                <div className="w-12 h-12 bg-[#D4AF37]/10 rounded-full flex items-center justify-center mb-4 text-[#D4AF37] mx-auto">
                  <Mail size={24} />
                </div>
                <h3 className="text-2xl font-bold text-white mb-2 text-center">Iniciar Sesión</h3>
                <p className="text-sm text-gray-400 text-center mb-6">
                  Ingresa tus credenciales para acceder.
                </p>

                <form onSubmit={handleEmailLogin} className="w-full space-y-4">
                  <div>
                    <label className="block text-xs text-gray-400 font-medium mb-1 uppercase tracking-wider">Email</label>
                    <input 
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="tu@email.com"
                      className="w-full bg-black border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-[#D4AF37] transition-colors"
                      required
                      disabled={isLoading}
                    />
                  </div>

                  <div>
                    <label className="block text-xs text-gray-400 font-medium mb-1 uppercase tracking-wider">Contraseña</label>
                    <div className="relative">
                      <input 
                        type={showPassword ? "text" : "password"}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="••••••••"
                        className="w-full bg-black border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-[#D4AF37] transition-colors pr-12"
                        required
                        disabled={isLoading}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                      >
                        {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                      </button>
                    </div>
                  </div>

                  <button 
                    type="submit"
                    disabled={isLoading}
                    className="w-full py-3 rounded-xl bg-[#D4AF37] text-black font-bold flex items-center justify-center gap-2 hover:bg-[#F3CE5E] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 size={18} className="animate-spin" />
                        Ingresando...
                      </>
                    ) : (
                      'Iniciar Sesión'
                    )}
                  </button>
                </form>
              </motion.div>
            )}

            {/* PASO 3: Email Register Form */}
            {step === "email_register" && (
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex flex-col"
              >
                <button 
                  onClick={() => setStep("login")}
                  className="text-left text-sm text-gray-400 hover:text-white mb-4 flex items-center gap-1"
                >
                  ← Volver
                </button>

                <div className="w-12 h-12 bg-[#22C55E]/10 rounded-full flex items-center justify-center mb-4 text-[#22C55E] mx-auto">
                  <Smartphone size={24} />
                </div>
                <h3 className="text-2xl font-bold text-white mb-2 text-center">Crear Cuenta</h3>
                <p className="text-sm text-gray-400 text-center mb-6">
                  Regístrate para desbloquear picks premium.
                </p>

                <form onSubmit={handleEmailRegister} className="w-full space-y-4">
                  <div>
                    <label className="block text-xs text-gray-400 font-medium mb-1 uppercase tracking-wider">Email</label>
                    <input 
                      type="email"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="tu@email.com"
                      className="w-full bg-black border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-[#D4AF37] transition-colors"
                      required
                      disabled={isLoading}
                    />
                  </div>

                  <div>
                    <label className="block text-xs text-gray-400 font-medium mb-1 uppercase tracking-wider">Contraseña</label>
                    <div className="relative">
                      <input 
                        type={showPassword ? "text" : "password"}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Mínimo 8 caracteres"
                        className="w-full bg-black border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-[#D4AF37] transition-colors pr-12"
                        required
                        minLength={8}
                        disabled={isLoading}
                      />
                      <button
                        type="button"
                        onClick={() => setShowPassword(!showPassword)}
                        className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-400 hover:text-white"
                      >
                        {showPassword ? <EyeOff size={18} /> : <Eye size={18} />}
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-xs text-gray-400 font-medium mb-1 uppercase tracking-wider">Confirmar Contraseña</label>
                    <input 
                      type="password"
                      value={confirmPassword}
                      onChange={(e) => setConfirmPassword(e.target.value)}
                      placeholder="Repite tu contraseña"
                      className="w-full bg-black border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-[#D4AF37] transition-colors"
                      required
                      disabled={isLoading}
                    />
                  </div>

                  <button 
                    type="submit"
                    disabled={isLoading}
                    className="w-full py-3 rounded-xl bg-[#22C55E] text-black font-bold flex items-center justify-center gap-2 hover:bg-[#4ade80] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 size={18} className="animate-spin" />
                        Creando cuenta...
                      </>
                    ) : (
                      'Crear Cuenta'
                    )}
                  </button>
                </form>
              </motion.div>
            )}

            {/* PASO 4: Captura de Teléfono */}
            {step === "phone_capture" && (
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex flex-col items-center"
              >
                <div className="w-12 h-12 bg-[#22C55E]/10 rounded-full flex items-center justify-center mb-4 text-[#22C55E]">
                  <Smartphone size={24} />
                </div>
                <h3 className="text-2xl font-bold text-white mb-2 text-center">Falta un último paso</h3>
                <p className="text-sm text-gray-400 text-center mb-6">
                  Para fines de seguridad y seguimiento en alertas en vivo, necesitamos confirmar tu número de WhatsApp/Teléfono.
                </p>

                <div className="w-full bg-[#1A1A1C] border border-[#D4AF37]/30 p-4 rounded-lg mb-6 flex items-start gap-3">
                  <AlertCircle size={20} className="text-[#D4AF37] flex-shrink-0 mt-0.5" />
                  <p className="text-xs text-gray-300">
                    Solo utilizamos esto para el <span className="font-bold text-white">Seguimiento CRM</span> de tus predicciones gratis y la verificación de tu cuenta local.
                  </p>
                </div>

                <form onSubmit={handleSubmitPhone} className="w-full space-y-4">
                  <div>
                    <label className="block text-xs text-gray-400 font-medium mb-1 uppercase tracking-wider">Número Celular</label>
                    <input 
                      type="tel"
                      value={phoneNumber}
                      onChange={(e) => setPhoneNumber(e.target.value)}
                      placeholder="+1 (555) 000-0000"
                      className="w-full bg-black border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-[#D4AF37] transition-colors"
                      required
                      disabled={isLoading}
                    />
                  </div>
                  <button 
                    type="submit"
                    disabled={isLoading}
                    className="w-full py-3 rounded-xl bg-[#D4AF37] text-black font-bold flex items-center justify-center gap-2 hover:bg-[#F3CE5E] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {isLoading ? (
                      <>
                        <Loader2 size={18} className="animate-spin" />
                        Guardando...
                      </>
                    ) : (
                      'Confirmar y Desbloquear Picks'
                    )}
                  </button>
                </form>
              </motion.div>
            )}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
```

- [ ] **Paso 2: Agregar import faltante de CheckCircle2**

```bash
# Verificar que CheckCircle2 esté importado
grep "CheckCircle2" src/components/AuthModal.tsx || echo "Falta importar CheckCircle2"
```

Si falta, agregarlo a la línea de imports con `AlertCircle`.

- [ ] **Paso 3: Commit**

```bash
git add src/components/AuthModal.tsx
git commit -m "feat(auth): implementar AuthModal con lógica real de Supabase"
```

---

## Fase 6: Actualización de la Página Principal

### Task 6.1: Integrar autenticación en page.tsx

**Archivos:**
- Modificar: `src/app/page.tsx`

- [ ] **Paso 1: Actualizar imports y agregar useAuth**

Modificar la parte superior del archivo:

```typescript
// src/app/page.tsx
"use client";

import React, { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { TrendingUp, Target, Activity, Lock, AlertCircle, CheckCircle2, ChevronRight, LogOut, User } from "lucide-react";
import AuthModal from "../components/AuthModal";
import PaymentModal from "../components/PaymentModal";
import { useAuth } from "../components/AuthContext";
```

- [ ] **Paso 2: Agregar componente UserButton dentro del archivo**

Agregar antes del componente principal:

```typescript
// Componente de botón de usuario
function UserButton() {
  const { user, signOut, isLoading } = useAuth();
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  if (isLoading) {
    return (
      <div className="w-8 h-8 rounded-full bg-[#D4AF37]/20 animate-pulse" />
    );
  }

  if (!user) return null;

  return (
    <div className="relative">
      <button
        onClick={() => setIsMenuOpen(!isMenuOpen)}
        className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-[#D4AF37]/10 border border-[#D4AF37]/30 text-[#D4AF37] hover:bg-[#D4AF37]/20 transition-colors"
      >
        <User size={16} />
        <span className="text-sm font-medium truncate max-w-[120px]">
          {user.email?.split('@')[0]}
        </span>
      </button>

      {isMenuOpen && (
        <div className="absolute right-0 top-full mt-2 w-48 bg-[#1A1A1C] border border-white/10 rounded-lg shadow-xl py-2 z-50">
          <button
            onClick={() => {
              signOut();
              setIsMenuOpen(false);
            }}
            className="w-full px-4 py-2 text-left text-sm text-gray-300 hover:bg-white/5 flex items-center gap-2"
          >
            <LogOut size={14} />
            Cerrar Sesión
          </button>
        </div>
      )}
    </div>
  );
}
```

- [ ] **Paso 3: Actualizar el header para mostrar UserButton**

Dentro del componente `SportGuruDashboard`, agregar después de `<motion.div>` inicial:

```typescript
// En el header section, agregar UserButton:
<motion.div
  initial={{ opacity: 0, y: -20 }}
  animate={{ opacity: 1, y: 0 }}
  className="container mx-auto px-6 text-center relative z-10"
>
  {/* Agregar UserButton en la esquina superior derecha */}
  <div className="absolute top-0 right-0">
    <UserButton />
  </div>
  
  {/* ... resto del contenido ... */}
</motion.div>
```

- [ ] **Paso 4: Agregar lógica de detección de query params para auth**

Dentro del componente principal, agregar después de los hooks existentes:

```typescript
export default function SportGuruDashboard() {
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isPaymentOpen, setIsPaymentOpen] = useState(false);
  const [selectedPick, setSelectedPick] = useState("");
  const { user, isLoading } = useAuth();

  // Detectar query params de auth al cargar
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    const authParam = params.get('auth');
    
    if (authParam === 'phone_required') {
      setIsAuthOpen(true);
    } else if (authParam === 'error') {
      // Mostrar error de auth
      alert('Error en la autenticación. Por favor intenta de nuevo.');
      // Limpiar URL
      window.history.replaceState({}, '', '/');
    }
  }, []);

  // ... resto del código
```

- [ ] **Paso 5: Commit**

```bash
git add src/app/page.tsx
git commit -m "feat(page): integrar componente de usuario y detección de auth"
```

---

## Fase 7: Configuración en Supabase Dashboard

### Task 7.1: Instrucciones de configuración

**Nota:** Estas instrucciones deben seguirse manualmente en el dashboard de Supabase.

- [ ] **Paso 1: Crear proyecto en Supabase**

1. Ir a https://supabase.com/dashboard
2. Crear nuevo proyecto
3. Nombre: "sport-guru-ai"
4. Guardar las credenciales mostradas

- [ ] **Paso 2: Ejecutar schema SQL**

En el SQL Editor de Supabase, ejecutar el contenido de `supabase_schema.sql`:

```sql
-- Ejecutar línea por línea o como un solo bloque
-- Este archivo ya existe en el proyecto
```

- [ ] **Paso 3: Configurar Google OAuth**

En Authentication > Providers:
1. Habilitar "Google"
2. Obtener Client ID y Client Secret de Google Cloud Console
3. Agregar redirect URL: `http://localhost:3000/auth/callback`

- [ ] **Paso 4: Actualizar variables de entorno locales**

```bash
# Reemplazar valores en .env.local
NEXT_PUBLIC_SUPABASE_URL=https://tu-proyecto.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=tu-anon-key
SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key
```

---

## Fase 8: Testing y Verificación

### Task 8.1: Verificar funcionamiento

- [ ] **Paso 1: Iniciar servidor de desarrollo**

```bash
npm run dev
```

- [ ] **Paso 2: Probar flujos**

1. Abrir http://localhost:3000
2. Hacer clic en "Ver Análisis Completo" → Debe abrir AuthModal
3. Probar "Continuar con Google"
4. Probar registro con Email
5. Verificar captura de teléfono
6. Verificar cierre de sesión

- [ ] **Paso 3: Verificar protección de rutas**

```bash
# Intentar acceder a ruta protegida sin auth
curl http://localhost:3000/premium
# Debe redirigir al home con param auth=required
```

---

## Summary de Archivos Creados/Modificados

| Archivo | Acción | Descripción |
|---------|--------|-------------|
| `package.json` | Modificar | Agregar dependencias Supabase |
| `.env.local` | Crear | Variables de entorno |
| `src/lib/supabase/client.ts` | Crear | Cliente browser |
| `src/lib/supabase/server.ts` | Crear | Cliente server + helpers |
| `src/middleware.ts` | Crear | Protección de rutas |
| `src/components/AuthContext.tsx` | Crear | Contexto React de auth |
| `src/app/layout.tsx` | Modificar | Integrar AuthProvider |
| `src/app/auth/callback/page.tsx` | Crear | Página de callback OAuth |
| `src/app/api/user/profile/route.ts` | Crear | API obtener perfil |
| `src/app/api/user/phone/route.ts` | Crear | API guardar teléfono |
| `src/components/AuthModal.tsx` | Reemplazar | Auth real con Supabase |
| `src/app/page.tsx` | Modificar | Integrar UserButton + auth detection |

---

## Criterios de Aceptación

- [ ] Usuario puede registrarse con Google OAuth
- [ ] Usuario puede registrarse con Email/Password
- [ ] Usuario puede iniciar sesión con ambos métodos
- [ ] Sistema solicita teléfono después del primer login
- [ ] Teléfono se guarda en tabla profiles
- [ ] Picks premium están protegidos (requieren auth)
- [ ] Usuario puede cerrar sesión
- [ ] Sesión persiste después de recargar página
- [ ] Middleware protege rutas /premium/*
- [ ] UI muestra errores de autenticación claros
- [ ] Loading states funcionan correctamente

---

**Plan creado:** 2026-04-10  
**Status:** Listo para ejecución
