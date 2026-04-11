"use client";

import React, { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Lock, Smartphone, Mail, AlertCircle, X } from "lucide-react";

interface AuthModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function AuthModal({ isOpen, onClose }: AuthModalProps) {
  const [step, setStep] = useState<"login" | "phone_capture">("login");
  const [phoneNumber, setPhoneNumber] = useState("");

  const handleSimulatedGoogleLogin = () => {
    // Simularemos que inició sesión con Google pero no nos dio el teléfono
    setStep("phone_capture");
  };

  const handleSubmitPhone = (e: React.FormEvent) => {
    e.preventDefault();
    if (phoneNumber.length > 7) {
      // Éxito: Guardar en Supabase y cerrar
      alert("¡Teléfono verificado! Prospecto guardado en CRM.");
      onClose();
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
            onClick={onClose}
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
              onClick={onClose}
              className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
            >
              <X size={20} />
            </button>

            {step === "login" ? (
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 bg-[#D4AF37]/10 rounded-full flex items-center justify-center mb-4 text-[#D4AF37]">
                  <Lock size={24} />
                </div>
                <h3 className="text-2xl font-bold text-white mb-2">Desbloquea el Pick</h3>
                <p className="text-sm text-gray-400 text-center mb-8">
                  Regístrate gratis para ver el análisis completo o comprar picks premium.
                </p>

                <div className="w-full space-y-3">
                  <button 
                    onClick={handleSimulatedGoogleLogin}
                    className="w-full py-3 px-4 bg-white hover:bg-gray-100 text-black rounded-lg font-semibold flex items-center justify-center gap-3 transition-colors"
                  >
                    <svg className="w-5 h-5" viewBox="0 0 24 24">
                      <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4"/>
                      <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.07v2.84C3.89 20.5 7.67 23 12 23z" fill="#34A853"/>
                      <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.07C1.34 8.52.95 10.2.95 12s.39 3.48 1.12 4.93l3.77-2.84z" fill="#FBBC05"/>
                      <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.67 1 3.89 3.5 2.07 7.07l3.77 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335"/>
                    </svg>
                    Continuar con Google
                  </button>
                  
                  <button 
                    onClick={handleSimulatedGoogleLogin}
                    className="w-full py-3 px-4 bg-[#1A1A1C] border border-white/5 hover:bg-white/5 text-white rounded-lg font-semibold flex items-center justify-center gap-3 transition-colors"
                  >
                    <Smartphone size={20} />
                    Usar Teléfono o SMS
                  </button>

                  <button 
                    onClick={handleSimulatedGoogleLogin}
                    className="w-full py-3 px-4 bg-[#1A1A1C] border border-white/5 hover:bg-white/5 text-white rounded-lg font-semibold flex items-center justify-center gap-3 transition-colors"
                  >
                    <Mail size={20} />
                    Continuar con Email
                  </button>
                </div>
              </div>
            ) : (
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
                    />
                  </div>
                  <button 
                    type="submit"
                    className="w-full py-3 rounded-xl bg-[#D4AF37] text-black font-bold flex items-center justify-center gap-2 hover:bg-[#F3CE5E] transition-colors"
                  >
                    Confirmar y Desbloquear Picks
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
