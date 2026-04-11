"use client";

import React, { useState } from "react";
import { motion } from "framer-motion";
import { TrendingUp, Target, Activity, Lock, AlertCircle, CheckCircle2, ChevronRight } from "lucide-react";
import AuthModal from "../components/AuthModal";
import PaymentModal from "../components/PaymentModal";

export default function SportGuruDashboard() {
  const [isAuthOpen, setIsAuthOpen] = useState(false);
  const [isPaymentOpen, setIsPaymentOpen] = useState(false);
  const [selectedPick, setSelectedPick] = useState("");

  const handlePremiumClick = (pickName: string) => {
    setSelectedPick(pickName);
    setIsPaymentOpen(true);
  };

  const containerVariants = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 },
    },
  };

  const itemVariants = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 },
  };

  return (
    <main className="min-h-screen bg-[#0A0A0B] text-[#EDEDED] flex flex-col items-center">
      {/* Header / Hero */}
      <header className="w-full flex-col items-center justify-center pt-16 pb-12 border-b border-white/5 relative overflow-hidden">
        <div className="absolute inset-0 bg-gradient-to-b from-[#D4AF37]/5 to-transparent pointer-events-none" />
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="container mx-auto px-6 text-center relative z-10"
        >
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full glass-panel text-xs text-[#D4AF37] mb-6 tracking-widest uppercase">
            <Activity size={14} /> The Brain Engine is Active
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight mb-4">
            SportGuru <span className="text-[#D4AF37]">AI</span>
          </h1>
          <p className="text-lg md:text-xl text-gray-400 max-w-2xl mx-auto font-light">
            No es una apuesta, es una inversión basada en datos. Accede a predicciones generadas por el modelo de IA más estricto del mercado.
          </p>
        </motion.div>
      </header>

      {/* Hit Counter Section */}
      <section className="w-full max-w-6xl px-6 py-12">
        <motion.div
          variants={containerVariants}
          initial="hidden"
          animate="show"
          className="grid grid-cols-1 md:grid-cols-3 gap-6"
        >
          {/* Free Picks Performance */}
          <motion.div variants={itemVariants} className="glass-panel p-6 rounded-2xl flex flex-col relative overflow-hidden">
            <div className="absolute top-0 right-0 w-32 h-32 bg-[#22C55E]/10 rounded-full blur-3xl -mr-16 -mt-16" />
            <span className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-2">Desempeño Picks Gratis</span>
            <div className="flex items-end gap-3">
              <span className="text-5xl font-bold text-[#22C55E]">68%</span>
            </div>
            <div className="mt-4 flex items-center gap-2 text-sm text-[#22C55E]">
              <TrendingUp size={16} /> 142 de 208 Acertados
            </div>
          </motion.div>

          {/* VIP Premium Performance (The FOMO Trigger) */}
          <motion.div variants={itemVariants} className="glass-panel p-6 rounded-2xl flex flex-col border border-[#D4AF37]/20 relative overflow-hidden shadow-[0_0_30px_rgba(212,175,55,0.05)]">
            <div className="absolute top-0 right-0 w-32 h-32 bg-[#D4AF37]/15 rounded-full blur-3xl -mr-16 -mt-16" />
            <span className="text-[#D4AF37] text-sm font-medium uppercase tracking-wider mb-2">Desempeño VIP Premium</span>
            <div className="flex items-end gap-3 relative z-10">
              <span className="text-5xl font-bold text-[#D4AF37]">84%</span>
              <span className="text-gray-500 mb-1 font-mono text-sm">WIN RATE</span>
            </div>
            <div className="mt-4 flex items-center gap-2 text-sm text-[#D4AF37]/80 relative z-10">
              <Target size={16} /> Algoritmo Institucional
            </div>
          </motion.div>

          {/* Projected ROI */}
          <motion.div variants={itemVariants} className="glass-panel p-6 rounded-2xl flex flex-col relative overflow-hidden">
            <span className="text-gray-400 text-sm font-medium uppercase tracking-wider mb-2">ROI Proyectado VIP</span>
            <div className="flex items-end gap-3">
              <span className="text-5xl font-bold text-white">+14.2%</span>
            </div>
            <div className="mt-4 flex items-center gap-2 text-sm text-gray-400">
              Sobre bankroll base de $1,000 en 30 días
            </div>
          </motion.div>
        </motion.div>
      </section>

      {/* Predictions Dashboard */}
      <section className="w-full max-w-6xl px-6 pb-24">
        <div className="flex justify-between items-end mb-8">
          <div>
            <h2 className="text-2xl font-bold">Picks del Día</h2>
            <p className="text-gray-400 mt-1">Análisis por Claude 3.5 y The Odds API</p>
          </div>
          <div className="text-sm font-medium bg-white/5 px-3 py-1 rounded-full text-gray-400">
            Actualizado hace 15 mins
          </div>
        </div>

        <motion.div variants={containerVariants} initial="hidden" animate="show" className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          
          {/* Free Pick */}
          <motion.div variants={itemVariants} className="glass-panel p-6 rounded-2xl flex flex-col hover:border-white/20 transition-all cursor-pointer group">
            <div className="flex justify-between items-start mb-4">
              <span className="bg-white/10 text-white text-xs px-2 py-1 rounded font-bold uppercase">NBA</span>
              <span className="bg-[#22C55E]/20 text-[#22C55E] text-xs px-2 py-1 rounded font-bold uppercase flex items-center gap-1">
                <CheckCircle2 size={12} /> Free Pick
              </span>
            </div>
            <h3 className="text-xl font-bold mb-1">Lakers vs Warriors</h3>
            <p className="text-gray-400 text-sm mb-4">Lakers +5.5 (Spread)</p>
            
            <div className="w-full bg-white/5 rounded-full h-1.5 mb-2 overflow-hidden">
              <div className="bg-[#22C55E] h-1.5 rounded-full" style={{ width: "85%" }} />
            </div>
            <div className="flex justify-between text-xs text-gray-400 mb-6">
              <span>Índice de Confianza</span>
              <span className="text-[#22C55E] font-bold">85%</span>
            </div>

            <p className="text-sm text-gray-300 font-light line-clamp-3 mb-6 flex-grow">
              Consenso algorítmico apunta a una sobrevaloración de Warriors en casa. AD tiene matchup favorable contra la línea interior actual de GSW.
            </p>

            {/* Bookmaker Odds Comparison (The Odds API Mock UI) */}
            <div className="bg-black/40 border border-white/5 rounded-lg p-3 mb-6">
              <span className="text-[10px] uppercase tracking-widest text-gray-500 font-bold mb-2 block flex items-center gap-1">
                Líneas en Vivo <Activity size={10} className="text-[#D4AF37]" />
              </span>
              <div className="flex flex-col gap-2">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-gray-400">Pinnacle (Sharp)</span>
                  <span className="bg-[#1A1A1C] px-2 py-1 rounded border border-white/10 font-mono text-[#D4AF37]">+5.5 (-115)</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-gray-400">DraftKings</span>
                  <span className="bg-[#1A1A1C] px-2 py-1 rounded border border-white/10 font-mono text-gray-300">+5.0 (-110)</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-gray-400">FanDuel</span>
                  <span className="bg-[#1A1A1C] px-2 py-1 rounded border border-white/10 font-mono text-gray-300">+5.5 (-105)</span>
                </div>
              </div>
            </div>

            <button 
              onClick={() => setIsAuthOpen(true)}
              className="w-full py-3 rounded-xl bg-white text-black font-bold flex items-center justify-center gap-2 group-hover:bg-gray-200 transition-colors"
            >
              Ver Análisis Completo <ChevronRight size={16} />
            </button>
          </motion.div>

          {/* Premium Pick 1 */}
          <motion.div variants={itemVariants} className="glass-panel p-6 rounded-2xl flex flex-col border border-[#D4AF37]/30 relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-br from-[#D4AF37]/5 to-transparent pointer-events-none" />
            <div className="flex justify-between items-start mb-4 relative z-10">
              <span className="bg-white/10 text-white text-xs px-2 py-1 rounded font-bold uppercase">MLB</span>
              <span className="bg-[#D4AF37]/20 text-[#D4AF37] text-xs px-2 py-1 rounded font-bold uppercase flex items-center gap-1">
                <Lock size={12} /> Premium
              </span>
            </div>
            <h3 className="text-xl font-bold mb-1 relative z-10">Yankees vs Red Sox</h3>
            <p className="text-gray-400 text-sm mb-4 relative z-10">Moneyline Oculta</p>
            
            <div className="w-full bg-white/5 rounded-full h-1.5 mb-2 overflow-hidden relative z-10">
              <div className="bg-[#D4AF37] h-1.5 rounded-full" style={{ width: "92%" }} />
            </div>
            <div className="flex justify-between text-xs text-gray-400 mb-6 relative z-10">
              <span>Índice de Confianza</span>
              <span className="text-[#D4AF37] font-bold">92%</span>
            </div>

            <div className="flex-grow flex flex-col items-center justify-center py-4 relative z-10 text-center">
              <AlertCircle size={24} className="text-[#D4AF37] mb-2 opacity-80" />
              <p className="text-sm text-gray-300">Análisis exclusivo de pitching matchups y clima detecta ineficiencia de cuotas (Vegas).</p>
            </div>

            <button 
              onClick={() => setIsAuthOpen(true)}
              className="w-full py-3 rounded-xl bg-[#D4AF37] text-black font-bold flex items-center justify-center gap-2 hover:bg-[#F3CE5E] transition-colors relative z-10 mt-2"
            >
              Desbloquear Pick - $1
            </button>
          </motion.div>

           {/* Premium Pick 2 */}
           <motion.div variants={itemVariants} className="glass-panel p-6 rounded-2xl flex flex-col border border-[#D4AF37]/30 relative overflow-hidden group">
            <div className="absolute inset-0 bg-gradient-to-br from-[#D4AF37]/5 to-transparent pointer-events-none" />
            <div className="flex justify-between items-start mb-4 relative z-10">
              <span className="bg-white/10 text-white text-xs px-2 py-1 rounded font-bold uppercase">NFL</span>
              <span className="bg-[#D4AF37]/20 text-[#D4AF37] text-xs px-2 py-1 rounded font-bold uppercase flex items-center gap-1">
                <Lock size={12} /> Premium
              </span>
            </div>
            <h3 className="text-xl font-bold mb-1 relative z-10">Chiefs vs Ravens</h3>
            <p className="text-gray-400 text-sm mb-4 relative z-10">Total Points Oculto</p>
            
            <div className="w-full bg-white/5 rounded-full h-1.5 mb-2 overflow-hidden relative z-10">
              <div className="bg-[#D4AF37] h-1.5 rounded-full" style={{ width: "88%" }} />
            </div>
            <div className="flex justify-between text-xs text-gray-400 mb-6 relative z-10">
              <span>Índice de Confianza</span>
              <span className="text-[#D4AF37] font-bold">88%</span>
            </div>

            <div className="flex-grow flex flex-col items-center justify-center py-4 relative z-10 text-center">
              <AlertCircle size={24} className="text-[#D4AF37] mb-2 opacity-80" />
              <p className="text-sm text-gray-300">Algoritmo identifica patrón de lesiones que afecta draśticamente el Under/Over real.</p>
            </div>

            <button 
              onClick={() => setIsAuthOpen(true)}
              className="w-full py-3 rounded-xl bg-[#D4AF37] text-black font-bold flex items-center justify-center gap-2 hover:bg-[#F3CE5E] transition-colors relative z-10 mt-2"
            >
              Desbloquear Pick - $1
            </button>
          </motion.div>

        </motion.div>
      </section>

      <AuthModal isOpen={isAuthOpen} onClose={() => setIsAuthOpen(false)} />
      <PaymentModal isOpen={isPaymentOpen} onClose={() => setIsPaymentOpen(false)} pickName={selectedPick} />
    </main>
  );
}
