// Middleware de autenticacion para Next.js
// Protege las rutas premium y redirige al login si no hay sesion

import { NextResponse } from 'next/server'
import type { NextRequest } from 'next/server'
import { createServerClient, type CookieOptions } from '@supabase/ssr'

// Rutas que requieren autenticacion
const PROTECTED_ROUTES = ['/premium', '/checkout', '/profile']

export async function middleware(request: NextRequest) {
  // Crear un response base
  let response = NextResponse.next({
    request: {
      headers: request.headers,
    },
  })

  // Crear cliente de Supabase para middleware
  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        get(name: string) {
          return request.cookies.get(name)?.value
        },
        set(name: string, value: string, options: CookieOptions) {
          // Establecer cookie en el request para lectura
          request.cookies.set({
            name,
            value,
            ...options,
          })
          // Establecer cookie en el response para enviar al browser
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value,
            ...options,
          })
        },
        remove(name: string, options: CookieOptions) {
          request.cookies.set({
            name,
            value: '',
            ...options,
            maxAge: 0,
          })
          response = NextResponse.next({
            request: {
              headers: request.headers,
            },
          })
          response.cookies.set({
            name,
            value: '',
            ...options,
            maxAge: 0,
          })
        },
      },
    }
  )

  // Refrescar la sesion si existe
  const { data: { user } } = await supabase.auth.getUser()

  const { pathname } = request.nextUrl

  // Verificar si la ruta esta protegida
  const isProtected = PROTECTED_ROUTES.some(route => pathname.startsWith(route))

  // Si es ruta protegida y no hay usuario, redirigir al login
  if (isProtected && !user) {
    const loginUrl = new URL('/', request.url)
    loginUrl.searchParams.set('auth', 'required')
    loginUrl.searchParams.set('returnTo', pathname)
    return NextResponse.redirect(loginUrl)
  }

  return response
}

// Configurar matcher para rutas
export const config = {
  matcher: [
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',
  ],
}
