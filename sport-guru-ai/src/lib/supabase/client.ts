// src/lib/supabase/client.ts
// Cliente de Supabase para componentes del navegador (Browser Client)
// Usamos la API moderna @supabase/ssr (no los helpers deprecados)

import { createBrowserClient } from '@supabase/ssr'

/**
 * Crea un cliente de Supabase para uso en el navegador.
 * Este cliente se usa en componentes client-side de Next.js.
 *
 * @returns Cliente de Supabase configurado para browser
 */
export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
  )
}

/**
 * Singleton del cliente de Supabase.
 * Se reutiliza la misma instancia en toda la aplicación cliente.
 * Esto mejora el rendimiento evitando crear múltiples clientes.
 */
export const supabaseClient = createClient()

/**
 * Helper para obtener el cliente de Supabase en componentes cliente.
 * Uso recomendado: importa esta función en tus componentes cliente
 *
 * Ejemplo:
 * const supabase = getSupabaseClient()
 * const { data } = await supabase.from('tabla').select()
 *
 * @returns La instancia singleton del cliente de Supabase
 */
export function getSupabaseClient() {
  return supabaseClient
}
