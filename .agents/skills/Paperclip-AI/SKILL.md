# 🦾 Paperclip AI: Agentic Business Orchestration

Paperclip AI es una plataforma de orquestación de agentes diseñada para ejecutar empresas autónomas mediante equipos de IA. Actúa como un "Capa de Gestión" (Org Chart) que coordina a múltiples agentes especializados para alcanzar objetivos compartidos.

## 🌟 Capacidades de la Habilidad
- **Orquestación de Equipos**: Define roles (CEO, Desarrollador, Marketing) y asigna tareas.
- **Integración con Claude Code**: Utiliza el potente CLI de Anthropic como el motor de ejecución técnica.
- **Gestión de Presupuestos**: Controla los costes de API estableciendo límites por agente o proyecto.
- **Audit Trails**: Mantiene un registro detallado de todas las acciones realizadas por los agentes.
- **Decomposición de Tareas**: Convierte una meta de alto nivel en tickets ejecutables.

## 🛠️ Cómo Inicializar Paperclip AI
Para activar el panel de control y el servidor local, ejecuta el siguiente comando en tu terminal:

```bash
npx paperclipai onboard --yes
```

> [!IMPORTANT]
> - Este comando configurará una base de datos PostgreSQL embebida y lanzará el servidor en `http://localhost:3100`.
> - Mantén la terminal abierta para que el servicio siga disponible.

## 🤝 Integración con Claude Code
Paperclip brilla cuando se conecta con **Claude Code**. Sigue estos pasos para configurar tu primer agente:

1. **Login de Claude**: Asegúrate de estar logueado en la terminal:
   ```bash
   claude login
   ```
2. **Dashboard**: Entra en `http://localhost:3100`.
3. **Hire Agent**: Elige el adaptador de **Claude Code**.
4. **Working Directory**: Define la carpeta de tu proyecto (ej: `MisProyectos/micheline-v2-beautera`).
5. **Approve & Run**: Revisa la estrategia propuesta por el Agente CEO y aprueba la ejecución.

## 🚀 Casos de Uso en MisProyectos
- **Desarrollo Autónomo**: "Finaliza la sección de precios de Micheline Nail Bar usando el sistema de diseño actual".
- **Marketing de Contenidos**: "Genera 5 variantes de anuncios para Instagram basados en el branding de Beautera".
- **Refactorización Masiva**: "Migra todos los estilos inline a componentes CSS modulares".

---
*Referencia: [Paperclip GitHub](https://github.com/paperclipai/paperclip) | [Claude Code GitHub](https://github.com/anthropics/claude-code)*
