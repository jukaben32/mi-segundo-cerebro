-- sportguru_schema.sql
-- Arquitectura de Base de Datos para SportGuru AI (Supabase)

-- 1. Tabla de Picks (Predicciones)
CREATE TABLE picks (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    sport TEXT NOT NULL, -- Ej: 'NBA', 'MLB', 'NFL'
    matchup TEXT NOT NULL, -- Ej: 'Lakers vs Warriors'
    prediction TEXT NOT NULL, -- Ej: 'Lakers -5.5'
    confidence_index DECIMAL NOT NULL, -- Ej: 85.5
    odds TEXT NOT NULL, -- Ej: '-110'
    rationale TEXT NOT NULL, -- El mini-artículo generado por Claude
    is_premium BOOLEAN DEFAULT false, -- True si cuesta $1
    status TEXT DEFAULT 'pending', -- 'pending', 'hit', 'miss'
    match_date TIMESTAMPTZ NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Tabla del Contador Global (Hit Counter)
CREATE TABLE hit_stats (
    id SERIAL PRIMARY KEY,
    total_hits INT DEFAULT 0,
    total_misses INT DEFAULT 0,
    current_streak INT DEFAULT 0,
    projected_roi DECIMAL DEFAULT 0.00,
    last_updated TIMESTAMPTZ DEFAULT NOW()
);

-- Iniciar con datos base para el contador
INSERT INTO hit_stats (total_hits, total_misses, current_streak, projected_roi)
VALUES (0, 0, 0, 0.00);

-- Función para actualizar el status automáticamente
CREATE OR REPLACE FUNCTION update_hit_stats_trigger()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'hit' AND OLD.status != 'hit' THEN
        UPDATE hit_stats SET 
            total_hits = total_hits + 1,
            current_streak = current_streak + 1;
    ELSIF NEW.status = 'miss' AND OLD.status != 'miss' THEN
        UPDATE hit_stats SET 
            total_misses = total_misses + 1,
            current_streak = 0;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_hit_stats
AFTER UPDATE OF status ON picks
FOR EACH ROW
EXECUTE FUNCTION update_hit_stats_trigger();

-- 3. Tabla de Perfiles (Usuarios con Teléfono Obligatorio para CRM)
CREATE TABLE profiles (
    id UUID REFERENCES auth.users NOT NULL PRIMARY KEY,
    phone_number TEXT,
    email TEXT,
    full_name TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Trigger para crear perfil automáticamente cuando un usuario se registra
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS trigger AS $$
BEGIN
  INSERT INTO public.profiles (id, email, phone_number, full_name)
  VALUES (
    new.id, 
    new.email, 
    new.raw_user_meta_data->>'phone',
    new.raw_user_meta_data->>'full_name'
  );
  RETURN new;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER on_auth_user_created
  AFTER INSERT ON auth.users
  FOR EACH ROW EXECUTE PROCEDURE public.handle_new_user();
