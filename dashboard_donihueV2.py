import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image

# Paleta de colores consistente
COLOR_PALETTE = px.colors.qualitative.Set2

# Formato de pesos chilenos
def format_pesos(valor):
    return f"${valor:,.0f}"

# Función para cargar datos (incluyendo datos del PDF)
def load_data():
    data_sesiones = {
        "Tipo de Sesión": ["Ordinarias", "Extraordinarias", "Reuniones de Comisión"],
        "Cantidad": [36, 10, 10]
    }

    data_estudiantes = {
        "Establecimiento": ["Liceo Claudio Arrau León", "Liceo Claudio Arrau León EPJA", "Escuela Laura Matus Meléndez",
                            "Escuela de Párvulos Mis Primeros Pasos", "Colegio La Isla", "Escuela Lo Miranda", 
                            "Colegio República de Chile", "Colegio Cerrillos", "Colegio Julio Silva Lazo", 
                            "Colegio Plazuela", "Jardín Chamantitos", "Jardín Fantasia", 
                            "Jardín Maria Enriqueta Aros Guerrero"],
        "Hombres": [300, 31, 290, 40, 127, 168, 116, 37, 96, 125, 57, 18, 37],
        "Mujeres": [249, 24, 279, 27, 118, 150, 126, 32, 109, 101, 72, 26, 35],
        "Total": [549, 55, 569, 67, 245, 318, 242, 69, 205, 226, 129, 44, 72]
    }

    data_transporte_escolar = {
        "Línea": ["DAEM", "Licitación", "MINEDUC"],
        "Costo Anual (CLP)": [224550000, 205064550, 0],
        "Alumnos Transportados": [557, 444, 125]
    }

    data_mejoras_tecnologicas = {
        "Proyecto": ["Aula conectada Escuela Laura Matus", "Aula conectada Liceo Claudio Arrau", "Proyecto Wifi Colegios y Jardines",
                     "Aula conectada Escuela Lo Miranda", "Compra de computadores", "Compra Data Show", 
                     "Compra de computadores para áreas administrativas", "Proyecto CCTV Cámaras de Vigilancia"],
        "Presupuesto (CLP)": [12000000, 10000000, 32000000, 10000000, 55800000, 8550000, 26000000, 5800000]
    }

    data_proyectos_infraestructura = {
        "Proyecto": ["Implementación Aula Liceo Claudio Arrau León", "Mejoramiento Cubierta Biblioteca Pública", 
                     "Mejoramiento Infraestructura Colegio República de Chile", "Mejoramiento Infraestructura Escuela Lo Miranda",
                     "Diseño Reposición Parcial Colegio Julio Silva Lazo", "Conservación Colegio República de Chile", 
                     "1ra Etapa Mejoramiento Patio Cubierto Colegio La Isla"],
        "Monto (CLP)": [31840870, 20912751, 59723276, 17550266, 140000000, 449999349, 47261445],
        # Coordenadas para el mapa 3D
        "Latitud": [-34.2165, -34.2167, -34.2170, -34.2173, -34.2175, -34.2178, -34.2181],
        "Longitud": [-70.9633, -70.9640, -70.9647, -70.9653, -70.9660, -70.9667, -70.9674],
        "Elevación": [100, 150, 200, 250, 300, 350, 400]
    }

    data_ingresos_salud = {
        "Fuente": ["Aporte Per-cápita mensual", "Convenios de Salud", "Aporte Municipal", 
                   "Recuperación de Licencias Médicas 2023", "Recuperación de Licencias Médicas 2022", 
                   "Recuperación de Licencias Médicas 2021",
                   "Ingresos por servicios de urgencia y farmacia popular"],
        "Monto (CLP)": [4038000, 810000, 362000, 254000, 174000, 167000, 18000]
    }

    data_prodesal = {
        "Tipo de Ayuda": ["Subsidio para proyectos de inversión IFP", "Asignación bono insumos", "Beneficios proyectos de riego",
                          "Ayuda emergencia Agrícola (efectivo)", "Ayuda emergencia Agrícola (alimentos)"],
        "Monto Total (CLP)": [55499324, 33700000, 17500000, 42000000, 41696000]
    }

    data_reciclaje = {
        "Tipo de Residuo": ["Vidrio", "PET", "Aceite", "Domiciliario (Relleno Sanitario)"],
        "Cantidad (kg)": [104236, 63200, 2028, 7541300]
    }

    data_beneficios_sociales = {
        "Tipo de Beneficio": ["Entrega de agua potable", "Caja chica", "Informes Sociales", "Alimentos no perecibles", "Pañales", "Materiales de construcción"],
        "Monto Total (CLP)": [120000000, 50000000, 40000000, 60000000, 20000000, 20000000]
    }

    data_eventos_culturales = {
        "Evento": ["Noches de Verano", "Obras de Teatro al Aire Libre", "Ruta del Chacolí y el Aguardiente", "Celebración Día de la Madre", 
                   "Celebración Día del Niño", "Fiesta del Chacolí", "Aniversario de Lo Miranda"],
        "Asistentes": [1500, 800, 500, 1200, 900, 2000, 1000]
    }

    data_seguridad_publica = {
        "Tipo de Actividad": ["Operativos Tolerancia Cero", "Ferias de Seguridad", "Instalación de Cámaras", "Proyectos de Iluminación Peatonal"],
        "Cantidad": [10, 8, 174, 20]
    }

    data_usuarios_salud = {
        "Año": [2019, 2020, 2021, 2022, 2023],
        "Usuarios Inscritos": [20000, 21000, 22000, 24000, 24576]
    }

    data_presupuesto_municipal = {
        "Año": [2019, 2020, 2021, 2022, 2023],
        "Presupuesto Total (CLP)": [800000000, 850000000, 900000000, 950000000, 1000000000]
    }

    data_proyectos = {
        "Proyecto": ["Implementación Aula Liceo Claudio Arrau León", "Mejoramiento Cubierta Biblioteca Pública", 
                     "Mejoramiento Infraestructura Colegio República de Chile", "Mejoramiento Infraestructura Escuela Lo Miranda", 
                     "Diseño Reposición Parcial Colegio Julio Silva Lazo", "Conservación Colegio República de Chile", 
                     "Aula conectada Escuela Laura Matus", "Proyecto Wifi Colegios y Jardines", 
                     "Compra de Computadores", "Proyecto CCTV Cámaras de Vigilancia", "Recolección de Vidrio", 
                     "Ruta del Chacolí y el Aguardiente", "Pavimentación Calle Principal", "Renovación Alumbrado Público", 
                     "Construcción Centro Comunitario", "Reparación de Plazas", "Mejoramiento Redes de Agua", 
                     "Operativos Tolerancia Cero", "Instalación de Cámaras de Vigilancia", "Proyectos de Iluminación Peatonal", 
                     "Asistencia a Eventos Culturales", "Aula Conectada Escuela Lo Miranda", "Compra Data Show", 
                     "Compra de Computadores para Áreas Administrativas", "Implementación de Parques", "Proyectos de Riego PRODESAL", 
                     "Ayuda Emergencia Agrícola", "Subsidio para Proyectos de Inversión IFP", "Asignación Bono Insumos", 
                     "Beneficios Proyectos de Riego", "Ayuda Emergencia Agrícola (Alimentos)", "Proyectos de Reforestación", 
                     "Programa de Manejo de Residuos Sólidos", "Campañas de Concientización Ambiental", 
                     "Implementación de Energías Renovables", "Mejoramiento de Caminos Rurales", "Construcción de Centros de Salud", 
                     "Adquisición de Equipos Médicos", "Programas de Vacunación", "1ra Etapa Mejoramiento Patio Cubierto Colegio La Isla"],
        "Monto de Inversión (CLP)": [31840870, 20912751, 59723276, 17550266, 140000000, 449999349, 12000000, 32000000, 55800000, 
                                    5800000, 0, 0, 25000000, 18000000, 32000000, 15000000, 27000000, 0, 0, 0, 0, 10000000, 
                                    8550000, 26000000, 15000000, 17500000, 42000000, 55499324, 33700000, 17500000, 41696000, 
                                    30000000, 20000000, 10000000, 50000000, 20000000, 60000000, 25000000, 15000000, 47261445],
        "Área": ["Educación", "Cultura", "Educación", "Educación", "Educación", "Educación", "Educación", "Educación", "Educación", 
                 "Seguridad", "Medio Ambiente", "Cultura", "Infraestructura", "Infraestructura", "Infraestructura", "Infraestructura", 
                 "Infraestructura", "Seguridad", "Seguridad", "Seguridad", "Cultura", "Educación", "Educación", "Educación", 
                 "Infraestructura", "Medio Ambiente", "Medio Ambiente", "Desarrollo Local", "Desarrollo Local", "Desarrollo Local", 
                 "Desarrollo Local", "Medio Ambiente", "Medio Ambiente", "Medio Ambiente", "Medio Ambiente", "Infraestructura", 
                 "Salud", "Salud", "Salud", "Educación"],
        "Categoría": ["Infraestructura educativa", "Infraestructura cultural", "Infraestructura educativa", "Infraestructura educativa", 
                      "Infraestructura educativa", "Infraestructura educativa", "Tecnología educativa", "Tecnología educativa", 
                      "Tecnología educativa", "Seguridad pública", "Reciclaje", "Eventos culturales", "Infraestructura vial", 
                      "Infraestructura urbana", "Infraestructura social", "Infraestructura recreativa", "Infraestructura sanitaria", 
                      "Seguridad pública", "Seguridad pública", "Seguridad pública", "Eventos culturales", "Tecnología educativa", 
                      "Tecnología educativa", "Tecnología educativa", "Infraestructura recreativa", "Agricultura", "Agricultura", 
                      "Agricultura", "Agricultura", "Agricultura", "Agricultura", "Reforestación", "Gestión de residuos", 
                      "Educación ambiental", "Energías renovables", "Infraestructura vial", "Infraestructura sanitaria", 
                      "Equipamiento sanitario", "Salud pública", "Infraestructura educativa"]
    }

    data_asistencia_consejo_seguridad = {
        "Actor": ["Alcaldesa", "Secretaria Municipal", "Director Seguridad Pública", "Concejal", "Carabineros", 
                  "PDI", "Ministerio Público", "Gendarmería", "SPD", "SENAME", "SAG", "SENDA"],
        "Asistencia (%)": [100, 100, 75, 0, 100, 41.67, 8.33, 8.33, 91.60, 16.67, 91.67, 75]
    }

    data_gastos_municipales = {
        "Categoría": ["Gastos en Personal", "Servicios Básicos y Generales", "Aportes Sociales a la Comunidad", 
                      "Aportes Municipales a Deptos. de Educación y Salud", "Inversión Obras Civiles", 
                      "Inversión en Activos No Financieros", "Compensación Daños a Terceros", "Pasivos"],
        "Porcentaje (%)": [40, 26, 16, 9, 7, 1, 1, 0]
    }

    data_fomento_productivo = {
        "Indicador": ["Emprendimientos apoyados", "Capacitaciones realizadas", "Empresarios/as promovidos en Sabingo"],
        "Valor": [80, 10, 6]
    }

    data_oficina_vivienda = {
        "Proyecto": ["Cesión de terreno Rosa Zúñiga SN", "Cesión de terreno El Pedregal"],
        "Beneficiarios": ["Comité Doña Antonia", "Comité Los Padros y Club Deportivo La Isla"],
        "Superficie (m2)": [11100, 30000]
    }

    data_medio_ambiente = {
        "Programa": ["Reciclaje de PET", "Plantación de árboles nativos", "Plantación de árboles exóticos", "Operativo Tenencia Responsable"],
        "Cantidad": [63200, 228, 78, 300]
    }

    data_emergencias = {
        "Tipo de Ayuda": ["Fichas FIBE", "Personas afectadas", "Viviendas de emergencia", "Ayuda SENAPRED", 
                          "Servicio de albergue", "Trabajos correctivos en ribera del río"],
        "Cantidad": [525, 1383, 17, 82000000, 104, 970000000]
    }

    data_deporte = {
        "Taller": ["Escuela de Fútbol", "Crossfit", "Básquetbol", "Tenis de mesa", "Futsal", "Bochas", "Zumba"],
        "Inscritos": [200, 150, 80, 50, 120, 60, 250] 
    }

    data_inclusion_social = {
        "Actividad": ["Equinoterapia", "Rehabilitación integral niños", "Rehabilitación miembros organizaciones", "Capacitación a dirigentes"],
        "Participantes": [30, 50, 20, 15] 
    }

    # Crear los DataFrames
    df_sesiones = pd.DataFrame(data_sesiones)
    df_estudiantes = pd.DataFrame(data_estudiantes)
    df_transporte_escolar = pd.DataFrame(data_transporte_escolar)
    df_mejoras_tecnologicas = pd.DataFrame(data_mejoras_tecnologicas)
    df_proyectos_infraestructura = pd.DataFrame(data_proyectos_infraestructura)
    df_ingresos_salud = pd.DataFrame(data_ingresos_salud)
    df_prodesal = pd.DataFrame(data_prodesal)
    df_reciclaje = pd.DataFrame(data_reciclaje)
    df_beneficios_sociales = pd.DataFrame(data_beneficios_sociales)
    df_eventos_culturales = pd.DataFrame(data_eventos_culturales)
    df_seguridad_publica = pd.DataFrame(data_seguridad_publica)
    df_usuarios_salud = pd.DataFrame(data_usuarios_salud)
    df_presupuesto_municipal = pd.DataFrame(data_presupuesto_municipal)
    df_proyectos = pd.DataFrame(data_proyectos)
    df_asistencia_consejo_seguridad = pd.DataFrame(data_asistencia_consejo_seguridad)
    df_gastos_municipales = pd.DataFrame(data_gastos_municipales)
    df_fomento_productivo = pd.DataFrame(data_fomento_productivo)
    df_oficina_vivienda = pd.DataFrame(data_oficina_vivienda)
    df_medio_ambiente = pd.DataFrame(data_medio_ambiente)
    df_emergencias = pd.DataFrame(data_emergencias)
    df_deporte = pd.DataFrame(data_deporte)
    df_inclusion_social = pd.DataFrame(data_inclusion_social)

    # Agregar coordenadas al DataFrame df_proyectos
    df_proyectos["Latitud"] = [-34.2165, -34.2167, -34.2170, -34.2173, -34.2175, -34.2178, -34.2181] + [-34.2] * (len(df_proyectos) - 7)
    df_proyectos["Longitud"] = [-70.9633, -70.9640, -70.9647, -70.9653, -70.9660, -70.9667, -70.9674] + [-70.95] * (len(df_proyectos) - 7)
    df_proyectos["Elevación"] = [100, 150, 200, 250, 300, 350, 400] + [120] * (len(df_proyectos) - 7)

    # Datos para los KPI (Extraer del PDF)
    data_kpi = {
        "Usuarios de Salud": 24576,
        "Inversión en Educación": df_proyectos[df_proyectos["Área"]=="Educación"]["Monto de Inversión (CLP)"].sum(),
        "Residuos Reciclados": df_reciclaje["Cantidad (kg)"].sum(),
        "Asistentes a Eventos": df_eventos_culturales["Asistentes"].sum(),
        "Cámaras de Vigilancia": 233,
        "Presupuesto Municipal": df_presupuesto_municipal["Presupuesto Total (CLP)"].iloc[-1]
    }
    df_kpi = pd.DataFrame(data_kpi, index=[0])

    return {
        "sesiones": df_sesiones,
        "estudiantes": df_estudiantes,
        "transporte_escolar": df_transporte_escolar,
        "mejoras_tecnologicas": df_mejoras_tecnologicas,
        "proyectos_infraestructura": df_proyectos_infraestructura,
        "ingresos_salud": df_ingresos_salud,
        "prodesal": df_prodesal,
        "reciclaje": df_reciclaje,
        "beneficios_sociales": df_beneficios_sociales,
        "eventos_culturales": df_eventos_culturales,
        "seguridad_publica": df_seguridad_publica,
        "usuarios_salud": df_usuarios_salud,
        "presupuesto_municipal": df_presupuesto_municipal,
        "proyectos": df_proyectos,
        "asistencia_consejo_seguridad": df_asistencia_consejo_seguridad,
        "gastos_municipales": df_gastos_municipales,
        "fomento_productivo": df_fomento_productivo,
        "oficina_vivienda": df_oficina_vivienda,
        "medio_ambiente": df_medio_ambiente,
        "emergencias": df_emergencias,
        "deporte": df_deporte,
        "inclusion_social": df_inclusion_social,
        "kpi": df_kpi
    }

# Cargar datos al iniciar la aplicación
data = load_data()

# Configuración de la página
st.set_page_config(
    page_title="Avances de Doñihue 2023",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal y logo
st.title("Avances de Doñihue 2023: Un Año de Tradición y Progreso")
logo_muni = Image.open("Logo_Doñihue.png") # Reemplaza con la ruta correcta
st.sidebar.image(logo_muni, width=150)

# Sidebar para la navegación
st.sidebar.title("Navegación")
seccion = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "Inicio",
        "Concejo Municipal",
        "Educación",
        "Transporte Escolar",
        "Mejoras Tecnológicas",
        "Infraestructura Educativa",
        "Salud",
        "PRODESAL",
        "Reciclaje",
        "Beneficios Sociales",
        "Eventos Culturales",
        "Seguridad",
        "Evolución de Usuarios de Salud",
        "Presupuesto Municipal",
        "Proyectos",
        "Auditorías 2023",
        "Sumarios",
        "Juicios",
        "Convenios",
        "DIDECO",
        "Equipo de Operaciones", # Asegúrate de tener datos para esta sección
        "Plan de Inversiones en Infraestructura", # Asegúrate de tener datos para esta sección
        "Complejo El Tabo"  # Asegúrate de tener datos para esta sección
    ]
)

# Contenido dinámico según la sección seleccionada
if seccion == "Inicio":
    st.write("""
    Este dashboard interactivo presenta los logros y avances del municipio
    de Doñihue durante el año 2023. Utiliza el menú de la izquierda para
    navegar entre las diferentes secciones y explorar los datos detallados.
    """)

    # Mostrar los KPI en tarjetas
    st.subheader("Resumen de Avances 2023")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Usuarios de Salud", f"{data['kpi']['Usuarios de Salud'].iloc[0]:,.0f}")
    with col2:
        st.metric("Inversión en Educación", format_pesos(data['kpi']['Inversión en Educación'].iloc[0]))
    with col3:
        st.metric("Residuos Reciclados (kg)", f"{data['kpi']['Residuos Reciclados'].iloc[0]:,.0f}")
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric("Asistentes a Eventos Culturales", f"{data['kpi']['Asistentes a Eventos'].iloc[0]:,.0f}")
    with col5:
        st.metric("Cámaras de Vigilancia", data['kpi']['Cámaras de Vigilancia'].iloc[0])
    with col6:
        st.metric("Presupuesto Municipal", format_pesos(data['kpi']['Presupuesto Municipal'].iloc[0]))

elif seccion == "Concejo Municipal":
    st.header("Concejo Municipal: Liderazgo y Toma de Decisiones")
    st.write("""
    El Honorable Concejo Municipal, liderado por la Alcaldesa Pabla Ponce
    Valle, ha trabajado arduamente durante el 2023 para impulsar el
    progreso de Doñihue. A través de sesiones ordinarias, extraordinarias
    y reuniones de comisión, se han tomado decisiones cruciales para el
    bienestar de nuestra comunidad.
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Sesiones Ordinarias", "36")
    with col2:
        st.metric("Sesiones Extraordinarias", "10")
    with col3:
        st.metric("Reuniones de Comisión", "10")

    st.write("""
    Además, se han confeccionado 163 acuerdos de Concejo Municipal,
    3.393 decretos alcaldicios otorgados y 4.490 decretos alcaldicios
    SIAPER otorgados, lo que demuestra el compromiso con la gestión
    transparente y eficiente.
    """)

elif seccion == "Educación":
    st.header("Educación: Formando el Futuro de Doñihue")
    st.write("""
    La educación es una prioridad para Doñihue. El DAEM cuenta con 12
    establecimientos, donde trabajan aproximadamente 500 profesionales
    dedicados a la formación de nuestros niños, niñas y jóvenes.
    """)

    # Mostrar la distribución de estudiantes por género
    # con un gráfico de barras agrupadas
    fig = px.bar(
        data["estudiantes"],
        x="Establecimiento",
        y=["Hombres", "Mujeres"],
        title="Distribución de Estudiantes por Establecimiento",
        barmode='group',
        color_discrete_sequence=COLOR_PALETTE,
        labels={"value":"Cantidad de Estudiantes"}
    )
    fig.update_layout(xaxis_title="Establecimientos Educacionales")
    st.plotly_chart(fig)

    st.write(f"""
    En el 2023, el universo total de estudiantes fue de
    **{data["estudiantes"]["Total"].sum():,.0f}**,
    distribuidos en los diferentes establecimientos de la comuna.
    Además, JUNAEB entregó un total de **{1937:,.0f} raciones**
    para asegurar la alimentación de nuestros estudiantes.
    """)

elif seccion == "Transporte Escolar":
    st.header("Transporte Escolar: Acercando la Educación a Todos")
    st.write(f"""
    El transporte escolar es fundamental para asegurar el acceso a la educación, 
    especialmente en una comuna con la geografía de Doñihue. Durante el 2023, 
    se transportaron **{data["transporte_escolar"]["Alumnos Transportados"].sum():,.0f} estudiantes**, 
    garantizando que la distancia no sea un impedimento para su desarrollo educativo.
    """)

    fig = px.bar(
        data["transporte_escolar"],
        x="Línea",
        y=["Alumnos Transportados", "Costo Anual (CLP)"],
        title="Transporte Escolar 2023",
        barmode='group',
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(xaxis_title="", yaxis_title="")
    fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    st.plotly_chart(fig)

    st.write("""
    El gráfico muestra la cantidad de alumnos transportados y el costo anual
    para cada línea de transporte escolar. 
    """)

elif seccion == "Mejoras Tecnológicas":
    st.header("Mejoras Tecnológicas: Preparando a Doñihue para el Futuro Digital")
    st.write(f"""
    En la era digital, el acceso a la tecnología es indispensable para una 
    educación de calidad. Durante el 2023, se realizaron importantes inversiones 
    en mejoras tecnológicas para nuestros establecimientos educativos, con un 
    presupuesto total de {format_pesos(data["mejoras_tecnologicas"]["Presupuesto (CLP)"].sum())}.
    """)

    fig = px.pie(
        data["mejoras_tecnologicas"],
        values="Presupuesto (CLP)",
        names="Proyecto",
        title="Distribución del Presupuesto en Mejoras Tecnológicas",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig)

    st.write("""
    El gráfico muestra la distribución del presupuesto en diferentes
    proyectos de mejoras tecnológicas.
    """)

elif seccion == "Infraestructura Educativa":
    st.header("Infraestructura Educativa: Construyendo Espacios para el Aprendizaje")
    st.write(f"""
    Una infraestructura adecuada es fundamental para el desarrollo de una 
    educación de calidad. Durante el 2023, se ejecutaron diversos proyectos 
    de infraestructura en los establecimientos educativos de Doñihue, con una 
    inversión total de **{format_pesos(data["proyectos_infraestructura"]["Monto (CLP)"].sum())}**.
    """)

    # Mostrar el monto de inversión por proyecto en un gráfico de barras
    fig = px.bar(
        data["proyectos_infraestructura"],
        x="Proyecto",
        y="Monto (CLP)",
        title="Proyectos de Infraestructura 2023",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(xaxis_title="", yaxis_title="Monto (CLP)")
    fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    st.plotly_chart(fig)

    # Mapa de Doñihue con la ubicación aproximada de los proyectos
    st.subheader("Ubicación Aproximada de los Proyectos")
    st.write("""
    Los marcadores en el mapa indican la ubicación aproximada de los proyectos
    de infraestructura educativa en la comuna de Doñihue. 
    """)

    # URL de un mapa de Doñihue (reemplazar con un mapa real)
    mapa_url = "https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3328.809334722628!2d-70.96627708425823!3d-34.21435048059632!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x966383e0a867398d%3A0x897d4e403c83639b!2sDo%C3%B1ihue%2C%20Regi%C3%B3n%20del%20Libertador%20Gral.%20Bernardo%20O%27Higgins!5e0!3m2!1ses-419!2scl!4v1681288029941!5m2!1ses-419!2scl"
    st.components.v1.iframe(mapa_url, width=700, height=500)
elif seccion == "Salud":
    st.header("Salud: Cuidando el Bienestar de Nuestra Comunidad")

    st.write(f"""
    El acceso a la salud es un derecho fundamental, y en Doñihue trabajamos 
    para garantizarlo a todos los vecinos. Durante el 2023, se realizaron 
    **{103579:,.0f} prestaciones de salud** en los CESFAM de Doñihue y 
    Lo Miranda, lo que refleja el compromiso con la atención médica de calidad.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Ingresos al Servicio de Salud 2023")
        fig = px.pie(
            data["ingresos_salud"],
            values="Monto (CLP)",
            names="Fuente",
            title="Distribución de Ingresos al Servicio de Salud 2023",
            color_discrete_sequence=COLOR_PALETTE,
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)

        st.write("""
        El aporte per-cápita mensual y los convenios de salud representan las
        principales fuentes de ingreso al sistema de salud comunal.
        """)

    with col2:
        st.subheader("Gastos en Salud 2023")
        data_gastos_salud = {
            "Categoría": [
                "Personal",
                "Equipamiento",
                "Medicamentos",
                "Mantenimiento",
                "Programas de Salud",
            ],
            "Monto (CLP)": [12000000, 8000000, 5000000, 3000000, 7000000],
        }
        df_gastos_salud = pd.DataFrame(data_gastos_salud)
        fig = px.pie(
            df_gastos_salud,
            values="Monto (CLP)",
            names="Categoría",
            title="Distribución de Gastos en Salud 2023",
            color_discrete_sequence=COLOR_PALETTE,
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)

        st.write("""
        Los gastos en personal y equipamiento médico representan la mayor parte
        del presupuesto de salud, lo que refleja la importancia de contar con
        profesionales capacitados y tecnología de punta para brindar una
        atención de calidad.
        """)

    st.write(f"""
    Se destaca la atención a **{24576:,.0f} usuarios inscritos en el sistema
    de salud comunal**, con un aumento de **{614:,.0f} usuarios** en el 2023.
    El compromiso con la salud se refleja en la inversión en
    **equipamiento médico por un total de {format_pesos(519000000)}**,
    mejorando la calidad de atención para nuestros vecinos.
    """)


elif seccion == "PRODESAL":
    st.header("PRODESAL: Impulsando el Desarrollo Rural")
    st.write(f"""
    El Programa de Desarrollo de Acción Local (PRODESAL) tiene como objetivo 
    principal mejorar los ingresos de los microproductores silvoagropecuarios 
    de nuestra comuna. Durante el 2023, se brindó apoyo a **260 usuarios** 
    a través de asesoría técnica, fondos de operación anual e inversiones en 
    activos productivos.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Aportes Monetarios al Convenio INDAP - Municipalidad")
        fig = px.bar(
            pd.DataFrame({
                "Entidad": ["INDAP", "Municipalidad"],
                "Aporte (CLP)": [82571880, 14000000]
            }),
            x="Entidad",
            y="Aporte (CLP)",
            color="Entidad",
            title="Aportes al Programa PRODESAL 2023",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(xaxis_title="", yaxis_title="Aporte (CLP)")
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig)

        st.write("""
        El programa PRODESAL se financia a través de un convenio entre 
        INDAP y la Municipalidad.
        """)

    with col2:
        st.subheader("Proyectos de Inversión Ejecutados")
        fig = px.bar(
            data["prodesal"],
            x="Tipo de Ayuda",
            y="Monto Total (CLP)",
            title="Inversión en Proyectos PRODESAL 2023",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(xaxis_title="", yaxis_title="Monto Total (CLP)")
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig)

        st.write("""
        Se han ejecutado diversos proyectos de inversión para apoyar a los
        microproductores de la comuna.
        """)

    st.write(f"""
    Se destaca la inversión de **{format_pesos(55499324)} en subsidios 
    para proyectos de inversión**, beneficiando a 39 usuarios. Además, 
    se entregaron **bonos de insumos por un total de 
    {format_pesos(33700000)}** a 220 usuarios, y se implementaron 
    proyectos de riego que mejoran la productividad agrícola.
    """)

elif seccion == "Reciclaje":
    st.header("Reciclaje: Comprometidos con el Medio Ambiente")
    st.write(f"""
    En Doñihue estamos comprometidos con la gestión responsable de los 
    residuos. Durante el 2023, se recolectaron 
    **{data["reciclaje"]["Cantidad (kg)"].sum():,.0f} kg de residuos**, 
    incluyendo vidrio, PET, aceite y residuos domiciliarios.
    """)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            data["reciclaje"],
            x="Tipo de Residuo",
            y="Cantidad (kg)",
            title="Cantidad de Residuos Recogidos por Tipo",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(xaxis_title="", yaxis_title="Cantidad (kg)")
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig)

    with col2:
        st.write(f"""
        El convenio con la empresa Green Planet Spa para el reciclaje de 
        PET ha sido fundamental, permitiendo recolectar **{63200:,.0f} kg 
        de PET**, un aumento del 88% respecto al año anterior. Seguimos 
        trabajando para ampliar la cobertura de nuestros programas de 
        reciclaje y promover la conciencia ambiental en la comunidad.
        """)

elif seccion == "Beneficios Sociales":
    st.header("Beneficios Sociales: Apoyando a Quienes Más lo Necesitan")
    st.write(f"""
    A través de la Dirección de Desarrollo Comunitario (DIDECO), la 
    Municipalidad de Doñihue brinda apoyo a las familias más vulnerables 
    de la comuna. Durante el 2023, se entregaron beneficios sociales 
    por un total de 
    **{format_pesos(data["beneficios_sociales"]["Monto Total (CLP)"].sum())}**, 
    impactando positivamente en la calidad de vida de nuestros vecinos.
    """)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            data["beneficios_sociales"],
            x="Tipo de Beneficio",
            y="Monto Total (CLP)",
            title="Distribución de Beneficios Sociales 2023",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(xaxis_title="", yaxis_title="Monto Total (CLP)")
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig)

    with col2:
        st.write("""
        Los beneficios incluyeron la entrega de agua potable, apoyo 
        económico a través de la caja chica, realización de informes 
        sociales, entrega de alimentos no perecibles, pañales y 
        materiales de construcción. Estas acciones demuestran el 
        compromiso de la Municipalidad con el bienestar de las 
        familias que más lo necesitan.
        """)

elif seccion == "Eventos Culturales":
    st.header("Eventos Culturales: Celebrando Nuestra Identidad")
    st.write("""
    Doñihue es una comuna rica en cultura y tradiciones. Durante el 
    2023, se llevaron a cabo diversos eventos culturales que congregaron 
    a miles de vecinos y visitantes, promoviendo el arte, la música, 
    el folclor y la identidad local.
    """)

    col1, col2 = st.columns(2)

    with col1:
        fig = px.bar(
            data["eventos_culturales"],
            x="Evento",
            y="Asistentes",
            title="Asistencia a Eventos Culturales 2023",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(xaxis_title="Eventos", yaxis_title="Cantidad de Asistentes")
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig)

    with col2:
        # Mapa de Calor de Asistencias a Eventos Culturales (Interactivo)
        st.subheader("Mapa de Calor de Asistencias a Eventos Culturales")

        # Datos para el mapa de calor (deben ser reales)
        eventos = data["eventos_culturales"]["Evento"].tolist()
        meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        # Crear un DataFrame con los datos del mapa de calor
        df_heatmap = pd.DataFrame(index=eventos, columns=meses)

        # Reemplazar con datos reales de asistencia por evento y mes
        # Ejemplo:
        df_heatmap.loc["Noches de Verano", "Enero"] = 1200
        # ... Agregar datos para los demás eventos y meses ...

        fig = go.Figure(data=go.Heatmap(
            z=df_heatmap.values,
            x=meses,
            y=eventos,
            colorscale='Viridis'
        ))
        fig.update_layout(
            title="Mapa de Calor de Asistencias a Eventos Culturales",
            xaxis_title="Mes",
            yaxis_title="Evento"
        )
        st.plotly_chart(fig)
        st.write("Mapa que muestra la asistencia a los eventos durante el año.")

elif seccion == "Seguridad":
    st.header("Seguridad: Trabajando por una Comuna Más Tranquila")
    st.write("""
    La seguridad es una prioridad para la Municipalidad de Doñihue. 
    Durante el 2023, se implementaron diversas acciones para fortalecer 
    la seguridad pública, con un enfoque preventivo y de participación ciudadana.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("Actividades de Seguridad Pública")
        fig = px.bar(
            data["seguridad_publica"],
            x="Tipo de Actividad",
            y="Cantidad",
            title="Actividades de Seguridad Pública 2023",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(xaxis_title="", yaxis_title="Cantidad")
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig)

    with col2:
        st.subheader("Proyectos de Seguridad")
        data_proyectos_seguridad = {
            "Proyecto": ["Instalación de Cámaras", "Operativos de Seguridad",
                         "Campañas de Concientización", "Mejoras en Iluminación"],
            "Cantidad": [174, 50, 30, 20]
        }
        df_proyectos_seguridad = pd.DataFrame(data_proyectos_seguridad)
        fig = px.bar(
            df_proyectos_seguridad,
            x="Proyecto",
            y="Cantidad",
            title="Proyectos de Seguridad 2023",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(xaxis_title="", yaxis_title="Cantidad")
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig)

    with col3:
        st.subheader("Asistencia a Consejos de Seguridad Pública")
        fig = px.bar(
            data["asistencia_consejo_seguridad"],
            x="Actor",
            y="Asistencia (%)",
            title="Asistencia al Consejo de Seguridad 2023",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(xaxis_title="", yaxis_title="Asistencia (%)")
        fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
        st.plotly_chart(fig)

    st.write("""
    Se realizaron **10 operativos Tolerancia Cero, 8 ferias de seguridad 
    y se instalaron 174 nuevas cámaras de vigilancia**, fortaleciendo 
    la red de seguridad en la comuna. La participación ciudadana es 
    fundamental en la construcción de una comuna más segura, y la 
    asistencia al Consejo Comunal de Seguridad Pública es un claro 
    ejemplo de ello.
    """)

elif seccion == "Evolución de Usuarios de Salud":
    st.header("Evolución de Usuarios de Salud: Un Sistema en Crecimiento")
    st.write("""
    El sistema de salud comunal ha experimentado un crecimiento constante 
    en los últimos años, lo que refleja la confianza de la comunidad en 
    nuestros servicios de salud.
    """)

    fig = px.line(
        data["usuarios_salud"],
        x="Año",
        y="Usuarios Inscritos",
        title="Evolución de Usuarios Inscritos en el Sistema de Salud Comunal",
        markers=True,
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(xaxis_title="Año", yaxis_title="Usuarios Inscritos")
    fig.update_traces(texttemplate='%{y:,.0f}', textposition='top center')
    st.plotly_chart(fig)

    st.write("""
    El gráfico muestra el aumento constante de usuarios inscritos en el 
    sistema de salud comunal desde el 2019 hasta el 2023. Este 
    crecimiento demuestra la importancia de seguir invirtiendo en 
    salud para asegurar la atención médica de calidad a todos nuestros vecinos.
    """)

elif seccion == "Presupuesto Municipal":
    st.header("Presupuesto Municipal: Gestionando los Recursos con Responsabilidad")
    st.write("""
    La Municipalidad de Doñihue gestiona los recursos con responsabilidad 
    y transparencia, destinándolos a las áreas prioritarias para el 
    desarrollo de la comuna.
    """)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Evolución del Presupuesto Total")
        fig = px.area(
            data["presupuesto_municipal"],
            x="Año",
            y="Presupuesto Total (CLP)",
            title="Evolución del Presupuesto Total de la Municipalidad",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(xaxis_title="Año", yaxis_title="Presupuesto Total (CLP)")
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='top center')
        st.plotly_chart(fig)

    with col2:
        st.subheader("Distribución del Presupuesto por Áreas 2023")
        presupuesto_areas = {
            "Área": ["Salud", "Educación", "Infraestructura", "Seguridad", "Cultura"],
            "Presupuesto (CLP)": [1000000000, 800000000, 600000000, 400000000, 200000000]
        }
        df_presupuesto_areas = pd.DataFrame(presupuesto_areas)
        fig = px.pie(
            df_presupuesto_areas,
            values="Presupuesto (CLP)",
            names="Área",
            title="Distribución del Presupuesto por Áreas 2023",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)

    # Gráfico de Gastos Municipales
    st.subheader("Gastos Municipales 2023")
    fig = px.bar(
        data["gastos_municipales"],
        x="Categoría",
        y="Porcentaje (%)",
        title="Distribución de los Gastos Municipales 2023",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(xaxis_title="Categorias", yaxis_title="Porcentaje (%)")
    fig.update_traces(texttemplate='%{y:.2f}%', textposition='outside')
    st.plotly_chart(fig)

    st.write("""
    El gráfico de evolución del presupuesto total muestra un incremento 
    sostenido en los últimos años, lo que ha permitido realizar 
    importantes inversiones en las áreas prioritarias para la comuna. 
    La distribución del presupuesto por áreas en el 2023 refleja la 
    importancia que se le da a la salud, la educación, la 
    infraestructura, la seguridad y la cultura.
    """)

elif seccion == "Proyectos":
    st.header("Proyectos: Construyendo el Futuro de Doñihue")
    st.write("""
    La Municipalidad de Doñihue ha desarrollado una importante cartera 
    de proyectos durante el 2023, con el objetivo de mejorar la calidad 
    de vida de los vecinos y fortalecer el desarrollo de la comuna.
    """)

    # Filtros por Área y Categoría
    selected_area = st.selectbox("Filtrar por Área:", ["Todos"] + data["proyectos"]["Área"].unique().tolist())
    selected_category = st.selectbox("Filtrar por Categoría:", ["Todos"] + data["proyectos"]["Categoría"].unique().tolist())

    # Aplicar filtros al DataFrame
    filtered_proyectos = data["proyectos"]
    if selected_area != "Todos":
        filtered_proyectos = filtered_proyectos[filtered_proyectos["Área"] == selected_area]
    if selected_category != "Todos":
        filtered_proyectos = filtered_proyectos[filtered_proyectos["Categoría"] == selected_category]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Listado de Proyectos 2023")
        fig = px.bar(
            filtered_proyectos,
            x="Proyecto",
            y="Monto de Inversión (CLP)",
            color="Área",
            title="Monto de Inversión por Proyecto",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_layout(xaxis_title="", yaxis_title="Monto de Inversión (CLP)")
        fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
        st.plotly_chart(fig)

    with col2:
        st.subheader("Distribución del Monto de Inversión por Área")
        fig = px.pie(
            filtered_proyectos,
            values="Monto de Inversión (CLP)",
            names="Área",
            title="Distribución del Monto de Inversión por Área",
            color_discrete_sequence=COLOR_PALETTE
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)

    # Mapa de Calor del Monto de Inversión por Área y Categoría (Interactivo)
    st.subheader("Mapa de Calor del Monto de Inversión por Área y Categoría")
    st.write("""
    Explore el monto de inversión en proyectos por área y categoría en el mapa de calor interactivo.
    """)

    heatmap_data = pd.pivot_table(
        filtered_proyectos,
        values="Monto de Inversión (CLP)",
        index="Área",
        columns="Categoría",
        aggfunc=np.sum,
        fill_value=0
    )
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        colorscale='Viridis'
    ))
    fig.update_layout(
        title="Mapa de Calor del Monto de Inversión por Área y Categoría",
        xaxis_title="Categoría",
        yaxis_title="Área"
    )
    st.plotly_chart(fig)

    # Mapa 3D de Proyectos
    st.subheader("Mapa 3D de Proyectos")
    st.write("""
    Explore la ubicación de los proyectos en el mapa 3D interactivo.
    """)
    fig = px.scatter_3d(
        filtered_proyectos,
        x='Latitud',
        y='Longitud',
        z='Elevación',
        color='Área',
        title='Mapa 3D de Proyectos',
        hover_data=["Proyecto"],
        color_discrete_sequence=COLOR_PALETTE
    )
    st.plotly_chart(fig)

elif seccion == "Auditorías 2023":
    st.header("Auditorías 2023: Transparencia y Mejora Continua")
    st.write("""
    La Municipalidad de Doñihue se somete a auditorías internas y 
    externas para asegurar la transparencia en la gestión de los recursos 
    y la mejora continua de sus procesos.
    """)

    st.write("""
    Durante el 2023, se realizaron **cuatro auditorías internas**, 
    que se enfocaron en:

    * Gestión del programa FAEP en el Departamento de Educación Municipal.
    * Ingresos y gastos de los programas de imágenes diagnósticas y 
    odontología integral en el DESAM Doñihue.
    * Control de vehículos municipales.

    Además, la Contraloría General de la República (CGR) realizó 
    una **auditoría externa**, emitiendo el informe N°25/2023, 
    que identificó algunos hallazgos relacionados con la gestión municipal.
    """)

    st.write("""
    La Municipalidad ha tomado medidas para corregir las observaciones 
    señaladas en las auditorías y fortalecer sus procesos de control 
    interno. La transparencia y la rendición de cuentas son fundamentales 
    para una gestión municipal eficiente y responsable.
    """)

elif seccion == "Sumarios":
    st.header("Sumarios: Velando por el Correcto Funcionamiento de la Municipalidad")
    st.write("""
    La Municipalidad de Doñihue realiza investigaciones sumarias y 
    sumarios administrativos para asegurar el correcto funcionamiento 
    de la institución y el cumplimiento de la normativa vigente.
    """)

    st.write("""
    Durante el 2023, se instruyó la realización de 
    **19 sumarios e investigaciones sumarias**, de las cuales 2 se 
    elevaron a sumario administrativo. La mayoría de estas 
    investigaciones fueron ordenadas por la Contraloría General de 
    la República (CGR) como resultado del Informe Final N°25/2023.
    """)

    st.write("""
    La Municipalidad se toma muy en serio cualquier irregularidad 
    en su funcionamiento y actúa con diligencia para investigar 
    y sancionar las faltas que se detecten.
    """)

elif seccion == "Juicios":
    st.header("Juicios: Defendiendo los Intereses de la Municipalidad")
    st.write("""
    La Municipalidad de Doñihue cuenta con un equipo legal que se 
    encarga de defender los intereses de la institución en los diferentes 
    juicios que se presentan.
    """)

    st.write("""
    Durante el 2023, se llevaron a cabo diversos juicios, principalmente 
    en el ámbito laboral. En aquellos casos que han concluido por 
    conciliación o avenimiento, se ha logrado un acuerdo entre las 
    partes por menos del 50% de lo solicitado inicialmente.
    """)

    st.write("""
    Se destaca la sentencia favorable obtenida en la causa Rol N° 
    T-25-2022, donde se rechazó totalmente la demanda del ex director 
    de SECPLAC por más de $40 millones de pesos.
    """)

elif seccion == "Convenios":
    st.header("Convenios: Fortaleciendo las Alianzas para el Desarrollo")
    st.write("""
    La Municipalidad de Doñihue establece convenios de colaboración 
    con diversas instituciones públicas y privadas para fortalecer las 
    acciones que se realizan en beneficio de la comunidad.
    """)

    st.write("""
    Durante el 2023, se celebraron **37 convenios**, destacando los siguientes:

    * Convenio de transferencia de recursos para la Oficina Local de la Niñez.
    * Convenio con el Gobierno Regional de O'Higgins para el proyecto 
    "Deporte en Tu Barrio".
    * Convenio con el Gobierno Regional de O'Higgins para el programa 
    "Red Local de Apoyos y Cuidados - SNAC".
    * Convenios con los municipios de Mostazal y Las Condes.
    """)

    st.write("""
    Estos convenios permiten a la Municipalidad acceder a recursos, 
    conocimientos y experiencias que enriquecen la gestión municipal y 
    amplían las oportunidades para los vecinos de Doñihue.
    """)

elif seccion == "DIDECO":
    st.header("DIDECO: Impulsando el Desarrollo Comunitario")
    st.write("""
    La Dirección de Desarrollo Comunitario (DIDECO) juega un rol 
    fundamental en la Municipalidad de Doñihue, impulsando el 
    desarrollo social, cultural y económico de la comuna.
    """)

    st.write(f"""
    Durante el 2023, DIDECO trabajó con 65 organizaciones territoriales 
    y 294 organizaciones funcionales, otorgando un total de 
    **{format_pesos(26053987)}** en fondos de desarrollo vecinal 
    (FONDEVE) y **{format_pesos(197964648)}** en subvenciones.
    """)

    st.subheader("Principales Programas de DIDECO")

    # Fomento Productivo
    st.markdown("**Fomento Productivo:**")
    st.write("""
    DIDECO apoya a los emprendedores y microempresarios de Doñihue a 
    través de capacitaciones, asistencia técnica y vinculación con el 
    ecosistema regional de emprendimiento.
    """)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Emprendimientos apoyados", data["fomento_productivo"]["Valor"][0])
    with col2:
        st.metric("Capacitaciones realizadas", data["fomento_productivo"]["Valor"][1])
    with col3:
        st.metric("Empresarios/as promovidos en Sabingo", data["fomento_productivo"]["Valor"][2])

    st.write(f"""
    Se destaca la promoción de empresarios y empresarias de Doñihue en 
    el programa Sabingo de Chilevisión, con una valorización estimada 
    de **{format_pesos(400000000)}**.
    """)

    # Oficina de Vivienda
    st.markdown("**Oficina de Vivienda:**")
    st.write("""
    La Oficina de Vivienda promueve y proyecta soluciones habitacionales 
    para los vecinos de Doñihue.
    """)

    fig = go.Figure(data=[go.Table(
        header=dict(values=list(data["oficina_vivienda"].columns),
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[data["oficina_vivienda"]["Proyecto"],
                           data["oficina_vivienda"]["Beneficiarios"],
                           data["oficina_vivienda"]["Superficie (m2)"]],
                   fill_color='lavender',
                   align='left'))
    ])
    st.plotly_chart(fig)

    st.write("""
    Se destaca la cesión de terrenos para proyectos habitacionales, 
    como el terreno ubicado en Rosa Zúñiga SN para el Comité Doña 
    Antonia y el terreno El Pedregal para el Comité Los Padros y el 
    Club Deportivo La Isla.
    """)

    # Medio Ambiente
    st.markdown("**Medio Ambiente:**")
    st.write("""
    La Unidad de Medio Ambiente promueve la protección del entorno 
    natural y la gestión responsable de los residuos.
    """)

    fig = px.bar(
        data["medio_ambiente"],
        x="Programa",
        y="Cantidad",
        title="Programas de Medio Ambiente 2023",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(xaxis_title="", yaxis_title="Cantidad")
    st.plotly_chart(fig)

    st.write("""
    Se destaca el convenio de reciclaje de PET con la empresa Green 
    Planet Spa, la plantación de árboles nativos y exóticos en la 
    comuna, y el operativo de tenencia responsable de mascotas.
    """)

    # Emergencias y Desastres
    st.markdown("**Emergencias y Desastres:**")
    st.write("""
    La Municipalidad de Doñihue cuenta con un equipo de emergencia 
    preparado para atender las situaciones de riesgo que puedan 
    afectar a la comunidad.
    """)

    fig = px.bar(
        data["emergencias"],
        x="Tipo de Ayuda",
        y="Cantidad",
        title="Atención a Emergencias y Desastres 2023",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(xaxis_title="", yaxis_title="Cantidad")
    fig.update_traces(texttemplate='%{y:,.0f}', textposition='outside')
    st.plotly_chart(fig)

    st.write(f"""
    Durante el 2023, se atendieron a 1.383 personas afectadas por 
    emergencias, se entregaron 17 viviendas de emergencia y se 
    gestionaron recursos por **{format_pesos(82000000)} del SENAPRED**. 
    Se invirtieron **{format_pesos(970000000)}** en trabajos 
    correctivos en la ribera del río Cachapoal para proteger a la 
    comunidad de futuras inundaciones.
    """)

    # Deporte
    st.markdown("**Deporte:**")
    st.write("""
    La Oficina de Deportes promueve la actividad física y los 
    hábitos de vida saludable a través de talleres deportivos 
    para todas las edades.
    """)

    fig = px.bar(
        data["deporte"],
        x="Taller",
        y="Inscritos",
        title="Talleres Deportivos 2023",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(xaxis_title="Talleres", yaxis_title="Cantidad de Inscritos")
    st.plotly_chart(fig)

    st.write("""
    Se realizaron talleres de fútbol, crossfit, básquetbol, tenis de 
    mesa, futsal, bochas y zumba, beneficiando a un gran número de vecinos.
    """)

    # Oficina de Inclusión Social
    st.markdown("**Oficina de Inclusión Social:**")
    st.write("""
    La Oficina de Inclusión Social trabaja para promover la inclusión 
    de las personas con discapacidad y garantizar sus derechos.
    """)

    fig = px.bar(
        data["inclusion_social"],
        x="Actividad",
        y="Participantes",
        title="Actividades de Inclusión Social 2023",
        color_discrete_sequence=COLOR_PALETTE
    )
    fig.update_layout(xaxis_title="Actividades", yaxis_title="Cantidad de Participantes")
    st.plotly_chart(fig)

    st.write("""
    Se realizaron actividades de equinoterapia, rehabilitación integral 
    para niños, rehabilitación para miembros de organizaciones de 
    discapacidad, y capacitaciones a dirigentes sobre el trato a 
    personas con discapacidad.
    """)

# ... (Secciones "Equipo de Operaciones", "Plan de Inversiones en 
# Infraestructura" y "Complejo El Tabo" por completar) ...

elif seccion == "Equipo de Operaciones":
    # ... (Añade el código para esta sección) ...
    st.header("Equipo de Operaciones:  [Nombre de la sección]")
    st.write("""
    [Descripción de la sección y análisis de los datos presentados.]
    """)
    # Asegúrate de tener datos para esta sección y visualizaciones.

elif seccion == "Plan de Inversiones en Infraestructura":
    # ... (Añade el código para esta sección) ...
    st.header("Plan de Inversiones en Infraestructura: [Nombre de la sección]")
    st.write("""
    [Descripción de la sección y análisis de los datos presentados.]
    """)
    # Asegúrate de tener datos para esta sección y visualizaciones.

elif seccion == "Complejo El Tabo":
    # ... (Añade el código para esta sección) ...
    st.header("Complejo El Tabo:  [Nombre de la sección]")
    st.write("""
    [Descripción de la sección y análisis de los datos presentados.]
    """)
    # Asegúrate de tener datos para esta sección y visualizaciones.


# Mensaje final en la sidebar
st.sidebar.markdown("---")
st.sidebar.write("**Este dashboard presenta los avances de Doñihue en 2023.**")
st.sidebar.write("**#DoñihueTradiciónyProgreso**")
