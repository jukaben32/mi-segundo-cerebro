// src/components/AuthContext.tsx
// Contexto de autenticación para toda la aplicación
// Provee estado de sesión, usuario y métodos de login/logout usando Supabase

'use client'

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { User, Session } from '@supabase/supabase-js'
import { createClient } from '../lib/supabase/client'

// Tipo del contexto de autenticación
interface AuthContextType {
  user: User | null
  session: Session | null
  isLoading: boolean
  isAuthenticated: boolean
  signInWithGoogle: () => Promise<void>
  signInWithEmail: (email: string, password: string) => Promise<void>
  signUpWithEmail: (email: string, password: string) => Promise<void>
  signOut: () => Promise<void>
  needsPhone: boolean
  setNeedsPhone: (value: boolean) => void
}

// Crear el contexto (inicialmente undefined para detectar uso incorrecto)
const AuthContext = createContext<AuthContextType | undefined>(undefined)

// Singleton del cliente de Supabase para evitar múltiples instancias
const supabase = createClient()

/**
 * Proveedor de autenticación que envuelve la aplicación.
 * Maneja el estado de sesión y provee métodos de autenticación a todos los componentes hijos.
 */
export function AuthProvider({ children }: { children: React.ReactNode }) {
  // Estado del usuario y sesión
  const [user, setUser] = useState<User | null>(null)
  const [session, setSession] = useState<Session | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [needsPhone, setNeedsPhone] = useState(false)

  // Efecto para inicializar el estado de autenticación al montar el componente
  useEffect(() => {
    const initializeAuth = async () => {
      try {
        // Obtener sesión inicial desde Supabase
        const { data: { session } } = await supabase.auth.getSession()
        setSession(session)
        setUser(session?.user ?? null)
      } catch (error) {
        console.error('Error initializing auth:', error)
      } finally {
        setIsLoading(false)
      }
    }

    initializeAuth()

    // Suscribirse a cambios de autenticación (login, logout, token refresh)
    const { data: { subscription } } = supabase.auth.onAuthStateChange(
      (_event, session) => {
        setSession(session)
        setUser(session?.user ?? null)
      }
    )

    // Limpiar suscripción al desmontar
    return () => subscription.unsubscribe()
  }, [])

  // Iniciar sesión con Google OAuth
  const signInWithGoogle = useCallback(async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: `${window.location.origin}/auth/callback`,
      },
    })
    if (error) throw error
  }, [])

  // Iniciar sesión con email y contraseña
  const signInWithEmail = useCallback(async (email: string, password: string) => {
    const { error } = await supabase.auth.signInWithPassword({
      email,
      password,
    })
    if (error) throw error
  }, [])

  // Registrar nuevo usuario con email y contraseña
  const signUpWithEmail = useCallback(async (email: string, password: string) => {
    const { error } = await supabase.auth.signUp({
      email,
      password,
      options: {
        emailRedirectTo: `${window.location.origin}/auth/callback`,
      },
    })
    if (error) throw error
  }, [])

  // Cerrar sesión y limpiar estado
  const signOut = useCallback(async () => {
    const { error } = await supabase.auth.signOut()
    if (error) throw error
    setNeedsPhone(false)
    setUser(null)
    setSession(null)
  }, [])

  // Valor del contexto que será accesible a través de useAuth()
  const value: AuthContextType = {
    user,
    session,
    isLoading,
    isAuthenticated: !!user,
    signInWithGoogle,
    signInWithEmail,
    signUpWithEmail,
    signOut,
    needsPhone,
    setNeedsPhone,
  }

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

/**
 * Hook personalizado para acceder al contexto de autenticación.
 * Debe usarse dentro de un AuthProvider.
 * @throws Error si se usa fuera de AuthProvider
 */
export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
