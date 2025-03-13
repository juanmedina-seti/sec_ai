import streamlit as st

st.title("App para encuestas de seguridad")
st.divider()
#st.logo()

pg = st.navigation(
    {
        "Buscar": [st.Page("navegacion/Busqueda.py", title="Búsqueda",)],
        "Administración": [st.Page("navegacion/azuresearch.py",title="Base de datos" ),
                           st.Page("navegacion/Carga_inicial.py",title="Carga inicial" ),
                          # st.Page("navegacion/Nueva.py",title="Nueva Pregunta" ),
                           st.Page("navegacion/Explorar.py",title="Explorar" )
                           ]
                           
    }
)

pg.run()
