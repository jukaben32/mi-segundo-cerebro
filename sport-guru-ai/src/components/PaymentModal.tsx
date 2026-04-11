"use client";

import React, { useState } from "react";
import { CreditCard, Landmark, Bitcoin, X, Copy, CheckCircle2, AlertCircle } from "lucide-react";

interface PaymentModalProps {
  isOpen: boolean;
  onClose: () => void;
  pickName: string;
}

export default function PaymentModal({ isOpen, onClose, pickName }: PaymentModalProps) {
  const [method, setMethod] = useState<"selector" | "stripe" | "transfer" | "crypto">("selector");
  const [copiedBank, setCopiedBank] = useState<string | null>(null);

  const bankAccounts = [
    { id: "banreservas", name: "Banreservas", account: "960-000000-1", type: "Ahorros" },
    { id: "bhd", name: "Banco BHD", account: "1234567-001-1", type: "Corriente" },
    { id: "popular", name: "Banco Popular", account: "765432101", type: "Ahorros" },
    { id: "scotia", name: "Scotiabank", account: "001-987654", type: "Ahorros" },
  ];

  const cryptoWallets = [
    { id: "btc", name: "Bitcoin (BTC)", network: "Bitcoin Network", address: "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh" },
    { id: "usdt", name: "USDT (Tether)", network: "TRC20 (Tron)", address: "T9zX3Qy2KgwA7B1oPlJmz98..." },
    { id: "sol", name: "Solana (SOL)", network: "Solana Network", address: "8x8X9Qy2KgwAL1T..." }
  ];

  const handleCopy = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedBank(id);
    setTimeout(() => setCopiedBank(null), 2000);
  };

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => { setMethod("selector"); onClose(); }}
            className="absolute inset-0 bg-black/60 backdrop-blur-sm"
          />

          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            className="relative w-full max-w-md bg-[#121214] border border-[#D4AF37]/30 rounded-2xl shadow-2xl p-6 overflow-hidden"
          >
            <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[#D4AF37]/0 via-[#D4AF37] to-[#D4AF37]/0 opacity-80" />
            
            <button
              onClick={() => { setMethod("selector"); onClose(); }}
              className="absolute top-4 right-4 text-gray-400 hover:text-white transition-colors"
            >
              <X size={20} />
            </button>

            {method === "selector" && (
              <div className="flex flex-col items-center">
                <div className="w-12 h-12 bg-[#D4AF37]/10 rounded-full flex items-center justify-center mb-4 text-[#D4AF37]">
                  <CreditCard size={24} />
                </div>
                <h3 className="text-2xl font-bold text-white mb-1">Desbloquear Pick Premium</h3>
                <p className="text-sm text-[#D4AF37] font-medium mb-6">{pickName}</p>
                <p className="text-sm text-gray-400 text-center mb-8">
                  Elige tu método de pago preferido para acceder al análisis VIP de $1.
                </p>

                <div className="w-full space-y-3">
                  <button 
                    onClick={() => setMethod("stripe")}
                    className="w-full py-3 px-4 bg-[#635BFF] hover:bg-[#5249E5] text-white rounded-lg font-bold flex items-center justify-center gap-3 transition-colors shadow-lg shadow-[#635BFF]/20"
                  >
                    <CreditCard size={20} />
                    Pagar con Tarjeta (Stripe)
                  </button>
                  
                  <button 
                    onClick={() => setMethod("transfer")}
                    className="w-full py-3 px-4 bg-[#1A1A1C] border border-white/10 hover:border-[#D4AF37]/50 text-white rounded-lg font-bold flex items-center justify-center gap-3 transition-colors"
                  >
                    <Landmark size={20} className="text-[#D4AF37]" />
                    Transferencia Bancaria Local (RD)
                  </button>

                  <button 
                    onClick={() => setMethod("crypto")}
                    className="w-full py-3 px-4 bg-[#1A1A1C] border border-white/10 hover:border-[#F7931A]/50 text-white rounded-lg font-bold flex items-center justify-center gap-3 transition-colors"
                  >
                    <Bitcoin size={20} className="text-[#F7931A]" />
                    Pagar con Criptomonedas
                  </button>
                </div>
              </div>
            )}

            {method === "stripe" && (
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex flex-col items-center"
              >
                <h3 className="text-xl font-bold text-white mb-2">Pago con Stripe</h3>
                <p className="text-sm text-gray-400 text-center mb-6">
                  Serás redirigido a la pasarela segura de Stripe para completar el pago de $1.00 USD.
                </p>
                
                <div className="w-full bg-[#1A1A1C] p-4 rounded-xl mb-6 border border-white/5">
                  <div className="flex justify-between items-center mb-2">
                    <span className="text-gray-400">Concepto</span>
                    <span className="text-white font-medium">{pickName} VIP</span>
                  </div>
                  <div className="flex justify-between items-center text-lg font-bold">
                    <span className="text-gray-400">Total</span>
                    <span className="text-[#22C55E]">$1.00 USD</span>
                  </div>
                </div>

                <div className="flex gap-3 w-full">
                  <button 
                    onClick={() => setMethod("selector")}
                    className="w-1/3 py-3 rounded-xl bg-white/5 text-white font-semibold hover:bg-white/10 transition-colors"
                  >
                    Volver
                  </button>
                  <button 
                    onClick={() => alert("Próximamente: Redirección de Checkout (StripeAPI)")}
                    className="w-2/3 py-3 rounded-xl bg-[#635BFF] text-white font-bold hover:bg-[#5249E5] transition-colors"
                  >
                    Proceder al Pago
                  </button>
                </div>
              </motion.div>
            )}

            {method === "transfer" && (
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex flex-col w-full"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-white">Cuentas Bancarias</h3>
                  <button onClick={() => setMethod("selector")} className="text-xs text-[#D4AF37] hover:underline">Volver</button>
                </div>
                
                <p className="text-xs text-gray-400 mb-4">
                  Transfiere el equivalente a <span className="text-white font-bold">$1.00 USD (Aprox. RD$59.00)</span>.
                  Una vez transferido, sube tu comprobante o avísanos por WhatsApp.
                </p>

                <div className="w-full space-y-3 max-h-[250px] overflow-y-auto pr-2 custom-scrollbar">
                  {bankAccounts.map((bank) => (
                    <div key={bank.id} className="bg-[#1A1A1C] border border-white/10 rounded-xl p-3 flex flex-col gap-1 relative group hover:border-[#D4AF37]/50 transition-colors">
                      <span className="text-white font-bold text-sm">{bank.name}</span>
                      <div className="flex items-center justify-between">
                        <span className="text-[#D4AF37] font-mono text-lg tracking-wider">{bank.account}</span>
                        <button 
                          onClick={() => handleCopy(bank.id, bank.account)}
                          className="text-gray-400 hover:text-white transition-colors"
                          title="Copiar Cuenta"
                        >
                          {copiedBank === bank.id ? <CheckCircle2 size={18} className="text-[#22C55E]" /> : <Copy size={18} />}
                        </button>
                      </div>
                      <span className="text-gray-500 text-xs">Cuenta de {bank.type} a nombre de SportGuru AI</span>
                    </div>
                  ))}
                </div>

                <div className="mt-6 p-3 bg-[#D4AF37]/10 border border-[#D4AF37]/20 rounded-lg flex gap-2">
                  <AlertCircle size={16} className="text-[#D4AF37] flex-shrink-0 mt-0.5" />
                  <p className="text-xs text-[#D4AF37]/90 leading-tight">
                    Luego de transferir, envíanos el comprobante vía WhatsApp al número de soporte para activar tu pick de forma inmediata.
                  </p>
                </div>
              </motion.div>
            )}

            {method === "crypto" && (
              <motion.div 
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                className="flex flex-col w-full"
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-bold text-white">Billeteras Crypto</h3>
                  <button onClick={() => setMethod("selector")} className="text-xs text-[#D4AF37] hover:underline">Volver</button>
                </div>
                
                <p className="text-xs text-gray-400 mb-4">
                  Transfiere exactamente <span className="text-white font-bold">$1.00 USD</span> a cualquiera de nuestras billeteras soportadas.
                </p>

                <div className="w-full space-y-3 max-h-[250px] overflow-y-auto pr-2 custom-scrollbar">
                  {cryptoWallets.map((wallet) => (
                    <div key={wallet.id} className="bg-[#1A1A1C] border border-white/10 rounded-xl p-3 flex flex-col gap-1 relative group hover:border-[#F7931A]/50 transition-colors">
                      <div className="flex items-center justify-between">
                        <span className="text-white font-bold text-sm">{wallet.name}</span>
                        <span className="bg-white/10 text-[10px] px-2 py-0.5 rounded text-gray-300">{wallet.network}</span>
                      </div>
                      <div className="flex items-center justify-between mt-1">
                        <span className="text-[#F7931A] font-mono text-sm truncate mr-4">{wallet.address}</span>
                        <button 
                          onClick={() => handleCopy(wallet.id, wallet.address)}
                          className="text-gray-400 hover:text-white transition-colors"
                          title="Copiar Address"
                        >
                          {copiedBank === wallet.id ? <CheckCircle2 size={16} className="text-[#22C55E]" /> : <Copy size={16} />}
                        </button>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="mt-6 p-3 bg-[#F7931A]/10 border border-[#F7931A]/20 rounded-lg flex gap-2">
                  <Bitcoin size={16} className="text-[#F7931A] flex-shrink-0 mt-0.5" />
                  <p className="text-xs text-[#F7931A]/90 leading-tight">
                    El procesamiento en Blockchain toma un par de minutos. Al transferir, el sistema validará tu Hash (TxID) y te liberará el Pick premium.
                  </p>
                </div>
              </motion.div>
            )}
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
